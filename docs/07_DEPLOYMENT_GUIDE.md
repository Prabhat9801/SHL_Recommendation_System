# Deployment Guide

**Document 7: Production Deployment Instructions**

---

## 🎯 **Deployment Overview**

We'll deploy:
1. **Backend API** → Render (free tier)
2. **Frontend** → Netlify (free tier)
3. **Code** → GitHub (version control)

**Total cost:** $0 (using free tiers)

---

## 📊 **Deployment Architecture**

```
GitHub Repository
    ↓
Render (Backend API)
    ↓
    API at: https://shl-api-xyz.onrender.com
    ↓
Netlify (Frontend)
    ↓
    Site at: https://shl-recommender.netlify.app
    ↓
Users access frontend → Frontend calls API → Results displayed
```

---

## 🚀 **Part 1: Deploy to GitHub**

### **Step 1: Initialize Git Repository**

```bash
cd SHL_Submission

# Initialize git
git init

# Create .gitignore (if not exists)
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Environment
.env
*.env

# Logs
logs/
*.log

# Generated files
vector_storage/
predicted_test_csv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOL
```

### **Step 2: Create GitHub Repository**

**Option A: Using GitHub CLI**
```bash
gh repo create shl-recommender --public --source=. --push
```

**Option B: Manual**
1. Go to https://github.com/new
2. Repository name: `shl-recommender`
3. Public or Private
4. Don't initialize with README
5. Create repository

### **Step 3: Push Code**

```bash
# Add all files
git add .

# Commit
git commit -m "SHL Assessment Recommendation System - 90.4% Recall@10"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/shl-recommender.git

# Push
git branch -M main
git push -u origin main
```

**Verify:** Visit your GitHub repo - code should be there!

---

## 🖥️ **Part 2: Deploy Backend to Render**

### **Step 1: Prepare for Render**

**Create `render.yaml` in project root:**
```yaml
services:
  - type: web
    name: shl-recommender-api
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: GROQ_API_KEY
        sync: false
```

### **Step 2: Create Render Account**

1. Go to: https://render.com
2. Sign up (free)
3. Connect GitHub account

### **Step 3: Create Web Service**

**In Render Dashboard:**

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `shl-recommender-api`
   - **Environment:** Python 3
   - **Build Command:**
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command:**
     ```bash
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Free

4. Add Environment Variable:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key

5. Click "Create Web Service"

### **Step 4: Wait for Deployment**

**Progress:**
```
[1/4] Building...              ██████░░░░  (2 min)
[2/4] Installing dependencies  ██████████  (3 min)
[3/4] Starting application...  ████░░░░░░  (1 min)
[4/4] Live!                    ██████████  ✅
```

**Total time:** ~5-8 minutes

### **Step 5: Verify API**

**Your API URL:**
```
https://shl-recommender-api.onrender.com
```

**Test:**
```bash
# Health check
curl https://shl-recommender-api.onrender.com/health

# Get recommendations
curl -X POST https://shl-recommender-api.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer", "top_k": 5}'
```

**View docs:**
```
https://shl-recommender-api.onrender.com/docs
```

---

## 🌐 **Part 3: Deploy Frontend to Netlify**

### **Step 1: Update Frontend Configuration**

**Edit `frontend/app.js`:**

Change:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

To:
```javascript
const API_BASE_URL = 'https://shl-recommender-api.onrender.com';
```

**Commit changes:**
```bash
git add frontend/app.js
git commit -m "Update API URL for production"
git push
```

### **Step 2: Create Netlify Account**

1. Go to: https://netlify.com
2. Sign up (free)
3. Can use GitHub login

### **Step 3: Deploy Frontend**

**Option A: Drag & Drop (Easiest)**

1. In Netlify dashboard, go to "Sites"
2. Drag `frontend/` folder onto upload area
3. Done! Site deploys instantly

**Your URL:**
```
https://random-name-123.netlify.app
```

**Option B: GitHub Integration**

1. "New site from Git"
2. Connect GitHub
3. Select repository
4. Configure:
   - **Base directory:** `frontend`
   - **Build command:** (leave empty)
   - **Publish directory:** `.` (current directory)
5. Deploy

### **Step 4: Custom Domain (Optional)**

**In Netlify:**
1. Site settings → Domain management
2. Click "Add custom domain"
3. Enter: `shl-recommender.yourdomain.com`
4. Follow DNS instructions

### **Step 5: Verify Frontend**

Visit your Netlify URL:
```
https://your-site.netlify.app
```

**Test:**
1. Enter query: "Java developer"
2. Click "Get Recommendations"
3. Should see 10 results!

---

## 🔧 **Part 4: Environment Configuration**

### **Render Environment Variables**

**In Render Dashboard:**
1. Select your service
2. Environment → Add Variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

3. Save (triggers redeploy)

### **Netlify Environment Variables (if needed)**

**In Netlify Dashboard:**
1. Site settings → Environment variables
2. Add any needed variables

---

## 📊 **Part 5: Monitoring & Logs**

### **Render Logs**

**View logs:**
1. Render dashboard → Your service
2. "Logs" tab
3. Real-time logs displayed

**Common issues:**
- Port binding errors
- Missing dependencies
- Environment variable issues

### **Netlify Logs**

**View deploy logs:**
1. Netlify dashboard → Your site
2. "Deploys" tab
3. Click on a deploy → "Deploy log"

---

## 🚨 **Troubleshooting Deployment**

### **Issue 1: Render Build Fails**

**Error:**
```
Error: Could not find a version that satisfies the requirement
```

**Solution:**
```bash
# Update requirements.txt with exact versions
pip freeze > backend/requirements.txt
git add backend/requirements.txt
git commit -m "Pin dependency versions"
git push
```

---

### **Issue 2: API Returns 500 Error**

**Check Render logs:**
```
ERROR: GROQ_API_KEY not set
```

**Solution:**
1. Render dashboard → Environment
2. Add `GROQ_API_KEY`
3. Redeploy

---

### **Issue 3: Frontend Can't Connect to API**

**Error in browser console:**
```
CORS error: Access-Control-Allow-Origin
```

**Solution Already Implemented:**
```python
# backend/main.py already has CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allows all origins
)
```

**If still failing:**
- Check API URL in `frontend/app.js`
- Ensure API is deployed and running
- Check browser network tab

---

### **Issue 4: Slow Cold Starts (Render Free Tier)**

**Symptom:**
First request after 15 min takes 30+ seconds

**Explanation:**
- Render free tier spins down after 15 min inactivity
- First request wakes it up (slow)
- Subsequent requests are fast

**Solutions:**
1. **Accept it** (free tier limitation)
2. **Upgrade to paid** ($7/month - no sleep)
3. **Ping service** every 10 min to keep alive:
   ```bash
   # Use cron-job.org or similar
   curl https://your-api.onrender.com/health
   ```

---

## 📈 **Performance Optimization**

### **Backend Optimization**

**Enable caching:**
```python
# Add to backend/main.py
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_recommend(query: str):
    return engine.recommend(query)
```

**Use production settings:**
```bash
# In Render start command:
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2
```

### **Frontend Optimization**

**Minify files (optional):**
```bash
# Install terser
npm install -g terser

# Minify JavaScript
terser frontend/app.js -o frontend/app.min.js
```

**Update index.html:**
```html
<script src="app.min.js"></script>
```

---

## 🔒 **Security Considerations**

### **API Security**

**Already implemented:**
- ✅ HTTPS (Render provides SSL)
- ✅ Environment variables for secrets
- ✅ Input validation (Pydantic)
- ✅ CORS configured

**Additional (optional):**
```python
# Rate limiting
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/recommend")
@limiter.limit("10/minute")
def recommend(...):
    ...
```

### **Frontend Security**

- ✅ HTTPS (Netlify provides SSL)
- ✅ No sensitive data in frontend code
- ✅ API calls use HTTPS

---

## 📊 **Monitoring Setup**

### **Render Built-in Monitoring**

**Available metrics:**
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

**Access:** Render dashboard → Metrics tab

### **Uptime Monitoring (Optional)**

**Use UptimeRobot (free):**
1. Sign up: https://uptimerobot.com
2. Add monitor
3. URL: Your Render API URL
4. Check interval: 5 minutes
5. Get alerts if down

---

## 🎯 **Deployment Checklist**

### **Pre-Deployment**
- [ ] Code tested locally
- [ ] All tests passing
- [ ] Environment variables documented
- [ ] .gitignore configured
- [ ] README updated

### **GitHub**
- [ ] Repository created
- [ ] Code pushed
- [ ] .env excluded from git
- [ ] README has setup instructions

### **Render (Backend)**
- [ ] Account created
- [ ] Service deployed
- [ ] Environment variables set
- [ ] Health endpoint working
- [ ] API docs accessible

### **Netlify (Frontend)**
- [ ] Account created
- [ ] Site deployed
- [ ] API URL updated in code
- [ ] Frontend loads correctly
- [ ] Can make API calls

### **Final Verification**
- [ ] End-to-end test from frontend
- [ ] Recommendations returned
- [ ] Logs show no errors
- [ ] Performance acceptable

---

## 🚀 **Go Live!**

### **Your Deployed URLs:**

**GitHub:**
```
https://github.com/YOUR_USERNAME/shl-recommender
```

**Backend API:**
```
https://shl-recommender-api.onrender.com
```

**Frontend:**
```
https://shl-recommender.netlify.app
```

**API Docs:**
```
https://shl-recommender-api.onrender.com/docs
```

---

## 📝 **Post-Deployment**

### **Update Documentation**

**Add to README:**
```markdown
## 🌐 Live Demo

- **Frontend:** https://shl-recommender.netlify.app
- **API:** https://shl-recommender-api.onrender.com
- **API Docs:** https://shl-recommender-api.onrender.com/docs
```

### **Share Links**

For submission, provide:
1. ✅ GitHub URL (code repository)
2. ✅ API URL (backend endpoint)
3. ✅ Frontend URL (web interface)

---

## 🎊 **Deployment Complete!**

**You now have:**
- ✅ Code on GitHub (version controlled)
- ✅ API deployed on Render (accessible worldwide)
- ✅ Frontend on Netlify (beautiful interface)
- ✅ All working together seamlessly!

**Total cost:** $0 (free tiers)
**Uptime:** 24/7 (with cold starts on free tier)
**SSL:** Automatic (HTTPS enabled)

---

**Your SHL Recommendation System is now live!** 🎉
