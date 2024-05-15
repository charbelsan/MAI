import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

def load_documents(directory_path):
    """
    Load .txt documents from the specified directory.

    Args:
        directory_path (str): The path to the directory containing the documents.

    Returns:
        list: A list of documents (each document is a string).
    """
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(directory_path, filename))
            documents.extend(loader.load())
    return documents

def create_index(documents):
    """
    Create an index for the documents using FAISS and OpenAI embeddings.

    Args:
        documents (list): A list of documents to index.

    Returns:
        FAISS: The FAISS index.
        list: The list of texts.
    """
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)
    return db.as_retriever(), texts

def rag_query(retriever, query, use_rag=True):
    """
    Perform a RAG query to retrieve relevant context for a given query.

    Args:
        retriever: The retriever constructed from the FAISS index.
        query: The query for which context is being retrieved.
        use_rag: Boolean flag to enable or disable RAG.

    Returns:
        str: The retrieved context if RAG is enabled, otherwise None.
    """
    if not use_rag:
        return None

    # Perform the RAG query using the retriever
    docs = retriever.invoke(query)
    return " ".join([doc.page_content for doc in docs])




# import os
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.retrievers.document_compressors import LLMChainFilter, ContextualCompressionRetriever
# from langchain.llms import OpenAI

# def pretty_print_docs(docs):
#     print(
#         f"\n{'-' * 100}\n".join(
#             [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
#         )
#     )

# def load_documents(directory_path):
#     """Load documents from a directory, converting PDFs and .txt files to text."""
#     loader = DirectoryLoader(directory_path, glob="**/*.pdf")
#     documents = loader.load()
#     return documents

# def create_retriever(documents):
#     """Create a FAISS retriever from the documents."""
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_documents(documents)
#     retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever()
#     return retriever

# def create_compression_retriever(retriever, llm):
#     """Create a ContextualCompressionRetriever using LLMChainFilter."""
#     _filter = LLMChainFilter.from_llm(llm)
#     compression_retriever = ContextualCompressionRetriever(
#         base_compressor=_filter, base_retriever=retriever
#     )
#     return compression_retriever

# def rag_query(retriever, query, use_rag=True):
#     """Query the retriever using RAG (Retrieval-Augmented Generation)."""
#     if not use_rag:
#         return None
#     docs = retriever.invoke(query)
#     pretty_print_docs(docs)
#     return docs
