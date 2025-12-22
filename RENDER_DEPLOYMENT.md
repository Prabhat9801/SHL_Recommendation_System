# Render Deployment Guide - Pre-Download Models

## 🎯 What Changed?

**Problem:** Models were downloading when users made queries (causing 500MB+ downloads and memory issues)

**Solution:** Models now download **during deployment** (build time), not at runtime!

---

## 📦 How It Works

### 1. **Build Phase (Happens Once During Deployment)**
```bash
pip install -r requirements.txt && python download_models.py
```
- Installs all dependencies
- **Downloads sentence-transformers model** (~500MB)
- Caches model in `.model_cache/` directory
- ✅ Model ready before app starts

### 2. **Runtime Phase (When App Is Live)**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```
- App starts with **pre-downloaded model**
- User queries use **cached model** (no downloads!)
- ✅ Fast responses, no memory spikes

---

## 🚀 Deployment Steps

### On Render Dashboard:

1. **Create New Web Service**
   - Connect your GitHub repository

2. **Environment Variables** (Set these in Render dashboard)
   ```
   GROQ_API_KEY=your_groq_api_key_here
   PYTHON_VERSION=3.10.13
   TRANSFORMERS_CACHE=/opt/render/project/src/.model_cache
   SENTENCE_TRANSFORMERS_HOME=/opt/render/project/src/.model_cache
   ```

3. **Build & Start Commands** (Auto-detected from render.yaml)
   - **Build Command:** `pip install -r requirements.txt && python download_models.py`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy!**
   - Render will run the build command
   - Model downloads during build (visible in logs)
   - App starts with cached model

---

## 📋 Files Modified

1. **`download_models.py`** - New script to pre-download models
2. **`modules/feature_extractor.py`** - Updated to use cached models
3. **`render.yaml`** - Added build command with model download
4. **`.gitignore`** - Added `.model_cache/` directory

---

## ✅ What to Expect in Deployment Logs

### During Build:
```
========================================
DOWNLOADING REQUIRED MODELS FOR DEPLOYMENT
========================================

📦 Downloading model: all-MiniLM-L6-v2
📁 Cache directory: /opt/render/project/src/.model_cache
----------------------------------------
Downloading model files...
[Progress bars showing ~500MB download]
----------------------------------------
✅ Model 'all-MiniLM-L6-v2' downloaded successfully!
📊 Model cached at: /opt/render/project/src/.model_cache

🧪 Testing model...
✅ Model test successful! Embedding shape: (1, 384)

========================================
✅ ALL MODELS DOWNLOADED SUCCESSFULLY
========================================
```

### When App Starts:
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### When User Makes First Query:
```
Initializing modular recommendation engine...
Loading embedding model: all-MiniLM-L6-v2
✅ Loading from cache (NO DOWNLOAD!)
✅ Recommendation engine ready!
```

---

## 🧪 Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Download models (one-time)
python download_models.py

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Test the endpoint
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Software Developer with Python skills", "top_k": 5}'
```

---

## 💡 Key Benefits

1. ✅ **No runtime downloads** - Model ready before app starts
2. ✅ **Faster responses** - No delay on first query
3. ✅ **Lower memory usage** - Download happens in build phase (more memory available)
4. ✅ **No logic changes** - Same recommendation system, just optimized deployment
5. ✅ **Build-time verification** - If model download fails, deployment fails (not at runtime)

---

## 🔧 Troubleshooting

### If Build Fails

**Check logs for:**
```
❌ Error downloading models: [error message]
```

**Solutions:**
1. Verify internet connection during build
2. Check if Render has enough memory for build
3. Model download might timeout - retry deployment

### If Model Not Found at Runtime

**Check environment variables:**
```bash
TRANSFORMERS_CACHE=/opt/render/project/src/.model_cache
SENTENCE_TRANSFORMERS_HOME=/opt/render/project/src/.model_cache
```

---

## 📝 Manual Deployment (Without render.yaml)

If not using `render.yaml`, set these in Render dashboard:

**Build Command:**
```bash
pip install -r requirements.txt && python download_models.py
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
- `GROQ_API_KEY` = your_api_key
- `PYTHON_VERSION` = 3.10.13
- `TRANSFORMERS_CACHE` = /opt/render/project/src/.model_cache
- `SENTENCE_TRANSFORMERS_HOME` = /opt/render/project/src/.model_cache

---

## 🎉 Success Indicators

✅ Build logs show "ALL MODELS DOWNLOADED SUCCESSFULLY"
✅ App starts without downloading models
✅ First query responds quickly
✅ No "Downloading model..." messages in runtime logs
✅ Memory usage stays within Render's 512MB limit

---

**Your backend is now optimized for Render deployment!** 🚀

Models download once during build, not every time a user makes a query!
