---
title: SHL Recommendation System API
emoji: 🎯
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# SHL Assessment Recommendation System

## 🎯 Overview

AI-powered recommendation system that suggests the most relevant SHL assessments based on job requirements. Achieves **90.4% Mean Recall@10** using a hybrid RAG architecture.

## 🚀 Features

- **90.4% Accuracy** - Exceptional recommendation quality
- **Hybrid Scoring** - Combines TF-IDF, semantic embeddings, and LLM
- **Fast Responses** - Pre-loaded models for instant recommendations
- **377 Assessments** - Complete SHL catalog
- **LLM Integration** - Groq Llama 3.3 70B for skill extraction

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Get Recommendations
```bash
POST /recommend
{
  "query": "Python Developer with SQL skills",
  "top_k": 10
}
```

### API Documentation
- Interactive Docs: `/docs`
- OpenAPI Schema: `/openapi.json`

## 🔑 Environment Variables

Required:
- `GROQ_API_KEY` - Your Groq API key for LLM integration

## 💡 Usage Example

```python
import requests

response = requests.post(
    "https://your-space.hf.space/recommend",
    json={
        "query": "Java developer who can collaborate with business teams",
        "top_k": 5
    }
)

recommendations = response.json()["recommendations"]
for rec in recommendations:
    print(f"{rec['assessment_name']}: {rec['relevance_score']:.2%}")
```

## 🏗️ Architecture

- **TF-IDF**: Keyword matching (35% weight)
- **Semantic Embeddings**: Meaning-based matching (18% weight)  
- **Training Patterns**: Learning from expert choices (20% weight)
- **LLM Extraction**: Skill identification (27% weight combined)

## 📊 Performance

- Mean Recall@10: 90.4%
- Response Time: 2-3 seconds
- Memory Usage: ~600MB (well within 16GB limit)

## 🔗 Links

- [GitHub Repository](https://github.com/Prabhat9801/SHL_Recommendation_System)
- [Documentation](https://github.com/Prabhat9801/SHL_Recommendation_System#readme)

## 👨‍💻 Author

**Prabhat Kumar Singh**
- Email: prabhatkumarsictc12@gmail.com
- GitHub: [@Prabhat9801](https://github.com/Prabhat9801)

---

**Built for SHL AI Intern Assessment** | **90.4% Accuracy** | **Production Ready**
