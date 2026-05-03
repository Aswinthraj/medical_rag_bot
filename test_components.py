"""Test individual components of the RAG system"""
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("=" * 60)
print("Testing RAG Components")
print("=" * 60)

# Test 1: GPU
print("\n[1] GPU Check:")
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# Test 2: Embeddings
print("\n[2] Loading Embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("✓ Embeddings loaded")

# Test 3: Vector Database
print("\n[3] Loading Vector Database...")
vectordb = Chroma(persist_directory="./vectorstore", embedding_function=embeddings)
print(f"✓ Vector DB loaded")

# Test 4: Query the database
print("\n[4] Testing Vector Search...")
query = "What is diabetes?"
docs = vectordb.similarity_search(query, k=3)
print(f"Found {len(docs)} relevant documents")
print("\nTop result preview:")
print("-" * 60)
print(docs[0].page_content[:300] if docs else "No documents found")
print("-" * 60)

# Test 5: LLM
print("\n[5] Testing LLM...")
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline

device = 0 if torch.cuda.is_available() else -1
print(f"Using device: {'GPU (cuda:0)' if device == 0 else 'CPU'}")

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device="cuda:0" if device == 0 else "cpu",
    max_length=256,
    model_kwargs={"torch_dtype": torch.float16} if device == 0 else {}
)

print("✓ LLM pipeline created")

# Test direct generation
print("\n[6] Testing Direct Generation...")
test_prompt = "Question: What is diabetes? Answer:"
result = generator(test_prompt, max_length=100)
print("Generated response:")
print(result[0]['generated_text'])

print("\n" + "=" * 60)
print("All components working!")
print("=" * 60)
