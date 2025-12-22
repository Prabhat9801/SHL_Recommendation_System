# Deployment Checklist - Step by Step

## ✅ Pre-Deployment Checklist

- [ ] All code changes committed to Git
- [ ] `download_models.py` created
- [ ] `render.yaml` configured correctly  
- [ ] `requirements.txt` updated (groq==0.11.0)
- [ ] `modules/feature_extractor.py` uses cache
- [ ] Backend tested locally: `uvicorn backend.main:app --reload`
- [ ] Frontend tested locally: `python -m http.server 3000` (in frontend/)
- [ ] Have GROQ_API_KEY ready

---

## 🚀 Backend Deployment (Render)

### Step 1: Push to GitHub
```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
git add .
git commit -m "Deploy backend with model pre-download"
git push origin main
```
- [ ] Pushed to GitHub successfully

### Step 2: Create Render Service
1. [ ] Go to https://dashboard.render.com/
2. [ ] Click "New +" → "Web Service"
3. [ ] Connect GitHub account (if not connected)
4. [ ] Select repository: `Prabhat9801/SHL_Recommendation_System`
5. [ ] Branch: `main`

### Step 3: Configure Service
1. [ ] Name: `shl-recommender-api`
2. [ ] Region: Oregon (US West)
3. [ ] Root Directory: Leave **BLANK** (or enter `.`)
4. [ ] Environment: Python 3
5. [ ] Build Command: (Auto-detected from render.yaml)
6. [ ] Start Command: (Auto-detected from render.yaml)

### Step 4: Set Environment Variables
1. [ ] Click "Advanced" → "Add Environment Variable"
2. [ ] Key: `GROQ_API_KEY`
3. [ ] Value: `paste_your_actual_groq_api_key_here`
4. [ ] Other variables auto-detected from render.yaml

### Step 5: Deploy
1. [ ] Click "Create Web Service"
2. [ ] Wait for build (5-10 minutes)
3. [ ] Watch build logs for:
   - [ ] "Installing dependencies" ✅
   - [ ] "Downloading model: all-MiniLM-L6-v2" ✅
   - [ ] "ALL MODELS DOWNLOADED SUCCESSFULLY" ✅
   - [ ] "Application startup complete" ✅

### Step 6: Get Backend URL
1. [ ] Build completed successfully
2. [ ] Copy URL: `https://shl-recommender-api.onrender.com`
3. [ ] Save this URL (needed for frontend)

### Step 7: Test Backend
```bash
# Test health endpoint
curl https://shl-recommender-api.onrender.com/health
```
- [ ] Returns: `{"status":"healthy",...}` ✅

```bash
# Test recommendation endpoint
curl -X POST https://shl-recommender-api.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Python Developer", "top_k": 5}'
```
- [ ] Returns list of recommendations ✅

---

## 🌐 Frontend Deployment (Netlify)

### Step 1: Update Frontend API URL

1. [ ] Open `frontend/app.js` in your editor
2. [ ] Find line 2: `const API_BASE_URL = 'http://localhost:8000';`
3. [ ] Change to: `const API_BASE_URL = 'https://shl-recommender-api.onrender.com';`
   - **Use YOUR actual Render URL from backend deployment**
4. [ ] Save file

### Step 2: Commit and Push
```bash
cd C:\Users\prabh\Desktop\SHL\SHL_Submission
git add frontend/app.js
git commit -m "Update frontend to use Render backend URL"
git push origin main
```
- [ ] Pushed successfully

### Step 3: Deploy on Netlify

#### Option A: Drag & Drop (Quickest)
1. [ ] Go to https://app.netlify.com/
2. [ ] Click "Add new site" → "Deploy manually"
3. [ ] Drag the entire `frontend/` folder to upload area
4. [ ] Wait for deployment (~30 seconds)
5. [ ] Get URL: `https://random-name.netlify.app`

#### Option B: GitHub (Recommended)
1. [ ] Go to https://app.netlify.com/
2. [ ] Click "Add new site" → "Import an existing project"
3. [ ] Click "GitHub" → Authorize Netlify
4. [ ] Select repository: `Prabhat9801/SHL_Recommendation_System`
5. [ ] Configure:
   - Branch: `main`
   - Base directory: `frontend`  ← **CRITICAL!**
   - Build command: (leave blank)
   - Publish directory: `.`
6. [ ] Click "Deploy site"
7. [ ] Wait for deployment (~1 minute)

### Step 4: Get Frontend URL
1. [ ] Deployment completed
2. [ ] Copy URL: `https://your-site-name.netlify.app`
3. [ ] Optional: Change site name in Settings

### Step 5: Test Frontend
1. [ ] Open: `https://your-site-name.netlify.app`
2. [ ] Page loads correctly ✅
3. [ ] No console errors (F12 → Console) ✅
4. [ ] Enter test query: "Python Developer with SQL skills"
5. [ ] Click "Get Recommendations"
6. [ ] Results appear within 2-3 seconds ✅
7. [ ] Assessment details displayed correctly ✅

---

## 🔗 Integration Testing

### Test Complete Flow
1. [ ] Open frontend: `https://your-site.netlify.app`
2. [ ] Open browser DevTools (F12)
3. [ ] Go to "Network" tab
4. [ ] Enter query and submit
5. [ ] Verify:
   - [ ] POST request to backend visible in Network tab
   - [ ] Request URL: `https://shl-api.onrender.com/recommend`
   - [ ] Status: 200 OK
   - [ ] Response has recommendations array
   - [ ] Frontend displays results

### Common Queries to Test
- [ ] "Python Developer with SQL skills"
- [ ] "Java developer who can collaborate with business teams"
- [ ] "Mid-level professionals proficient in Python, SQL and JavaScript"
- [ ] "Leadership and teamwork skills"
- [ ] "Data Analyst with Excel and visualization skills"

---

## 📊 Deployment Summary

| Component | Platform | URL | Status |
|-----------|----------|-----|--------|
| **Backend API** | Render | `https://shl-api.onrender.com` | [ ] ✅ |
| **Frontend** | Netlify | `https://yoursite.netlify.app` | [ ] ✅ |
| **API Docs** | Render | `https://shl-api.onrender.com/docs` | [ ] ✅ |

---

## 🎯 Final Verification

- [ ] Backend health check returns 200 OK
- [ ] Backend /recommend endpoint works
- [ ] Frontend loads without errors
- [ ] Frontend can reach backend (no CORS errors)
- [ ] Test query returns recommendations
- [ ] Results display correctly on frontend
- [ ] Response time < 5 seconds
- [ ] No console errors in browser
- [ ] Mobile responsive (test on phone)

---

## 📝 Post-Deployment

### Save Your URLs
**Backend:** `_____________________________________`

**Frontend:** `_____________________________________`

**API Docs:** `_____________________________________`

### Share Your Project
- [ ] Add frontend URL to README.md
- [ ] Add backend URL to README.md
- [ ] Test sharing link with friend/colleague
- [ ] Update portfolio with live demo link

### Monitor
- [ ] Check Render dashboard for backend health
- [ ] Check Netlify dashboard for frontend traffic
- [ ] Monitor Render logs for errors
- [ ] Check browser console for frontend errors

---

## 🆘 Troubleshooting

### If Backend Build Fails:
1. Check build logs in Render dashboard
2. Verify requirements.txt has correct package versions
3. Ensure GROQ_API_KEY is set in environment variables
4. Try "Clear build cache" and redeploy

### If Frontend Shows CORS Error:
1. Verify backend URL in frontend/app.js is correct (no typos)
2. Check backend has CORS middleware (it does!)
3. Test backend directly with curl
4. Check browser console for exact error message

### If Results Don't Appear:
1. Open browser DevTools → Console tab
2. Check for JavaScript errors
3. Verify API call in Network tab
4. Check backend response format
5. Ensure frontend is displaying response correctly

---

## 🎉 Success!

Once all boxes are checked:

✅ Your SHL Recommendation System is **LIVE!**

✅ Backend deployed on Render with **cached models**

✅ Frontend deployed on Netlify as **static site**

✅ Frontend successfully calls backend API

✅ **90.4% accuracy** maintained

✅ Ready to share with the world!

---

**Congratulations!** 🎊🎊🎊

Your full-stack AI application is now deployed and accessible to anyone with the link!
