from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document

def create_vector_store(df):
    docs = []
    for col in df.columns:
        docs.append(Document(page_content=f"{col}: {df[col].head().tolist()}"))
    
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

def retrieve_context(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=2)
    return "\n".join([d.page_content for d in docs])