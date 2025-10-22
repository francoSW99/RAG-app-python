import os

from src.file_processor import chunk_pdfs
from src.chroma_db import save_to_chroma_db
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI


if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"




# Process the documents
processed_documents = chunk_pdfs()
# Initialize the OpenAI Embedding Model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
# Save the documents to the database
db = save_to_chroma_db(processed_documents, embedding_model)

query = "What are the recommended steps for fertilizing a vegetable garden?"

# Perform similarity search with the query
docs = db.similarity_search_with_score(query, k=3)

context = "\n\n---\n\n".join([doc.page_content for doc, _score in docs])

# Define the prompt template
PROMPT_TEMPLATE = """
You have to answer the following question based on the given context:
{context}
Answer the following question:{question}
Provide a detailed answer.
Don't include non-relevant information.
"""

# Generate the prompt
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
prompt = prompt_template.format(context=context, question=query)

# Import OpenAI LLM model
model = ChatOpenAI()
response = model.predict(prompt)

print(response)

"""
Example Response:
The recommended steps for fertilizing a vegetable garden are as follows:

1. Establish the basic fertility level by applying the right kind and amount of fertilizer to your garden soil. This can be determined through a soil test, which will indicate the specific fertilizer needed.

2. Apply fertilizer to maintain the basic fertility level each year after it has been established. This ensures that your soil remains at the optimal fertility level for growing healthy plants.

3. If the soil test recommends "no basic application" due to adequate fertility levels, then skip this step and monitor the soil for any excess elements that may need to be addressed.

4. Plow or spade the soil after applying half of the recommended fertilizer to distribute it evenly throughout the top 7 inches of soil. This helps ensure that the plants receive the necessary nutrients for growth.

By following these steps, you can effectively fertilize your vegetable garden and promote healthy plant growth throughout the growing season.

"""

