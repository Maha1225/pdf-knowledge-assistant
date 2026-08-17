# 📄 PDF Knowledge Assistant

An AI-powered **PDF Question Answering system** built using **Retrieval-Augmented Generation (RAG)**. Users can upload PDF documents and ask natural-language questions. The system retrieves relevant document content using semantic search and generates answers using a **local Llama 3.2 LLM through Ollama**.

## 🚀 Features

* Upload and process PDF documents
* Extract and chunk PDF text
* Generate semantic embeddings
* Store embeddings in **PostgreSQL + pgvector**
* Perform similarity-based document retrieval
* Generate context-aware answers using **Llama 3.2**
* Return relevant page and chunk sources
* REST API using **FastAPI**
* React-based frontend
* Dockerized PostgreSQL database
* Alembic database migrations
* Local LLM inference without requiring a cloud LLM API

## 🧠 RAG Pipeline

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
PostgreSQL + pgvector
    ↓
Semantic Similarity Search
    ↓
Relevant Context
    ↓
Llama 3.2 via Ollama
    ↓
Generated Answer
```

## 🛠️ Tech Stack

**Backend**

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic

**AI / RAG**

* Retrieval-Augmented Generation
* Sentence Transformers
* Vector Embeddings
* Ollama
* Llama 3.2 3B

**Database**

* PostgreSQL
* pgvector

**Frontend**

* React
* Vite
* Tailwind CSS

**Infrastructure**

* Docker
* Docker Compose

## 📁 Project Structure

```text
pdf-knowledge-assistant/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── rag/
│   │   ├── embeddings/
│   │   ├── ingestion/
│   │   ├── llm/
│   │   └── retrieval/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
├── frontend/
├── scripts/
├── storage/
├── tests/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Maha1225/pdf-knowledge-assistant.git
cd pdf-knowledge-assistant
```

### 2. Create Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start PostgreSQL + pgvector

```powershell
docker compose up -d
```

### 5. Run database migrations

```powershell
alembic upgrade head
```

### 6. Install and configure Ollama

Install Ollama and download the model:

```powershell
ollama pull llama3.2:3b
```

Verify:

```powershell
ollama list
```

### 7. Start the backend

```powershell
python -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 8. Start the frontend

Open a new terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🔌 API Endpoints

| Method | Endpoint                   | Description                       |
| ------ | -------------------------- | --------------------------------- |
| GET    | `/`                        | API status                        |
| GET    | `/health`                  | Health check                      |
| POST   | `/documents/upload`        | Upload a PDF                      |
| GET    | `/documents/{document_id}` | Get document details              |
| POST   | `/rag/ask`                 | Ask a question about the document |

### Example RAG Request

```json
{
  "question": "What projects are mentioned in the document?",
  "limit": 6
}
```

### Example Response

```json
{
  "answer": "The document mentions several projects...",
  "sources": [
    {
      "page_number": 1,
      "chunk_index": 1,
      "distance": 0.7579
    }
  ]
}
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
APP_NAME=PDF Knowledge Assistant
APP_ENV=development
DEBUG=true
DATABASE_URL=postgresql+psycopg://raguser:ragpassword123@localhost:5432/ragdb
UPLOAD_DIR=storage/uploads
CHUNK_SIZE=400
CHUNK_OVERLAP=50
TOP_K=6
```

**Never commit `.env` or API keys to GitHub.**

## 🧪 Testing

Test the local LLM:

```powershell
python test_ollama.py
```

Test the LLM service:

```powershell
python test_llm_service.py
```

Test retrieval:

```powershell
python test_retrieval.py
```

Test the complete RAG pipeline:

```powershell
python test_rag.py
```

## 🔮 Future Improvements

* Multi-document conversations
* OCR support for scanned PDFs
* Chat history
* User authentication
* Hybrid keyword + vector search
* Reranking for improved retrieval
* Streaming responses
* RAG evaluation metrics
* Cloud deployment

## 👩‍💻 Author

**Mahalakshmi Murugesh**

B.Tech CSE — Artificial Intelligence & Machine Learning

GitHub: https://github.com/Maha1225

LinkedIn: https://www.linkedin.com/in/mahalakshmimurugesh
