# Hugging Face Spaces Deployment Guide

## 🎯 Why Hugging Face Spaces?

- ✅ **16GB RAM** (free tier with persistent storage)
- ✅ **Perfect for ML models** (designed for it!)
- ✅ **No credit card required**
- ✅ **Persistent storage** for cached models
- ✅ **Docker support**
- ✅ **Easy deployment** from GitHub

---

## 🚀 Deployment Steps

### **Step 1: Create Hugging Face Account**

1. Go to: https://huggingface.co/join
2. Sign up (free)
3. Verify your email

### **Step 2: Create a New Space**

1. Go to: https://huggingface.co/new-space
2. Fill in details:
   - **Owner:** Your username
   - **Space name:** `shl-recommendation-system`
   - **License:** MIT
   - **Select SDK:** Docker
   - **Space hardware:** CPU basic (free) or T4 small (upgrade for faster)
   - **Visibility:** Public (or Private if you prefer)
3. Click **"Create Space"**

### **Step 3: Enable Persistent Storage (Important!)**

1. In your Space, go to **"Settings"**
2. Scroll to **"Persistent storage"**
3. Click **"Enable persistent storage"**
4. This keeps your downloaded models cached!

### **Step 4: Set Environment Variables**

1. In Space Settings, scroll to **"Repository secrets"**
2. Click **"New secret"**
3. Add:
   - **Name:** `GROQ_API_KEY`
   - **Value:** `your_actual_groq_api_key`
4. Click **"Add secret"**

### **Step 5: Deploy from GitHub**

#### **Option A: Direct GitHub Integration (Recommended)**

1. In your Space, click **"Files and versions"** tab
2. Click **"Sync from GitHub"**
3. Authorize Hugging Face to access your GitHub
4. Select repository: `Prabhat9801/SHL_Recommendation_System`
5. Click **"Sync"**

**That's it!** Hugging Face will:
- Pull your code from GitHub
- Build the Docker image
- Download models (cached!)
- Start your API

#### **Option B: Manual Upload**

1. Clone your repo locally
2. In your Space, click **"Files"** tab
3. Click **"Add file"** → **"Upload files"**
4. Drag and drop all project files
5. Click **"Commit changes to main"**

#### **Option C: Git Push**

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/shl-recommendation-system
cd shl-recommendation-system

# Copy your project files
cp -r /path/to/SHL_Submission/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

---

## 📊 Monitor Deployment

### **Watch Build Logs:**

1. In your Space, go to **"Logs"** tab
2. You'll see:
   ```
   Building Docker image...
   Downloading models... (~500MB)
   ✅ ALL MODELS DOWNLOADED SUCCESSFULLY
   Starting server...
   INFO: Uvicorn running on http://0.0.0.0:7860
   Your Space is running!
   ```

**Build time:** 10-15 minutes (first time)
**Subsequent builds:** 2-3 minutes (models cached!)

---

## ✅ Test Your Deployed API

Once deployment is complete, your API will be at:
```
https://YOUR_USERNAME-shl-recommendation-system.hf.space
```

### **Health Check:**
```bash
curl https://YOUR_USERNAME-shl-recommendation-system.hf.space/health
```

### **Get Recommendations:**
```bash
curl -X POST https://YOUR_USERNAME-shl-recommendation-system.hf.space/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Python Developer with SQL skills", "top_k": 5}'
```

### **API Docs:**
```
https://YOUR_USERNAME-shl-recommendation-system.hf.space/docs
```

---

## 🔄 Update Your Frontend

After deployment, update `frontend/app.js`:

```javascript
// Change from Render URL to Hugging Face URL
const API_BASE_URL = 'https://YOUR_USERNAME-shl-recommendation-system.hf.space';
```

Then deploy frontend to Netlify as before!

---

## 📝 Files Created for Deployment

1. ✅ **`Dockerfile`** - Docker configuration for HF Spaces
2. ✅ **`README.md`** - Space description and documentation
3. ✅ **`.dockerignore`** - Excludes unnecessary files (create if needed)

---

## 🎛️ Space Configuration

### **Hardware Options:**

| Tier | RAM | CPU | Cost | Recommendation |
|------|-----|-----|------|----------------|
| **CPU basic** | 16GB | 2 cores | Free | ✅ Start here |
| **CPU upgrade** | 32GB | 8 cores | $0.03/hr | Heavy traffic |
| **T4 small** | 16GB | GPU | $0.60/hr | ML inference |

**For your app:** CPU basic (free) is perfect!

### **Persistent Storage:**

- **Tier:** 50GB included free
- **Purpose:** Caches downloaded models
- **Benefit:** Faster rebuilds (models don't re-download)

---

## 🆘 Troubleshooting

### **Build Fails:**

**Check:**
1. Dockerfile syntax
2. All files uploaded correctly
3. Build logs for specific errors

**Solution:**
- Click **"Restart Space"** in Settings
- Check "Logs" tab for details

### **Out of Memory:**

With 16GB RAM, this should NOT happen!

But if it does:
- Upgrade to **CPU upgrade** tier (32GB RAM)

### **API Returns 503:**

**Cause:** Space is sleeping (inactive for 48 hours)

**Solution:**
- Visit your Space URL - it will wake up (30 seconds)
- Or upgrade to **persistent** hardware (never sleeps)

### **Can't Find Models:**

**Cause:** Persistent storage not enabled

**Solution:**
1. Go to Space Settings
2. Enable Persistent stor age
3. Restart Space

---

## 🎯 Best Practices

1. **Enable Persistent Storage**
   - Keeps models cached
   - Faster rebuilds

2. **Set Secrets Correctly**
   - Never commit `GROQ_API_KEY` to Git
   - Use Space secrets

3. **Monitor Usage**
   - Check "Analytics" tab
   - Watch for sleeps
   - Upgrade if needed

4. **Use README.md**
   - Good README shows up on Space page
   - Helps users understand your API

---

## 💰 Cost Comparison

| Platform | RAM | Monthly Cost | Build Time | Notes |
|----------|-----|--------------|------------|-------|
| **Render Free** | 512MB | $0 | 5 min | ❌ Too small |
| **Render Starter** | 2GB | $7 | 5 min | ✅ Works |
| **HF Spaces Free** | 16GB | $0 | 15 min | ✅ Perfect! |
| **HF Spaces Upgrade** | 32GB | ~$22/mo | 15 min | Overkill |

**Winner:** Hugging Face Spaces (Free) 🎉

---

## ✅ Deployment Checklist

### **Before Deployment:**
- [ ] Hugging Face account created
- [ ] Space created (Docker SDK)
- [ ] Persistent storage enabled
- [ ] GROQ_API_KEY added as secret
- [ ] Dockerfile created
- [ ] README.md updated

### **During Deployment:**
- [ ] Files uploaded to Space
- [ ] Build starts automatically
- [ ] Watch logs for "✅ ALL MODELS DOWNLOADED"
- [ ] Wait for "Your Space is running!"

### **After Deployment:**
- [ ] Test `/health` endpoint
- [ ] Test `/recommend` endpoint
- [ ] Visit `/docs` for API documentation
- [ ] Update frontend with Space URL
- [ ] Deploy frontend to Netlify

---

## 🎉 Success!

Once deployed, you'll have:

✅ **Backend API:** `https://USERNAME-shl-recommendation-system.hf.space`
✅ **API Docs:** `https://USERNAME-shl-recommendation-system.hf.space/docs`
✅ **16GB RAM** - More than enough!
✅ **Free forever** - No credit card needed!
✅ **90.4% accuracy** - Full semantic embeddings!

---

## 🔗 Next Steps

1. Deploy backend to Hugging Face Spaces
2. Get the Space URL
3. Update `frontend/app.js` with Space URL
4. Deploy frontend to Netlify
5. Share your live demo!

---

**Ready to deploy!** Create your Space now: https://huggingface.co/new-space 🚀
