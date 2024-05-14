import os
import faiss
import numpy as np
from langchain.document_loaders import SimpleDirectoryReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

# Load documents from a directory containing PDFs
def load_documents(directory: str):
    return SimpleDirectoryReader(directory).load()

# Create an index for the documents using FAISS
def create_index(documents):
    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectors = [embeddings.embed(document.content) for document in texts]

    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype(np.float32))

    return index, texts

# Perform a RAG query
def rag_query(index, texts, query: str):
    embeddings = OpenAIEmbeddings()
    query_vector = embeddings.embed(query).astype(np.float32).reshape(1, -1)

    _, indices = index.search(query_vector, k=5)
    results = [texts[i[0]].content for i in indices]

    return "\n".join(results)
