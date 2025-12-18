# 🚀 Deploy Frontend to Render - Quick Guide

**Your Backend is LIVE:** https://shl-recommendation-system-qfgu.onrender.com ✅

**Now deploy the Frontend in 5 minutes!**

---

## 📝 **Step-by-Step: Deploy Frontend**

### **Step 1: Go to Render Dashboard**

1. Visit: https://dashboard.render.com
2. You should be logged in already

---

### **Step 2: Create New Static Site**

1. Click **"New +"** (top right)
2. Select **"Static Site"**

---

### **Step 3: Connect Repository**

1. Select your repository: **SHL_Recommendation_System**
2. Click **"Connect"**

---

### **Step 4: Configure Static Site**

Fill in these details:

| Field | Value |
|-------|-------|
| **Name** | `shl-recommendation-frontend` |
| **Branch** | `main` |
| **Root Directory** | (leave blank) |
| **Build Command** | (leave blank) |
| **Publish Directory** | `frontend` |
| **Auto-Deploy** | Yes (default) |

---

### **Step 5: Create Static Site**

1. Click **"Create Static Site"** (bottom)
2. Wait **2-3 minutes**
3. Watch the deployment logs

---

## ✅ **Your Frontend Will Be Live!**

**Frontend URL will be:**
```
https://shl-recommendation-frontend.onrender.com
```

**Or custom:**
```
https://shl-recommendation-frontend-XXXX.onrender.com
```

---

## 🧪 **Test Your Live Application**

### **Option 1: Visit Frontend**
1. Go to your frontend URL
2. Enter query: "Java developer who collaborates"
3. Click "Get Recommendations"
4. Should see 10 recommendations! ✨

### **Option 2: Test Backend Directly**
Visit: https://shl-recommendation-system-qfgu.onrender.com/docs

Try the `/recommend` endpoint with:
```json
{
  "query": "Python developer needed",
  "top_k": 5
}
```

---

## 🔗 **Your Complete Live System**

**Backend API:**
- URL: https://shl-recommendation-system-qfgu.onrender.com
- Docs: https://shl-recommendation-system-qfgu.onrender.com/docs
- Health: https://shl-recommendation-system-qfgu.onrender.com/health

**Frontend:**
- URL: (will be available after deploying)

---

## ⚠️ **First Request May Be Slow**

**This is NORMAL!**

- Free tier services "sleep" after 15 min inactivity
- First request wakes them up (~30-60 seconds)
- Subsequent requests are fast
- This is expected behavior on free tier

**Just wait 30 seconds and it will work!**

---

## 📊 **Update README with Live Links**

Once frontend is deployed, add to your README:

```markdown
## 🌐 Live Demo

**Try it now:**
- 🖥️ **Frontend:** https://shl-recommendation-frontend.onrender.com
- 🔌 **API:** https://shl-recommendation-system-qfgu.onrender.com
- 📚 **API Docs:** https://shl-recommendation-system-qfgu.onrender.com/docs

**Note:** First request may take 30s (free tier cold start)
```

---

## ✅ **Deployment Checklist**

- [x] ✅ Backend deployed
- [x] ✅ Frontend updated to use backend URL
- [x] ✅ Changes pushed to GitHub
- [ ] 🔄 Frontend deployment in progress
- [ ] 🔄 Test end-to-end

---

## 🎉 **You're Almost There!**

**Just 5 more minutes to deploy frontend and you'll have:**
- ✅ Live backend API
- ✅ Live frontend interface
- ✅ Working end-to-end
- ✅ Shareable with anyone!

**Follow the steps above to deploy frontend now!** 🚀
