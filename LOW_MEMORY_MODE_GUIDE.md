# LOW MEMORY MODE - Testing & Deployment Guide

## 🎯 What Changed

**Files Updated:**
1. ✅ `modules/recommender.py` - Added LOW_MEMORY environment variable check
2. ✅ `render.yaml` - Set `LOW_MEMORY=true` for Render deployment
3. ✅ `test_low_memory.bat` - Local testing script (NEW)

---

## 📊 Memory Comparison

| Mode | Semantic Embeddings | Memory Usage | Accuracy | Works on Render Free? |
|------|-------------------|--------------|----------|---------------------|
| **Normal** | ✅ Enabled | ~600MB | 90.4% | ❌ Out of memory |
| **LOW_MEMORY** | ❌ Disabled | ~250MB | ~70-75% | ✅ Works! |

---

## 🧪 Test Locally First

### **Method 1: Using Test Script (Easiest)**

```cmd
# Double-click this file or run in terminal:
test_low_memory.bat
```

**Expected output:**
```
================================================================================
INITIALIZING RECOMMENDATION SYSTEM
⚠️  LOW MEMORY MODE: Semantic embeddings DISABLED
⚠️  This reduces memory usage but may affect accuracy
================================================================================
✅ Loaded 377 assessments
✅ TF-IDF matrix shape: (377, 10000)
⚠️  SKIPPING semantic embeddings to reduce memory usage
    Using zero embeddings (semantic matching disabled)
✅ Zero embeddings created (memory saved!)
✅ Recommendation system ready!
```

### **Method 2: Manual Terminal Commands**

```cmd
# Set environment variable
set LOW_MEMORY=true

# Start backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Method 3: PowerShell**

```powershell
# Set environment variable
$env:LOW_MEMORY = "true"

# Start backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Test That It Works

Once backend starts:

### **1. Health Check**
```cmd
curl http://localhost:8000/health
```

### **2. Test Recommendation**
```cmd
curl -X POST http://localhost:8000/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Python Developer\", \"top_k\": 5}"
```

### **3. Check API Docs**
```
Open: http://localhost:8000/docs
```

---

## 🚀 Deploy to Render

Once you've tested locally and confirmed it works:

### **Step 1: Commit and Push**

```cmd
git add modules/recommender.py render.yaml
git commit -m "Enable LOW_MEMORY mode for Render deployment"
git push origin main
```

### **Step 2: Render Auto-Deploys**

Render will automatically detect the push and redeploy.

### **Step 3: Watch Build Logs**

You should see:
```
==> Building...
==> Running download_models.py
✅ ALL MODELS DOWNLOADED SUCCESSFULLY
==> Starting service...

INITIALIZING RECOMMENDATION ENGINE AT STARTUP
================================================================================
INITIALIZING RECOMMENDATION SYSTEM
⚠️  LOW MEMORY MODE: Semantic embeddings DISABLED
================================================================================
✅ Loaded 377 assessments
✅ TF-IDF matrix shape: (377, 10000)
⚠️  SKIPPING semantic embeddings to reduce memory usage
✅ Zero embeddings created (memory saved!)
✅ Recommendation system ready!

INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:10000
==> Your service is live 🎉
```

**No "Out of memory" error!** ✅

---

## 📝 What LOW_MEMORY Mode Does

### **Disabled:**
- ❌ Semantic embeddings (sentence-transformers model)
- ❌ Semantic similarity matching

### **Still Active:**
- ✅ TF-IDF keyword matching (primary scoring)
- ✅ Training pattern learning (huge boost!)
- ✅ LLM skill extraction (Groq)
- ✅ Technical skills matching
- ✅ Soft skills matching
- ✅ Test type matching

### **Result:**
- Memory: 600MB → 250MB ✅
- Accuracy: 90.4% → ~70-75%
- **But it WORKS on Render free tier!**

---

## 🔄 Switching Between Modes

### **Enable LOW_MEMORY (Render free tier):**
```yaml
# In render.yaml:
- key: LOW_MEMORY
  value: "true"
```

### **Disable LOW_MEMORY (Full accuracy):**
```yaml
# In render.yaml:
- key: LOW_MEMORY
  value: "false"
```

Or upgrade to Render Starter ($7/month, 2GB RAM) and set to `"false"`.

---

## ⚠️ Important Notes

1. **Models still download during build**
   - The download_models.py script still runs
   - Models are cached but won't be loaded into RAM in LOW_MEMORY mode
   - This is fine - the cache is there if you upgrade later

2. **Zero embeddings are created**
   - Instead of loading the model, we create an array of zeros
   - Semantic matching will always return 0 (no contribution to score)
   - Other signals (TF-IDF, training patterns, LLM) still work

3. **You can still get good results**
   - Training pattern learning is the biggest contributor (54.4% boost!)
   - TF-IDF is very effective for keyword matching
   - LLM extracts technical/soft skills

---

## 🎯 Recommendation

**For Render Free Tier:**
Use LOW_MEMORY=true (this fix)

**For Production:**
- Upgrade to Render Starter ($7/month)
- Or use a platform with more RAM (see COMPLETE_DEPLOYMENT_GUIDE.md)
- Set LOW_MEMORY=false for full 90.4% accuracy

---

## ✅ Deployment Checklist

- [ ] Test locally with `test_low_memory.bat`
- [ ] Verify you see "LOW MEMORY MODE" messages
- [ ] Test `/recommend` endpoint works
- [ ] Commit changes to git
- [ ] Push to GitHub
- [ ] Monitor Render deployment logs
- [ ] Verify "Your service is live 🎉" message
- [ ] No "Out of memory" error
- [ ] Test live backend URL

---

**Ready to test!** Run `test_low_memory.bat` now! 🚀
