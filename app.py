from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFacePipeline


from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate 

from transformers import pipeline
import os
import torch

# Increase timeout for model downloads
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '300'

# Initialize FastAPI
app = FastAPI(title="Offline Medical RAG Chatbot (Local Mode)")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Local Hugging Face Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load local vector database
vectordb = Chroma(persist_directory="./vectorstore", embedding_function=embeddings)

# Create a local LLM pipeline (Flan-T5)
# Auto-detect GPU availability
device = 0 if torch.cuda.is_available() else -1
device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
print(f"\n{'='*50}")
print(f"Using device: {'GPU' if device == 0 else 'CPU'}")
if device == 0:
    print(f"GPU Name: {device_name}")
print(f"{'='*50}\n")

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device="cuda:0" if device == 0 else "cpu",
    max_new_tokens=200,  # Reduced for faster response
    min_new_tokens=30,   # Reduced minimum
    do_sample=False,     # Greedy decoding for speed
    temperature=0.7,     # Lower temperature
    top_p=0.9,
    repetition_penalty=1.15,
    model_kwargs={"torch_dtype": torch.float16} if device == 0 else {}
)
llm = HuggingFacePipeline(pipeline=generator)

# Define an optimized prompt for better medical responses
PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are an expert medical AI assistant. Answer the medical question using ONLY the information provided in the context below.\n\n"
        "CONTEXT:\n{context}\n\n"
        "QUESTION: {question}\n\n"
        "INSTRUCTIONS:\n"
        "- Provide a clear, comprehensive answer based on the context\n"
        "- Include relevant medical terms and explanations\n"
        "- If the context doesn't contain enough information, state that clearly\n"
        "- Be accurate and professional\n\n"
        "ANSWER:"
    )
)

# Define the input model for the chatbot
class Query(BaseModel):
    query: str
    top_k: int

# POST endpoint for chatbot questions
@app.post("/ask")
def ask_medical_bot(request: Query):
    try:
        # Retrieve relevant documents based on top_k
        docs = vectordb.similarity_search(request.query, k=request.top_k)
        
        # Extract contexts from retrieved documents
        contexts = [doc.page_content for doc in docs]
        
        # Create retriever for QA chain
        retriever = vectordb.as_retriever(search_kwargs={"k": request.top_k})
        
        # Generate answer using QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        # Using .invoke() which is the new standard
        result_dict = qa_chain.invoke({"query": request.query})
        
        return {
            "answer": result_dict['result'],
            "contexts": contexts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve the frontend
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

# API info route
@app.get("/api")
def api_info():
    return {"message": "Welcome to the Offline Medical RAG Chatbot API (Local Mode)"}