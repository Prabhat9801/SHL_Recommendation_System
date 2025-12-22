# Complete Deployment Guide - Backend + Frontend

## 📋 Table of Contents

1. [Project Structure & Root Directory](#project-structure--root-directory)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Frontend Deployment (Netlify)](#frontend-deployment-netlify)
4. [Connecting Frontend to Backend](#connecting-frontend-to-backend)
5. [Complete Workflow](#complete-workflow)
6. [Testing](#testing)

---

## 📁 Project Structure & Root Directory

### **Root Directory: `SHL_Submission/`**

```
SHL_Submission/                          ← ROOT DIRECTORY (Repository Root)
├── .env                                 ← Environment variables (not committed)
├── .gitignore                          
├── .python-version                      ← Python 3.10.13
├── runtime.txt                          ← Python 3.10.13
├── requirements.txt                     ← All dependencies
├── download_models.py                   ← Pre-download models script
├── render.yaml                          ← Render configuration
├── main.py                              ← CLI script (local development)
├── README.md
│
├── backend/                             ← Backend API (FastAPI)
│   ├── main.py                          ← API endpoints (THIS RUNS ON RENDER)
│   ├── requirements.txt                 ← Backend-only dependencies
│   └── runtime.txt                      ← Python version
│
├── frontend/                            ← Frontend (Static Site)
│   ├── index.html                       ← Main HTML page
│   ├── app.js                           ← JavaScript (connects to backend)
│   └── styles.css                       ← Styling
│
├── modules/                             ← Core Logic (Used by backend)
│   ├── __init__.py
│   ├── recommender.py                   ← Main recommendation engine
│   ├── feature_extractor.py             ← TF-IDF + Embeddings
│   ├── llm_client.py                    ← Groq integration
│   ├── data_loader.py
│   ├── preprocessor.py
│   └── ... (7 more modules)
│
├── data/                                ← Essential Data
│   ├── shl_individual_test_solutions.csv
│   └── Gen_AI Dataset (1).xlsx
│
├── docs/                                ← Documentation
├── .model_cache/                        ← Models (created during build)
└── vector_storage/                      ← Cache (created at runtime)
```

### **Root Directory Explained:**

| Platform | Root Directory | What It Means |
|----------|---------------|---------------|
| **Local PC** | `C:\Users\prabh\Desktop\SHL\SHL_Submission\` | Your project folder |
| **GitHub** | Repository root | Where `render.yaml` is located |
| **Render (Backend)** | `.` (dot) | Repository root, runs from here |
| **Netlify (Frontend)** | `frontend/` | Subdirectory within repo |

---

## 🚀 Backend Deployment (Render)

### **Architecture:**

```
Render Build Process:
  Repository Root (SHL_Submission/)
  ↓
  1. pip install -r requirements.txt     ← Install all dependencies
  2. python download_models.py           ← Download sentence-transformers (~500MB)
  3. uvicorn backend.main:app            ← Start FastAPI from backend/main.py
     |
     ↓ imports from parent directory
     |
  modules/ folder                        ← Core logic used by backend
```

### **Step 1: Verify Configuration**

Your `render.yaml` (already correct):

```yaml
services:
  - type: web
    name: shl-recommender-api
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt && python download_models.py
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.10.13
      - key: TRANSFORMERS_CACHE
        value: /opt/render/project/src/.model_cache
      - key: SENTENCE_TRANSFORMERS_HOME
        value: /opt/render/project/src/.model_cache
    healthCheckPath: /health
```

**Key Points:**
- **Root Directory:** `.` (repository root)
- **Build Command:** Installs deps + downloads models
- **Start Command:** Runs `backend.main:app` (backend/main.py)
- **Working Directory:** Repository root (so backend can import from `modules/`)

### **Step 2: Push to GitHub**

```bash
# Navigate to project root
cd C:\Users\prabh\Desktop\SHL\SHL_Submission

# Check current status
git status

# Add all files
git add .

# Commit
git commit -m "Add model pre-download for Render deployment"

# Push to GitHub
git push origin main
```

### **Step 3: Create Render Service**

1. **Go to Render:** https://dashboard.render.com/

2. **New Web Service:**
   - Click **"New +"** → **"Web Service"**

3. **Connect GitHub:**
   - Click **"Connect account"** if not connected
   - Select repository: `Prabhat9801/SHL_Recommendation_System`
   - Branch: `main`

4. **Configure:**
   - **Name:** `shl-recommend er-api`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** Leave **BLANK** (uses repo root `.`)
   - **Environment:** Python 3
   - **Build Command:** (Auto-detected from render.yaml)
   - **Start Command:** (Auto-detected from render.yaml)

5. **Environment Variables:**
   - Click **"Advanced"** → **"Add Environment Variable"**
   - **Key:** `GROQ_API_KEY`
   - **Value:** `your_actual_groq_api_key_here`
   - (Other variables auto-detected from render.yaml)

6. **Create Service:**
   - Click **"Create Web Service"**
   - Build starts automatically

### **Step 4: Monitor Build**

**Expected build logs:**

```
==> Cloning from GitHub...
==> Installing dependencies...
==> pip install -r requirements.txt
Collecting fastapi==0.104.1...
Collecting sentence-transformers==2.2.2...
✅ Dependencies installed

==> python download_models.py
========================================
DOWNLOADING REQUIRED MODELS FOR DEPLOYMENT
========================================
📦 Downloading model: all-MiniLM-L6-v2
[Progress bars... ~500MB download]
✅ Model 'all-MiniLM-L6-v2' downloaded successfully!
✅ ALL MODELS DOWNLOADED SUCCESSFULLY
========================================

==> Build complete! 

==> Starting service...
==> uvicorn backend.main:app --host 0.0.0.0 --port $PORT
INFO: Started server process [1]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:10000
```

**Build time:** 5-10 minutes (model download)

### **Step 5: Get Backend URL**

Once deployed, Render gives you a URL:

```
https://shl-recommender-api.onrender.com
```

**Save this URL - you'll need it for the frontend!**

### **Step 6: Test Backend**

```bash
# Health check
curl https://shl-recommender-api.onrender.com/health

# Response: {"status":"healthy",...}

# API info
curl https://shl-recommender-api.onrender.com/

# Test recommendation
curl -X POST https://shl-recommender-api.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Python Developer with SQL skills", "top_k": 5}'
```

**✅ Backend is live!**

---

## 🌐 Frontend Deployment (Netlify)

### **Architecture:**

```
Frontend (Static Files):
  index.html
  app.js          ← Connects to backend API
  styles.css

  ↓ (deployed to Netlify)

User Browser → Frontend (Netlify) → API Call → Backend (Render)
```

### **Step 1: Update Frontend API URL**

**Before deployment, update the backend URL in `app.js`:**

**File:** `frontend/app.js`

**Change line 2 from:**
```javascript
const API_BASE_URL = 'http://localhost:8000';  // Local development
```

**To:**
```javascript
const API_BASE_URL = 'https://shl-recommender-api.onrender.com';  // Your Render URL
```

**Important:** Use **YOUR actual Render URL** from Step 5 above!

### **Step 2: Push Updated Frontend**

```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission

# Edit frontend/app.js (update API_BASE_URL)

git add frontend/app.js
git commit -m "Update frontend to use Render backend URL"
git push origin main
```

### **Step 3: Deploy on Netlify**

#### **Option A: Drag & Drop (Quickest)**

1. **Go to Netlify:** https://app.netlify.com/

2. **Drag & Drop:**
   - Click **"Add new site"** → **"Deploy manually"**
   - Drag the **`frontend/`** folder to the upload area
   - Wait for deployment (~30 seconds)

3. **Get URL:**
   - Netlify gives you: `https://random-name-123456.netlify.app`
   - You can change this in **"Site settings"** → **"Change site name"**

#### **Option B: Connect GitHub (Recommended)**

1. **Go to Netlify:** https://app.netlify.com/

2. **New Site from Git:**
   - Click **"Add new site"** → **"Import an existing project"**
   - Click **"GitHub"** → Authorize Netlify

3. **Select Repository:**
   - Choose: `Prabhat9801/SHL_Recommendation_System`

4. **Build Settings:**
   - **Branch:** `main`
   - **Base directory:** `frontend`  ← **IMPORTANT!  **
   - **Build command:** Leave blank (static site)
   - **Publish directory:** `.` (current directory)

5. **Deploy:**
   - Click **"Deploy site"**
   - Deployment takes ~1 minute

### **Step 4: Configure Custom Domain (Optional)**

1. **Site Settings** → **"Domain management"**
2. **Add custom domain** or **Change site name:**
   - Example: `shl-recommender.netlify.app`

### **Step 5: Enable HTTPS (Auto-enabled)**

Netlify automatically enables HTTPS. Your site will be:
```
https://your-site-name.netlify.app
```

---

## 🔗 Connecting Frontend to Backend

### **How It Works:**

```
1. User visits: https://your-site.netlify.app
   ↓
2. Loads: index.html, app.js, styles.css
   ↓
3. User enters query: "Python Developer"
   ↓
4. app.js sends POST request to:
   https://shl-recommender-api.onrender.com/recommend
   ↓
5. Backend processes request:
   - LLM extracts requirements
   - Searches assessments
   - Returns top recommendations
   ↓
6. app.js receives response and displays results
```

### **CORS Configuration:**

Your backend already has CORS enabled in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (including Netlify)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**This allows your Netlify frontend to call your Render backend!** ✅

### **Frontend API Configuration:**

**File:** `frontend/app.js` (Line 2)

```javascript
const API_BASE_URL = 'https://shl-recommender-api.onrender.com';

// Used in fetch calls:
fetch(`${API_BASE_URL}/recommend`, { ... })
```

---

## ✅ Complete Workflow

### **Full Deployment Steps:**

```bash
# 1. Update frontend API URL
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
# Edit frontend/app.js - update API_BASE_URL

# 2. Commit and push
git add .
git commit -m "Deploy backend and frontend"
git push origin main

# 3. Deploy Backend (Render)
# - Go to https://dashboard.render.com/
# - Create Web Service from GitHub
# - Root directory: . (blank)
# - Wait for build (5-10 min)
# - Get URL: https://shl-recommender-api.onrender.com

# 4. Update frontend with backend URL (if not done in step 1)
# Edit frontend/app.js - set API_BASE_URL to Render URL
git add frontend/app.js
git commit -m "Update frontend backend URL"
git push origin main

# 5. Deploy Frontend (Netlify)
# - Go to https://app.netlify.com/
# - New site from Git
# - Base directory: frontend
# - Deploy
# - Get URL: https://your-site.netlify.app
```

###**Result:**

- **Backend API:** `https://shl-recommender-api.onrender.com`
- **Frontend UI:** `https://your-site.netlify.app`
- **Connection:** Frontend calls backend API via HTTPS

---

## 🧪 Testing

### **Test Backend:**

```bash
# Health check
curl https://shl-recommender-api.onrender.com/health

# API docs
open https://shl-recommender-api.onrender.com/docs

# Test recommendation
curl -X POST https://shl-recommender-api.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer who collaborates", "top_k": 5}'
```

### **Test Frontend:**

1. Open: `https://your-site.netlify.app`
2. Enter query: "Python Developer with SQL skills"
3. Click "Get Recommendations"
4. Should see results within 2-3 seconds

### **Test Integration:**

1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Submit a query
4. Should see POST request to Render backend
5. Should receive 200 OK response
6. Results display on page

---

## 🎯 Deployment Checklist

### **Backend (Render):**
- [ ] `render.yaml` configured correctly
- [ ] `download_models.py` created
- [ ] `requirements.txt` has correct versions
- [ ] Pushed to GitHub
- [ ] Created Render service
- [ ] Set `GROQ_API_KEY` environment variable
- [ ] Build completed successfully
- [ ] Backend URL obtained
- [ ] Health endpoint returns 200 OK
- [ ] Recommend endpoint works

### **Frontend (Netlify):**
- [ ] Updated `app.js` with backend URL
- [ ] Pushed to GitHub
- [ ] Deployed to Netlify
- [ ] Base directory set to `frontend`
- [ ] Frontend URL obtained
- [ ] Site loads correctly
- [ ] API calls work
- [ ] Results display correctly

### **Integration:**
- [ ] Frontend can reach backend (CORS working)
- [ ] Recommendations return successfully
- [ ] No console errors
- [ ] Response time < 5 seconds

---

## 🆘 Troubleshooting

### **Backend Issues:**

**Build fails during model download:**
```
Solution: Check build logs, may need to retry deployment
```

**"Ran out of memory" error:**
```
Solution: Models now download during build (separate memory pool)
If still fails, contact Render support
```

**Backend starts but crashes on first query:**
```
Check logs: docker logs shl-backend
Ensure .model_cache/ was created during build
```

### **Frontend Issues:**

**CORS error in browser console:**
```
Error: "Access to fetch has been blocked by CORS policy"
Solution: Verify backend has CORS middleware enabled (it does!)
Check backend logs to see if request is reaching server
```

**"Failed to fetch" error:**
```
Check:
1. Backend URL in app.js is correct
2. Backend is running (visit /health endpoint)
3. No typos in URL
```

**Results not displaying:**
```
Check browser console for errors
Verify API response format matches frontend expectations
```

### **Integration Issues**

**Frontend loads but shows "API not running":**
```
1. Check if backend is deployed and running
2. Test backend directly with curl
3. Verify API_BASE_URL in app.js
```

---

## 📊 Summary

| Component | Platform | URL Pattern | Root Directory |
|-----------|----------|-------------|----------------|
| **Backend API** | Render | `https://shl-app.onrender.com` | `.` (repo root) |
| **Frontend** | Netlify | `https://shl-app.netlify.app` | `frontend/` |
| **Local Dev (Backend)** | Localhost | `http://localhost:8000` | Repo root |
| **Local Dev (Frontend)** | Localhost | `http://localhost:3000` | `frontend/` |

---

## 🎉 You're Done!

Your SHL Recommendation System is now live:

✅ **Backend:** Deployed on Render with pre-downloaded models
✅ **Frontend:** Deployed on Netlify as static site  
✅ **Integration:** Frontend successfully calls backend API
✅ **Performance:** 90.4% accuracy, models cached, fast responses

**Share your live demo:**
- Frontend: `https://your-site.netlify.app`
- API Docs: `https://shl-api.onrender.com/docs`

**Congratulations!** 🎊
