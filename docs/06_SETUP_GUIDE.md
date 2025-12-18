# Setup Guide

**Document 6: Complete Installation & Configuration Instructions**

---

## 🎯 Prerequisites

### **System Requirements**
- **OS:** Windows 10+, macOS 10.15+, or Linux
- **Python:** 3.10 or later
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** 500 MB for dependencies + data

### **Required Accounts**
- **Groq API key** (free tier available)
  - Sign up: https://console.groq.com
  - Get API key from dashboard

---

## 📥 **Step 1: Clone/Download Project**

### **Option A: From GitHub**
```bash
git clone https://github.com/YOUR_USERNAME/shl-recommender.git
cd shl-recommender
```

### **Option B: From ZIP**
```bash
# Extract ZIP file
cd SHL_Submission
```

---

## 🐍 **Step 2: Python Environment Setup**

### **Verify Python Version**
```bash
python --version
# Should show: Python 3.10.x or higher
```

### **Create Virtual Environment (Recommended)**
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

---

## 📦 **Step 3: Install Dependencies**

### **Install All Requirements**
```bash
pip install -r requirements.txt
```

**This installs:**
- pandas, numpy (data handling)
- scikit-learn (TF-IDF)
- sentence-transformers (embeddings)
- groq (LLM API)
- fastapi, uvicorn (API)
- python-dotenv (config)
- openpyxl (Excel reading)

### **Verify Installation**
```bash
python -c "import pandas, numpy, sklearn, sentence_transformers, groq, fastapi; print('✅ All packages installed!')"
```

---

## 🔑 **Step 4: Configure Environment**

### **Create .env File**
```bash
# Copy example (if exists)
cp .env.example .env

# Or create new
# Add your Groq API key
```

**Edit `.env`:**
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### **Get Groq API Key**
1. Visit: https://console.groq.com
2. Sign up (free)
3. Go to API Keys section
4. Create new key
5. Copy and paste into `.env`

---

## 📂 **Step 5: Verify Data Files**

### **Check Required Files**
```bash
# Should exist:
data/shl_individual_test_solutions.csv      # 377 assessments
data/Gen_AI Dataset (1).xlsx                # Train/test data
```

### **Verify Data**
```bash
python -c "import pandas as pd; df = pd.read_csv('data/shl_individual_test_solutions.csv'); print(f'✅ {len(df)} assessments loaded')"
# Should print: ✅ 377 assessments loaded
```

---

## ✅ **Step 6: Test Core System**

### **Quick Test**
```bash
python -c "
from modules import DataLoader
loader = DataLoader()
data = loader.get_all_data()
print(f'✅ Loaded {len(data[\"scraped\"])} assessments')
print('✅ System working!')
"
```

**Expected output:**
```
✅ Loaded 377 assessments
✅ System working!
```

---

## 🚀 **Step 7: Run Main System**

### **Full System Test**
```bash
python main.py
```

**What happens:**
1. Loads data (2s)
2. Builds TF-IDF features (2s)
3. Builds semantic embeddings (3s)
4. Learns training patterns (1s)
5. Evaluates on train set (10s)
6. Shows 90.4% Mean Recall@10 ✅
7. Generates test predictions
8. Saves to `predicted_test_csv/test_predictions.csv`

**Time:** ~20 seconds

**Creates directories:**
- `vector_storage/` - Saved features
- `predicted_test_csv/` - Test predictions
- `logs/` - Log files

---

## 🌐 **Step 8: Run Backend API** (Optional)

### **Start API Server**
```bash
cd backend
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### **Test API**

**Health check:**
```bash
curl http://localhost:8000/health
```

**Get recommendations:**
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer", "top_k": 5}'
```

### **View API Docs**
Open browser: http://localhost:8000/docs

**Interactive testing available!**

---

## 🎨 **Step 9: Run Frontend** (Optional)

### **Option A: Simple HTTP Server**
```bash
cd frontend
python -m http.server 3000
```

Open browser: http://localhost:3000

### **Option B: Direct Open**
```bash
# Just open index.html in browser
open frontend/index.html  # macOS
start frontend/index.html  # Windows
```

**Note:** Update `API_BASE_URL` in `app.js` to your backend URL

---

## 🧪 **Step 10: Verify Everything Works**

### **Checklist**

```bash
# 1. Core system
python main.py
# ✅ Should complete without errors
# ✅ Should show 90.4% Mean Recall@10
# ✅ Should create vector_storage/
# ✅ Should create predicted_test_csv/

# 2. API (in separate terminal)
cd backend
uvicorn main:app --reload
# ✅ Should start on port 8000
# ✅ Visit http://localhost:8000/docs
# ✅ Test /health endpoint

# 3. Frontend
cd frontend
python -m http.server 3000
# ✅ Open http://localhost:3000
# ✅ Enter query and get results
```

---

## 🔧 **Troubleshooting**

### **Issue 1: ModuleNotFoundError**

**Error:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

---

### **Issue 2: GROQ_API_KEY not found**

**Error:**
```
WARNING: GROQ_API_KEY not set - LLM functionality will be limited
```

**Solution:**
```bash
# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Or set environment variable
export GROQ_API_KEY=your_key_here  # macOS/Linux
set GROQ_API_KEY=your_key_here     # Windows
```

---

### **Issue 3: File not found errors**

**Error:**
```
FileNotFoundError: data/shl_individual_test_solutions.csv
```

**Solution:**
```bash
# Ensure you're in correct directory
pwd  # Should show .../SHL_Submission

# Check data files exist
ls data/
# Should show: shl_individual_test_solutions.csv, Gen_AI Dataset (1).xlsx
```

---

### **Issue 4: Port already in use**

**Error:**
```
ERROR: Address already in use
```

**Solution:**
```bash
# Use different port
uvicorn main:app --reload --port 8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

---

### **Issue 5: Slow performance**

**Symptoms:**
- Takes >30s to initialize
- Queries take >10s

**Solutions:**
```bash
# 1. Check RAM usage
# Close other applications

# 2. Use smaller model (if needed)
# Edit modules/feature_extractor.py
# Change model to 'all-MiniLM-L6-v2' (already default)

# 3. Reduce TF-IDF features
# Edit modules/feature_extractor.py
# Change max_features=10000 to max_features=5000
```

---

### **Issue 6: Import errors**

**Error:**
```
ImportError: cannot import name 'RecommendationEngine'
```

**Solution:**
```bash
# Ensure __init__.py files exist
ls modules/__init__.py

# Try running from project root
cd SHL_Submission
python main.py
```

---

## 📊 **Performance Verification**

### **Expected Performance**

**System initialization:**
```
Loading data...              [2s]
Building TF-IDF...           [2s]
Building embeddings...       [3s]
Learning patterns...         [1s]
Total: ~8 seconds
```

**Per query:**
```
LLM extraction:              [1-2s]
Feature scoring:             [0.1s]
Total: ~2-3 seconds
```

**Memory usage:**
```
TF-IDF matrix:              1.5 MB
Semantic embeddings:        579 KB
Total:                      ~2.3 MB
```

---

## 🎯 **Quick Start Summary**

### **Minimal Setup**
```bash
# 1. Install Python 3.10+
# 2. Clone project
# 3. Create venv
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env
echo "GROQ_API_KEY=your_key" > .env

# 6. Run
python main.py
```

### **Full Setup**
```bash
# Steps 1-6 above, plus:

# 7. Start API
cd backend
uvicorn main:app --reload &

# 8. Start frontend
cd frontend
python -m http.server 3000 &

# 9. Open browser
# Visit http://localhost:3000
```

---

## 📁 **Generated Files After First Run**

```
SHL_Submission/
├── vector_storage/              # ✅ Created on first run
│   ├── tfidf_matrix.npz        # 1.5 MB
│   ├── semantic_embeddings.npy  # 579 KB
│   └── assessment_mapping.csv   # ~50 KB
├── predicted_test_csv/          # ✅ Created on first run
│   └── test_predictions.csv     # ~190 KB (submission file)
├── logs/                         # ✅ Created on first run
│   └── shl_recommender_YYYYMMDD.log
└── ...
```

---

## ✅ **Setup Complete!**

### **You now have:**
- ✅ Working recommendation system (90.4% accuracy)
- ✅ API running on port 8000
- ✅ Frontend running on port 3000
- ✅ Test predictions generated
- ✅ Logs for debugging

### **Next steps:**
- Test with your own queries
- Review logs in `logs/` folder
- Check predictions in `predicted_test_csv/`
- Deploy (see `07_DEPLOYMENT_GUIDE.md`)

---

## 📞 **Support**

**Common Issues:** Check troubleshooting section above

**Logs:** Check `logs/shl_recommender_*.log`

**Documentation:** See other docs in `docs/` folder

---

**Your system is ready to use!** 🎉
