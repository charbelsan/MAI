import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.retrievers.document_compressors import LLMChainFilter, ContextualCompressionRetriever
from langchain.llms import OpenAI

def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

def load_documents(directory_path):
    """Load documents from a directory, converting PDFs and .txt files to text."""
    loader = DirectoryLoader(directory_path, glob="**/*.pdf")
    documents = loader.load()
    return documents

def create_retriever(documents):
    """Create a FAISS retriever from the documents."""
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever()
    return retriever

def create_compression_retriever(retriever, llm):
    """Create a ContextualCompressionRetriever using LLMChainFilter."""
    _filter = LLMChainFilter.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=_filter, base_retriever=retriever
    )
    return compression_retriever

def rag_query(retriever, query, use_rag=True):
    """Query the retriever using RAG (Retrieval-Augmented Generation)."""
    if not use_rag:
        return None
    docs = retriever.invoke(query)
    pretty_print_docs(docs)
    return docs
