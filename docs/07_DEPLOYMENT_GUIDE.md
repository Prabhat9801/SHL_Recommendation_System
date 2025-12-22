# Deployment Guide

## Production Deployment

**Live API:** https://prabhat9801-shl-recommendation-system.hf.space

### Platform: Hugging Face Spaces

**Deployment Status:** ✅ Live and Running

**Configuration:**
- **Hardware:** CPU basic (16GB RAM, 2 vCPU) - Free tier
- **SDK:** Docker
- **Region:** Auto-selected by Hugging Face
- **Storage:** Persistent (models cached in Docker layers)

---

## 🚀 Accessing the API

### Base URL
```
https://prabhat9801-shl-recommendation-system.hf.space
```

### Endpoints

#### 1. Health Check
```bash
GET https://prabhat9801-shl-recommendation-system.hf.space/health
```

**Response:**
```json
{
  "status": "healthy",
  "system": "SHL Recommendation System",
  "version": "1.0.0"
}
```

#### 2. Get Recommendations
```bash
POST https://prabhat9801-shl-recommendation-system.hf.space/recommend
Content-Type: application/json

{
  "query": "Python developer with strong SQL skills",
  "top_k": 10
}
```

**Response:**
```json
{
  "query": "Python developer with strong SQL skills",
  "recommendations": [
    {
      "assessment_name": "Python Programming Test",
      "assessment_url": "https://www.shl.com/solutions/products/...",
      "description": "Comprehensive Python assessment...",
      "duration": 30,
      "test_type": ["Knowledge & Skills"],
      "relevance_score": 0.95
    },
    ...
  ],
  "total_recommended": 10,
  "processing_time_seconds": 2.3
}
```

#### 3. API Documentation
```
https://prabhat9801-shl-recommendation-system.hf.space/docs
```

Interactive Swagger UI with:
- API schema
- Try-it-out functionality
- Example requests/responses

---

## 🌐 Frontend Deployment

### Platform: Netlify

**Status:** Ready to deploy

### Steps:

1. **Go to Netlify:**
   ```
   https://app.netlify.com/
   ```

2. **Deploy:**
   - Click "Add new site" → "Deploy manually"
   - Drag `frontend/` folder
   - Wait 30 seconds
   - Done!

3. **Configuration:**
   - Base directory: `frontend`
   - Build command: (none - static site)
   - Publish directory: `.`

### Frontend Configuration

The frontend is pre-configured to connect to Hugging Face backend:

```javascript
// frontend/app.js
const API_BASE_URL = 'https://prabhat9801-shl-recommendation-system.hf.space';
```

---

## 🔧 Environment Variables

### Backend (Hugging Face Space)

Required secrets set in Space Settings:

| Variable | Value | Purpose |
|----------|-------|---------|
| `GROQ_API_KEY` | `your_groq_api_key` | LLM integration for skill extraction |

**How to set:**
1. Go to Space Settings
2. Scroll to "Variables and secrets"
3. Add secret: `GROQ_API_KEY`
4. Restart space

---

## 🏗️ Deployment Architecture

```
User Browser
    ↓
Frontend (Netlify)
    ↓ (API calls via fetch)
Backend (Hugging Face Spaces)
    ↓
FastAPI Server (port 7860)
    ↓
Recommendation Engine
    ├── TF-IDF Features
    ├── Semantic Embeddings (all-MiniLM-L6-v2)
    ├── Training Patterns
    └── LLM Client (Groq)
```

---

## 📊 Deployment Metrics

### Build Process
- **Time:** 10-15 minutes (first build)
- **Subsequent builds:** 2-3 minutes (cached)
- **Model download:** ~500MB (sentence-transformers)
- **Docker image size:** ~2.5GB

### Runtime Performance
- **Startup time:** 30-45 seconds
- **Memory usage:** ~600MB (well within 16GB limit)
- **Query response:** 2-3 seconds (includes LLM call)
- **Concurrent requests:** Handles multiple (limited by free tier)

### Uptime
- **Free tier:** Space sleeps after 48 hours inactivity
- **Wake time:** 30 seconds
- **Availability:** 99.9% (when active)

---

## 🔄 Updating Deployment

### Update Backend

```bash
# Make changes to code
git add .
git commit -m "Update backend"

# Push to GitHub
git push origin main

# Push to Hugging Face Space
git push hf main
```

Hugging Face automatically rebuilds on push.

### Update Frontend

1. Update `frontend/` files
2. Commit to Git
3. Redeploy to Netlify (drag folder again or use Netlify CLI)

---

## 🧪 Testing Deployed API

### cURL
```bash
# Health check
curl https://prabhat9801-shl-recommendation-system.hf.space/health

# Recommendation
curl -X POST https://prabhat9801-shl-recommendation-system.hf.space/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer", "top_k": 5}'
```

### Python
```python
import requests

response = requests.post(
    "https://prabhat9801-shl-recommendation-system.hf.space/recommend",
    json={"query": "Python developer with SQL", "top_k": 10}
)

print(response.json())
```

### JavaScript (Frontend)
```javascript
fetch('https://prabhat9801-shl-recommendation-system.hf.space/recommend', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        query: 'Data scientist with ML skills',
        top_k: 5
    })
})
.then(res => res.json())
.then(data => console.log(data.recommendations));
```

---

## 🛠️ Troubleshooting

### Space Returns 503
**Cause:** Space is sleeping (inactive 48 hours)  
**Solution:** Visit URL - wakes in 30 seconds

### Build Fails
**Check:**
1. Logs tab for error details
2. Dockerfile syntax
3. requirements.txt dependencies

**Solution:**
- Click "Factory rebuild" in Settings
- Check logs for specific error

### API Returns 500
**Possible causes:**
1. Missing GROQ_API_KEY secret
2. Model loading error
3. Data file missing

**Solution:**
1. Check Settings → Secrets
2. Check Logs for error traceback
3. Verify all files pushed correctly

### Slow Response
**Expected:** 2-3 seconds (includes LLM call)  
**If slower:**
- First request after wake: +30 seconds
- Check Groq API status
- Monitor Space resource usage

---

## 💰 Cost Analysis

| Component | Platform | Tier | Cost |
|-----------|----------|------|------|
| **Backend** | Hugging Face Spaces | CPU basic (Free) | $0/month |
| **Frontend** | Netlify | Free tier | $0/month |
| **LLM API** | Groq | Free tier | $0/month* |
| **Storage** | GitHub | Free tier | $0/month |
| **Domain** | HF subdomain | Included | $0/month |

**Total: $0/month**

*Groq free tier: Rate limited but sufficient for demo/testing

---

## 🔐 Security Considerations

1. **API Key:** Stored as secret in HF Space (not in code)
2. **CORS:** Enabled for frontend integration
3. **Rate Limiting:** Handled by Groq API
4. **Input Validation:** FastAPI automatic validation
5. **Public Access:** API is public (add auth if needed)

---

## 📈 Scaling Options

### If Traffic Increases:

**Option 1: Upgrade HF Space Hardware**
- CPU upgrade: 32GB RAM, 8 vCPU ($0.03/hour)
- Persistent (no sleep)

**Option 2: Add Caching**
- Redis for frequent queries
- Response caching

**Option 3: Load Balancing**
- Deploy multiple Spaces
- Use load balancer

**Option 4: Production Platform**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

---

## ✅ Deployment Checklist

### Backend (Hugging Face Spaces)
- [x] Space created
- [x] Docker configured (`Dockerfile`)
- [x] Dependencies listed (`requirements.txt`)
- [x] Models pre-download script (`download_models.py`)
- [x] Environment variables set (`GROQ_API_KEY`)
- [x] Code pushed to Space
- [x] Build completed successfully
- [x] API endpoints tested
- [x] Health check passes

### Frontend (Netlify)
- [ ] `frontend/app.js` updated with HF Space URL
- [ ] Static files ready
- [ ] Deploy to Netlify
- [ ] Test API integration
- [ ] Verify CORS working

---

## 🎯 Next Steps

1. **Monitor:** Watch Logs tab for any issues
2. **Test:** Try different queries via `/docs`
3. **Deploy Frontend:** Upload to Netlify
4. **Share:** Your live demo is ready!

---

**Live API:** https://prabhat9801-shl-recommendation-system.hf.space  
**API Docs:** https://prabhat9801-shl-recommendation-system.hf.space/docs  
**GitHub:** https://github.com/Prabhat9801/SHL_Recommendation_System

**System Status:** ✅ Production Ready | 🚀 Deployed | 📊 90.4% Accuracy
