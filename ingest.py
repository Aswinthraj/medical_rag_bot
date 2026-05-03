from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Initialize a local embedding model (runs on GPU if available)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingest_pdf(pdf_path, vectordb=None):
    """Load a single PDF and store embeddings in vector DB"""
    print(f"Loading {pdf_path} ...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print(f"   Found {len(documents)} pages")

    # Split text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    print(f"   Split into {len(docs)} chunks")

    # Create or add to existing Chroma vector store
    if vectordb is None:
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory="./vectorstore"
        )
    else:
        vectordb.add_documents(docs)
    
    print(f"Ingested {pdf_path}")
    return vectordb

if __name__ == "__main__":
    # Folder where all your PDFs are stored
    data_folder = r"C:\Users\Femilin Aswinth Raj\medical_rag_bot\data"

    # Automatically detect all PDF files in the folder
    pdf_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the data folder!")
    else:
        print(f"\n{'='*60}")
        print(f"Found {len(pdf_files)} PDF files to ingest")
        print(f"{'='*60}\n")
        
        vectordb = None
        for i, pdf in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] Processing: {os.path.basename(pdf)}")
            vectordb = ingest_pdf(pdf, vectordb)
        
        if vectordb:
            vectordb.persist()
            print(f"\n{'='*60}")
            print("ALL DOCUMENTS INGESTED SUCCESSFULLY!")
            print(f"{'='*60}\n")
