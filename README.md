# 📌 AI Skill Gap Analysis – Microservices Project  

This project is a **FastAPI-based microservices system** that performs **diagnosis, curriculum planning, prediction, and data ingestion** for AI-driven skill gap analysis.  

It follows a **gateway + microservices** architecture:  

```
ai-skill-gap-full/
│
├── gateway/        # API Gateway - central entry point
├── diagnose/       # Diagnose service
├── curriculum/     # Curriculum planner service
├── predict/        # Prediction service
├── ingestion/      # Data ingestion service
├── docker-compose.yml
└── README.md
```

---

## 🚀 Features
- **Gateway Service (port 8080):** Handles requests and routes them to appropriate services  
- **Diagnose Service (port 8001):** Analyzes student profiles and gaps  
- **Curriculum Service (port 8002):** Generates personalized learning curriculum  
- **Predict Service (port 8003):** Provides predictions based on progress  
- **Ingestion Service (port 8004):** Handles external data ingestion  

---

## ⚙️ Requirements  

- Python **3.9+** (tested with Python 3.11)  
- [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)  
- [HTTPX](https://www.python-httpx.org/) for async HTTP calls  
- Docker & Docker Compose (optional but recommended)  

---

## 🔧 Installation & Setup  

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-skill-gap-full.git
cd ai-skill-gap-full
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

Activate it:  
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Services  

You have **two options** to run:  

---

### 🟢 Option A: Run Locally (Multiple Terminals)  

Open **separate terminals** and run:

```bash
# Terminal 1 → Gateway
uvicorn gateway.main:app --reload --port 8080

# Terminal 2 → Diagnose
uvicorn diagnose.main:app --reload --port 8001

# Terminal 3 → Curriculum
uvicorn curriculum.main:app --reload --port 8002

# Terminal 4 → Predict
uvicorn predict.main:app --reload --port 8003

# Terminal 5 → Ingestion
uvicorn ingestion.main:app --reload --port 8004
```

---

### 🟠 Option B: Run with Docker Compose  

Make sure you have **Docker & Docker Compose** installed.  
Then simply run:

```bash
docker-compose up --build
```

This will spin up all services in one go 🎉  

---

## 📡 API Endpoints  

### Gateway (http://localhost:8080)
- `GET /health` → Health check  
- `POST /diagnose` → Send student profile & responses  
- `POST /curriculum` → Generate curriculum plan  
- `POST /predict` → Get predictions  
- `POST /ingest` → Ingest external data  

---

## 🛠 Example Usage with Postman  

### 1. Health Check  
**Request:**  
```http
GET http://localhost:8080/health
```  
**Response:**  
```json
{
  "status": "ok",
  "service": "gateway"
}
```

---

### 2. Diagnose API  
**Request:**  
```http
POST http://localhost:8080/diagnose
Content-Type: application/json
```  
**Body:**  
```json
{
  "student_profile": {"id": "s-123", "locale": "en-US"},
  "context": {"subject": "math", "taxonomy_version": "v3", "window_days": 28},
  "responses": [
    {"item_id": "i123", "type": "msq", "answer": ["A", "C"], "time_sec": 45}
  ]
}
```  
**Response:**  
```json
{
  "mastery_vector": [{"skill_id":"skill:fractions.add","score":0.56}],
  "gaps": ["fractions"]
}
```

---

### 3. Curriculum API  
**Request:**  
```http
POST http://localhost:8080/curriculum
Content-Type: application/json
```  
**Body:**  
```json
{
  "mastery_vector": [{"skill_id":"skill:fractions.add","score":0.56}],
  "constraints": {"pace_minutes_per_day": 30, "modality": ["video","practice"]}
}
```  
**Response:**  
```json
{
  "plan": [
    {"objective": "Improve Fractions", "activity": "Watch video lesson", "duration": 20}
  ]
}
```

---

### 4. Prediction API  
**Request:**  
```http
POST http://localhost:8080/predict
Content-Type: application/json
```  
**Body:**  
```json
{
  "student_profile": {"id": "s-123"},
  "context": {"subject": "math"}
}
```  
**Response:**  
```json
{
  "prediction": "pass",
  "confidence": 0.87
}
```

---

### 5. Ingestion API  
**Request:**  
```http
POST http://localhost:8080/ingest
Content-Type: multipart/form-data
```  
**Form Data:**  
- `dataset`: (file upload)  
- `source`: "manual"  

**Response:**  
```json
{
  "status": "success",
  "message": "File ingested successfully"
}
```

---

## ⚡ Troubleshooting  

- **Warning:** `model_config['protected_namespaces']`  
  → Fix: Add this in all Pydantic models:  
  ```python
  model_config = {"protected_namespaces": ()}
  ```

- **Error:** `httpx.ConnectError: All connection attempts failed`  
  → Fix: Make sure all microservices (`diagnose`, `curriculum`, `predict`, `ingestion`) are running.  

- **404 on `/`**  
  → Default FastAPI root path not defined. Use `/docs` or `/health`.  

---

## 📖 API Docs  

Once services are running, visit:  

- Gateway → [http://localhost:8080/docs](http://localhost:8080/docs)  
- Diagnose → [http://localhost:8001/docs](http://localhost:8001/docs)  
- Curriculum → [http://localhost:8002/docs](http://localhost:8002/docs)  
- Predict → [http://localhost:8003/docs](http://localhost:8003/docs)  
- Ingestion → [http://localhost:8004/docs](http://localhost:8004/docs)  

---
