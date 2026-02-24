from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embeddings)

def get_context(vector_store, question, k=3):
    docs = vector_store.similarity_search(question, k=k)
    return "\n".join([doc.page_content for doc in docs])