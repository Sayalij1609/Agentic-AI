from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Load vector database
vectorstore = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

# Retriever (top 3 relevant chunks)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Load Phi-3 model from Ollama
llm = Ollama(model="phi3")

def ask_question(query):
    # Step 1: Retrieve relevant documents (UPDATED METHOD)
    docs = retriever.invoke(query)

    # Step 2: Combine context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 3: Create prompt
    prompt = f"""
You are an AI assistant. Answer the question using the context below.

Context:
{context}
Question:
{query}
Answer:
"""

    # Step 4: Generate response using Phi-3
    response = llm.invoke(prompt)

    return response