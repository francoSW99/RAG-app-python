import os
from dotenv import load_dotenv

from src.file_processor import chunk_pdfs
from src.chroma_db import save_to_chroma_db
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Set your Groq API Key (get it from https://console.groq.com/)
# IMPORTANT: Create a .env file with GROQ_API_KEY=your-key-here
if not os.getenv("GROQ_API_KEY"):
    raise ValueError(
        "GROQ_API_KEY not found! Please follow these steps:\n"
        "1. Copy .env.example to .env\n"
        "2. Get your free API key from: https://console.groq.com/\n"
        "3. Add it to .env file: GROQ_API_KEY=your-api-key-here"
    )


# Process the documents
processed_documents = chunk_pdfs()

# Initialize HuggingFace Embedding Model (FREE and runs locally)
# Using 'all-MiniLM-L6-v2' - fast, efficient, and performs well
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},  # Use 'cuda' if you have GPU
    encode_kwargs={'normalize_embeddings': True}
)

# Save the documents to the database
db = save_to_chroma_db(processed_documents, embedding_model)

# Initialize Groq LLM (FREE API with fast inference)
# Available models: llama-3.3-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,  # For more deterministic outputs
)

# Define the prompt template
PROMPT_TEMPLATE = """
Based on the following context from the documents, answer the question below.

CONTEXT:
{context}

QUESTION: {question}

INSTRUCTIONS:
1. Provide a detailed and accurate answer based ONLY on the information in the context
2. At the end of your answer, cite the sources using the format: "Source: [document name]"
3. If the context doesn't contain relevant information, clearly state that the information is not available in the provided documents
4. Do not include information that is not supported by the context
5. Be concise but comprehensive

ANSWER:
"""
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

print("=" * 80)
print("RAG CHATBOT - Powered by Groq + HuggingFace (100% FREE)")
print("=" * 80)
print(f"Documents loaded: {len(processed_documents)} chunks")
print("Type 'exit', 'quit', or 'salir' to end the conversation")
print("=" * 80)

# Interactive chat loop
while True:
    # Get user query
    query = input("\nYour question: ").strip()

    # Check if user wants to exit
    if query.lower() in ['exit', 'quit', 'salir', 'q']:
        print("\nGoodbye! Thanks for using the RAG chatbot.")
        break

    # Skip empty queries
    if not query:
        print("Please enter a question.")
        continue

    # Perform similarity search with the query
    docs = db.similarity_search_with_score(query, k=3)

    # Build context from retrieved documents with source information
    context_parts = []
    sources = []
    for i, (doc, score) in enumerate(docs, 1):
        # Extract source information
        source = doc.metadata.get('source', 'Unknown')
        source_name = source.split('\\')[-1] if '\\' in source else source.split('/')[-1]

        # Get page number (ChromaDB stores it as 'page' in metadata)
        page_num = doc.metadata.get('page', 'Unknown')
        page_display = f"Page {page_num + 1}" if isinstance(page_num, int) else "Page Unknown"

        # Convert score to percentage (higher score = more relevant)
        # Note: Scores are distances, so we convert to similarity percentage
        relevance_percentage = (1 - score) * 100 if score <= 1 else 0

        # Add to context with source marker
        context_parts.append(f"[Source {i}: {source_name}, {page_display}]\n{doc.page_content}")
        sources.append(f"  📄 {source_name} - {page_display} ({relevance_percentage:.1f}% relevance to your question)")

    context = "\n\n---\n\n".join(context_parts)

    # Generate the prompt
    prompt = prompt_template.format(context=context, question=query)

    # Get response from Groq
    print("\nThinking...")
    response = model.invoke(prompt)

    # Display response with sources
    print(f"\nAnswer:\n{response.content}")
    print(f"\n📚 Information retrieved from:")
    for source in sources:
        print(source)
    print("\n" + "=" * 80)

"""
================================================================================
EXAMPLE CONVERSATION:
================================================================================

Your question: How can I prioritize my daily tasks effectively?

Thinking...

Answer:
Based on the provided context from the time management book, here are the key
strategies for prioritizing daily tasks effectively:

1. **Use the ABCDE Method**: Categorize tasks by importance - A tasks are critical,
   B tasks are important, C tasks are nice to do, D tasks can be delegated, and
   E tasks should be eliminated.

2. **Apply the 80/20 Rule**: Focus on the 20% of tasks that will generate 80% of
   your results. Identify your highest-value activities and concentrate on those.

3. **Work on Your Most Important Task First**: Start each day by tackling your
   most challenging and important task when your energy levels are highest.

4. **Plan Your Day the Night Before**: Take 10-15 minutes each evening to write
   down your priorities for the next day, which gives your subconscious time to
   work on solutions overnight.

Source: Administración del tiempo - Tracy Brayan.pdf (Pages 23, 45, 67)

📚 Information retrieved from:
  📄 Administración del tiempo - Tracy Brayan.pdf - Page 23 (85.2% relevance to your question)
  📄 Administración del tiempo - Tracy Brayan.pdf - Page 45 (78.6% relevance to your question)
  📄 Administración del tiempo - Tracy Brayan.pdf - Page 67 (72.3% relevance to your question)

================================================================================

Your question: exit

Goodbye! Thanks for using the RAG chatbot.
================================================================================
"""

