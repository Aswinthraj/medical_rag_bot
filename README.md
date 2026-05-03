# Medical RAG Bot

An offline medical chatbot using Retrieval-Augmented Generation (RAG) with FastAPI, LangChain, and ChromaDB.

## Features

- 📚 Local document ingestion and vectorization
- 🔍 Semantic search using Hugging Face embeddings
- 💬 RAG-based question answering
- 🚀 FastAPI backend with REST API
- 🎨 Interactive web frontend
- 🔒 Completely offline - no external API calls required

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd medical_rag_bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Ingest documents:
```bash
python ingest.py  # For full ingestion
# or
python ingest_quick.py  # For quick ingestion
```

## Usage

Start the server:
```bash
python app.py
```

Access the web interface at `http://localhost:8000`

## API Endpoints

- `POST /ask` - Ask a question and get RAG-based response
- `GET /` - Access the web interface

## Project Structure

```
medical_rag_bot/
├── app.py              # FastAPI application
├── ingest.py           # Full document ingestion
├── ingest_quick.py     # Quick ingestion script
├── requirements.txt    # Python dependencies
├── index.html          # Web frontend
├── style.css           # Frontend styling
├── data/               # Input documents
├── vectorstore/        # ChromaDB vector storage
└── tests/              # Test files
```

## License

MIT

## Author

[Your Name]
