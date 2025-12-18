# 🚀 QUICK START: Deploy to Render

**30-second checklist for deploying SHL Recommendation System**

---

## Backend API Deployment

1. **Go to:** https://render.com → New + → Web Service
2. **Connect:** SHL_Recommendation_System repo
3. **Configure:**
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Env: `GROQ_API_KEY` = your key
4. **Deploy** → Get URL: `https://shl-recommender-api.onrender.com`

---

## Frontend Deployment

1. **Update** `frontend/app.js` line 2:
   ```javascript
   const API_BASE_URL = 'https://shl-recommender-api.onrender.com';
   ```

2. **Push to GitHub:**
   ```bash
   git add frontend/app.js
   git commit -m "Update API URL"
   git push origin main
   ```

3. **Render:** New + → Static Site
   - Publish dir: `frontend`
   - Deploy!

4. **Live at:** `https://shl-recommender-frontend.onrender.com`

---

## Test It!

**Frontend:** Open browser → Enter query → Get recommendations ✅  
**Backend:** Visit `/docs` endpoint → Try API ✅

---

**Total Time:** 15-20 minutes  
**Cost:** $0 (Free tier)  
**Result:** Live production system! 🎉
