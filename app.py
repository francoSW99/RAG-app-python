import os
import streamlit as st
from dotenv import load_dotenv

from src.file_processor import chunk_pdfs
from src.chroma_db import save_to_chroma_db
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot - Free AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "db" not in st.session_state:
    st.session_state.db = None
if "model" not in st.session_state:
    st.session_state.model = None
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # API Key input
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Get your free API key from https://console.groq.com/"
    )

    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

    # Model selection
    model_name = st.selectbox(
        "LLM Model",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"],
        help="Choose the Groq model for generation"
    )

    # Number of sources
    k_sources = st.slider(
        "Number of sources",
        min_value=1,
        max_value=10,
        value=3,
        help="How many document chunks to retrieve"
    )

    # Temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )

    st.markdown("---")

    # Initialize button
    if st.button("🚀 Initialize RAG System", use_container_width=True):
        if not api_key:
            st.error("Please enter your Groq API key!")
        else:
            with st.spinner("Loading documents and initializing models..."):
                try:
                    # Process documents
                    processed_documents = chunk_pdfs()

                    # Initialize embeddings
                    embedding_model = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/all-MiniLM-L6-v2",
                        model_kwargs={'device': 'cpu'},
                        encode_kwargs={'normalize_embeddings': True}
                    )

                    # Save to ChromaDB
                    st.session_state.db = save_to_chroma_db(processed_documents, embedding_model)

                    # Initialize LLM
                    st.session_state.model = ChatGroq(
                        model=model_name,
                        temperature=temperature,
                    )

                    st.session_state.initialized = True
                    st.success(f"✅ System initialized! {len(processed_documents)} chunks loaded.")

                except Exception as e:
                    st.error(f"Error initializing system: {str(e)}")

    # Status
    if st.session_state.initialized:
        st.success("✅ System Ready")
    else:
        st.warning("⚠️ System not initialized")

    st.markdown("---")

    # Info
    st.markdown("""
    ### 📚 About
    This RAG chatbot uses:
    - **Groq** (Free LLM)
    - **HuggingFace** (Free Embeddings)
    - **ChromaDB** (Vector Database)

    ### 🔗 Resources
    - [Get Groq API Key](https://console.groq.com/)
    - [GitHub Repo](https://github.com/francoSW99/RAG-app-python)
    """)

    # Clear chat
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content
st.markdown("<h1 class='main-header'>🤖 RAG Chatbot - Free AI Assistant</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #666; margin-bottom: 2rem;'>
    Ask questions about your documents with AI-powered search | 100% Free using Groq + HuggingFace
</div>
""", unsafe_allow_html=True)

# Check if system is initialized
if not st.session_state.initialized:
    st.info("👈 Please initialize the RAG system using the sidebar to start chatting!")

    # Display instructions
    with st.expander("📖 How to use", expanded=True):
        st.markdown("""
        1. **Get API Key**: Sign up at [console.groq.com](https://console.groq.com/) for a free API key
        2. **Enter API Key**: Paste it in the sidebar
        3. **Add Documents**: Place your PDF files in the `documents/` folder
        4. **Initialize**: Click the "🚀 Initialize RAG System" button
        5. **Start Chatting**: Ask questions about your documents!

        ### Example Questions:
        - "What are the main topics discussed in the document?"
        - "Summarize the key points from page 10"
        - "What does the author say about [specific topic]?"
        """)

else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Display sources if available
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.markdown(f"<div class='source-box'>{source}</div>", unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Perform similarity search
                    docs = st.session_state.db.similarity_search_with_score(prompt, k=k_sources)

                    # Build context with sources
                    context_parts = []
                    sources = []

                    for i, (doc, score) in enumerate(docs, 1):
                        source = doc.metadata.get('source', 'Unknown')
                        source_name = source.split('\\')[-1] if '\\' in source else source.split('/')[-1]
                        page_num = doc.metadata.get('page', 'Unknown')
                        page_display = f"Page {page_num + 1}" if isinstance(page_num, int) else "Page Unknown"
                        relevance_percentage = (1 - score) * 100 if score <= 1 else 0

                        context_parts.append(f"[Source {i}: {source_name}, {page_display}]\n{doc.page_content}")
                        sources.append(f"📄 **{source_name}** - {page_display} ({relevance_percentage:.1f}% relevant)")

                    context = "\n\n---\n\n".join(context_parts)

                    # Create prompt
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
                    formatted_prompt = prompt_template.format(context=context, question=prompt)

                    # Get response
                    response = st.session_state.model.invoke(formatted_prompt)

                    # Display response
                    st.markdown(response.content)

                    # Display sources
                    with st.expander("📚 Sources", expanded=True):
                        for source in sources:
                            st.markdown(f"<div class='source-box'>{source}</div>", unsafe_allow_html=True)

                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response.content,
                        "sources": sources
                    })

                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9rem;'>
    Made with ❤️ using Streamlit | Powered by Groq + HuggingFace |
    <a href='https://github.com/francoSW99/RAG-app-python' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
