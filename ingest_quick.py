from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

print("Quick Medical Document Ingestion")
print("=" * 60)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Select only the most important medical PDFs (smaller, faster)
data_folder = r"C:\Users\Femilin Aswinth Raj\medical_rag_bot\data"

# Priority documents (smaller files for faster processing)
priority_files = [
    "General.pdf",           # 62MB - General medical knowledge
    "InfectiousDisease.pdf", # 6MB - Infections
]

print(f"\nProcessing {len(priority_files)} priority medical documents...")
print("=" * 60)

vectordb = None

for i, filename in enumerate(priority_files, 1):
    pdf_path = os.path.join(data_folder, filename)
    
    if not os.path.exists(pdf_path):
        print(f"Skipping {filename} - file not found")
        continue
    
    print(f"\n[{i}/{len(priority_files)}] Processing: {filename}")
    
    try:
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"   Loaded {len(documents)} pages")
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(documents)
        print(f"   Created {len(docs)} chunks")
        
        # Add to vectorstore
        if vectordb is None:
            vectordb = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory="./vectorstore"
            )
            print(f"   Created vectorstore")
        else:
            vectordb.add_documents(docs)
            print(f"   Added to vectorstore")
            
    except Exception as e:
        print(f"   Error: {str(e)}")
        continue

if vectordb:
    vectordb.persist()
    print("\n" + "=" * 60)
    print("QUICK INGESTION COMPLETE!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Start the server: .\\start_app.ps1")
    print("2. Ask medical questions")
    print("\nTo add more documents later, run: python ingest.py")
else:
    print("\nNo documents were ingested")
