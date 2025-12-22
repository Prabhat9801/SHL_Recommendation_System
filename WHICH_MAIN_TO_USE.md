# Which main.py to Use?

## 📁 Two main.py Files Explained

Your project has **TWO** `main.py` files with different purposes:

---

## 1️⃣ **Root `main.py`** (Training/Evaluation Script)

**Location:** `C:\Users\prabh\Desktop\SHL\SHL_Submission\main.py`

**Purpose:** 
- CLI script for training and evaluation
- Generates test predictions
- Evaluates model performance
- Saves vectors to disk

**When to use:**
- ✅ Local development and testing
- ✅ Running evaluation scripts
- ✅ Generating test predictions
- ❌ **NOT for Render deployment**

**How to run locally:**
```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
python main.py
```

**What it does:**
- Initializes recommendation engine
- Runs evaluation (90.4% Recall@10)
- Generates test predictions CSV
- Saves TF-IDF and embeddings to disk

---

## 2️⃣ **Backend `main.py`** (FastAPI Web Server) ✅

**Location:** `C:\Users\prabh\Desktop\SHL\SHL_Submission\backend\main.py`

**Purpose:**
- FastAPI web server
- REST API endpoints
- Serves recommendations via HTTP

**When to use:**
- ✅ **Render deployment** ✅
- ✅ Production web server
- ✅ API for frontend
- ✅ Local API testing

**How to run locally:**
```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Endpoints:**
- `GET /` - API info
- `GET /health` - Health check
- `POST /recommend` - Get recommendations
- `GET /docs` - Interactive API docs

---

## 🚀 For Render Deployment

### ✅ **Use `backend/main.py`**

**render.yaml configuration:**
```yaml
services:
  - type: web
    name: shl-recommender-api
    env: python
    buildCommand: pip install -r requirements.txt && python download_models.py
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

**Key points:**
- `backend.main:app` tells uvicorn to:
  - Look in the `backend/` directory
  - Import the `main.py` file
  - Use the `app` object (FastAPI instance)

---

## 📊 Quick Comparison

| Aspect | `main.py` (root) | `backend/main.py` |
|--------|------------------|-------------------|
| **Type** | CLI Script | Web Server |
| **Framework** | Pure Python | FastAPI |
| **Usage** | Development/Testing | **Production API** ✅ |
| **Output** | Console logs, CSV files | HTTP responses |
| **Endpoints** | None | REST API |
| **For Render?** | ❌ No | ✅ **Yes** |
| **Run command** | `python main.py` | `uvicorn backend.main:app` |

---

## 🧪 Test Both Locally

### Test CLI Script (root main.py):
```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
python main.py
```
**Expected output:**
- Evaluation results
- Test predictions saved
- 90.4% Recall@10

### Test API Server (backend/main.py):
```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
**Then test:**
```bash
# Health check
curl http://localhost:8000/health

# Get recommendations
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Python Developer\", \"top_k\": 5}"
```

---

## ✅ Summary for Render

**Use this command in render.yaml:**
```bash
startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

**NOT this:**
```bash
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT  ❌ WRONG
```

---

## 🎯 Why Two Files?

1. **`main.py` (root)** - For development, testing, and evaluation
2. **`backend/main.py`** - For production web API deployment

Both use the same **modular architecture** (from `modules/`), just different interfaces.

---

**For Render deployment, always use `backend.main:app`!** ✅
