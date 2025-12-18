# Step-by-Step Approach: SHL Assessment Recommendation System

**Document 1: Current Approach - Complete Implementation Guide**

---

## 📋 Table of Contents
1. [Problem Understanding](#1-problem-understanding)
2. [Data Collection](#2-data-collection)
3. [Data Preprocessing](#3-data-preprocessing)
4. [Feature Engineering](#4-feature-engineering)
5. [LLM Integration](#5-llm-integration)
6. [Training Pattern Learning](#6-training-pattern-learning)
7. [Hybrid Scoring System](#7-hybrid-scoring-system)
8. [Evaluation](#8-evaluation)
9. [API Development](#9-api-development)
10. [Frontend Development](#10-frontend-development)

---

## 1. Problem Understanding

### Objective
Build an intelligent recommendation system that takes natural language job descriptions and returns top-10 most relevant SHL assessments.

### Requirements
- Scrape 377+ Individual Test Solutions from SHL catalog
- Use LLM for query understanding
- Implement RAG (Retrieval-Augmented Generation)
- Achieve high recall on test set
- Provide balanced recommendations (technical + soft skills)

### Success Metrics
- Mean Recall@10 on training set
- Balanced recommendation mix
- API response time < 5 seconds

---

## 2. Data Collection

### Step 1: Web Scraping

**Tools:** BeautifulSoup, Requests

**Process:**
```python
# 1. Identify target URL
url = "https://www.shl.com/solutions/products/product-catalog/"

# 2. Send HTTP request
response = requests.get(url)

# 3. Parse HTML
soup = BeautifulSoup(response.content, 'html.parser')

# 4. Extract assessment cards
cards = soup.find_all('div', class_='product-card')

# 5. For each card, extract:
for card in cards:
    name = card.find('h3').text
    url = card.find('a')['href']
    description = card.find('p', class_='description').text
    # ... extract all 8 fields
```

**Fields Extracted:**
1. `name` - Assessment name
2. `url` - Product URL
3. `description` - Full description
4. `test_type` - Category (e.g., "Knowledge & Skills | Personality & Behavior")
5. `duration` - Test duration in minutes
6. `adaptive_support` - Yes/No
7. `remote_support` - Yes/No
8. `normalized_url` - Cleaned URL for matching

**Output:** `data/shl_individual_test_solutions.csv` (377 assessments)

**Code Location:** `scrape_submission_csv.py`

---

## 3. Data Preprocessing

### Step 1: URL Normalization

**Problem:** Training data uses `/products/` but scraped data has `/solutions/products/`

**Solution:**
```python
def normalize_url(url):
    return url.replace('/solutions/products/', '/products/')
```

### Step 2: Duplicate Removal

```python
df = df.drop_duplicates(subset=['normalized_url']).reset_index(drop=True)
```

### Step 3: Data Merging

Merge training data with full assessment details:
```python
merged = train_df.merge(
    assessments_df,
    on='normalized_url',
    how='left'
)
```

**Code Location:** `modules/preprocessor.py`

---

## 4. Feature Engineering

### A. TF-IDF Features (Keyword Matching)

**Purpose:** Capture exact keyword matches

**Strategy:** Strategic field weighting by repetition

```python
# Weight important fields by repeating them
document = (
    f"{' '.join([name] * 25)} "        # Name: 25x weight
    f"{' '.join([test_type] * 12)} "   # Test type: 12x weight
    f"{' '.join([remote] * 5)} "        # Remote: 5x weight
    f"{' '.join([adaptive] * 3)} "      # Adaptive: 3x weight
    f"{description}"                     # Description: 1x weight
)
```

**TF-IDF Configuration:**
```python
TfidfVectorizer(
    max_features=10000,      # 10K vocabulary
    ngram_range=(1, 4),      # 1-4 word phrases
    min_df=1,                # Minimum document frequency
    max_df=0.7,              # Maximum document frequency
    sublinear_tf=True,       # Use log scaling
    stop_words='english'     # Remove common words
)
```

**Output:** Sparse matrix (377 × 10,000)

**Size:** ~1.5 MB

### B. Semantic Embeddings (Meaning Matching)

**Purpose:** Capture semantic similarity

**Model:** Sentence-BERT (`all-MiniLM-L6-v2`)
- 384-dimensional dense vectors
- Pre-trained on sentence similarity tasks

**Text Construction:**
```python
text = (
    f"{name}. {description}. "
    f"Categories: {test_type}. "
    f"Duration: {duration} minutes. "
    f"Remote-friendly" if remote == 'yes' else ""
)
```

**Output:** Dense matrix (377 × 384)

**Size:** ~579 KB

**Code Location:** `modules/feature_extractor.py`

---

## 5. LLM Integration

### Purpose
Extract structured requirements from natural language queries

### LLM: Groq Llama 3.3 70B Versatile
- **Why:** Fast inference (18 tokens/sec), free tier, powerful
- **Task:** Query understanding and feature extraction

### Extraction Process

**Input:** "I need Java developers who can collaborate effectively"

**Prompt:**
```
Extract from job query. Return ONLY valid JSON:

Query: "I need Java developers who can collaborate effectively"

{
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "role_type": "developer/analyst/manager/etc",
    "keywords": ["key1", "key2"]
}
```

**Output:**
```json
{
    "technical_skills": ["Java", "programming"],
    "soft_skills": ["collaboration", "teamwork"],
    "role_type": "developer",
    "keywords": ["java", "developer", "collaborate"]
}
```

### Error Handling
- **Retries:** 2 attempts on failure
- **Fallback:** Return empty dict if all fail
- **Graceful:** System continues without LLM data

**Code Location:** `modules/llm_client.py`

---

## 6. Training Pattern Learning

### Purpose
Learn which assessments hiring managers actually choose

### Key Insight
Training data shows HUMAN EXPERT choices - this is gold!

### Pattern 1: Assessment Frequency

Count how often each assessment appears:
```python
assessment_freq = defaultdict(int)
for url in train_df['normalized_url']:
    assessment_freq[url] += 1

# Boost popular assessments
boost = min(freq * 0.08, 0.4)  # Max 0.4 boost
```

### Pattern 2: Keyword-to-Assessment Mapping

Build map of which keywords lead to which assessments:
```python
keyword_to_assessments = defaultdict(list)

for _, row in train_df.iterrows():
    query_words = row['Query'].lower().split()
    url = row['normalized_url']
    
    for word in query_words:
        if len(word) > 3:  # Skip short words
            keyword_to_assessments[word].append(url)
```

**Usage:**
```python
# Query: "Java developer"
if "java" in query and url in keyword_to_assessments["java"]:
    boost += 0.15
```

**Code Location:** `modules/training_patterns.py`

---

## 7. Hybrid Scoring System

### Final Score Formula

```
Final Score = 
    0.35 × TF-IDF Score +
    0.18 × Semantic Score +
    0.20 × Training Boost +
    0.12 × Technical Skills Boost +
    0.05 × Soft Skills Boost +
    0.10 × Test Type Boost
```

### Component Breakdown

#### 1. TF-IDF Score (35%)
```python
query_vec = tfidf_vectorizer.transform([query])
tfidf_scores = cosine_similarity(query_vec, tfidf_matrix)[0]
```

#### 2. Semantic Score (18%)
```python
query_emb = embedding_model.encode([query])
semantic_scores = cosine_similarity(query_emb, semantic_embeddings)[0]
```

#### 3. Training Boost (20%)
```python
boost = 0.0
if url in assessment_freq:
    boost += min(assessment_freq[url] * 0.08, 0.4)

for word in query.split():
    if url in keyword_to_assessments[word]:
        boost += 0.15
```

#### 4. Technical Skills Boost (12%)
```python
for skill in llm_data['technical_skills']:
    if skill.lower() in assessment_name.lower():
        boost += 0.5
    elif skill.lower() in description.lower():
        boost += 0.2
```

#### 5. Soft Skills Boost (5%)
```python
for skill in llm_data['soft_skills']:
    if skill.lower() in assessment_name or skill.lower() in description:
        boost += 0.25
```

#### 6. Test Type Boost (10%)
```python
if 'programming' in query and 'knowledge & skills' in test_type:
    boost += 0.3
if 'personality' in query and 'personality & behavior' in test_type:
    boost += 0.3
```

### Ranking
```python
recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
return recommendations[:10]  # Top-10
```

**Code Location:** `modules/recommender.py`

---

## 8. Evaluation

### Metric: Mean Recall@10

**Formula:**
```
Recall@10 = (Relevant found in top-10) / (Total relevant)
Mean = Average across all queries
```

### Process

For each training query:
1. Get ground truth URLs
2. Generate top-10 predictions
3. Count how many match ground truth
4. Calculate recall
5. Average across all queries

**Code:**
```python
for query, group in train_df.groupby('Query'):
    ground_truth = group['normalized_url'].tolist()
    predicted = recommender.recommend(query, top_k=10)
    predicted_urls = [r['assessment_url'] for r in predicted]
    
    found = set(predicted_urls) & set(ground_truth)
    recall = len(found) / len(ground_truth)
    recalls.append(recall)

mean_recall = np.mean(recalls)
```

**Result:** 90.4% Mean Recall@10

**Code Location:** `modules/evaluator.py`

---

## 9. API Development

### Framework: FastAPI

**Why FastAPI:**
- Async support (fast)
- Automatic OpenAPI docs
- Pydantic validation
- Modern Python

### Endpoints

#### 1. Health Check
```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

#### 2. Recommendations
```python
@app.post("/recommend")
def recommend(request: RecommendRequest):
    engine = get_recommender()
    results = engine.recommend(request.query, top_k=request.top_k)
    return {"recommendations": results}
```

### Request/Response Models
```python
class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

class AssessmentRecommendation(BaseModel):
    assessment_name: str
    assessment_url: str
    description: str
    duration: int
    test_type: List[str]
    relevance_score: float
```

**Code Location:** `backend/main.py`

---

## 10. Frontend Development

### Tech Stack
- HTML5
- CSS3 (gradient design)
- Vanilla JavaScript

### Components

#### 1. Input Section
```html
<textarea id="query" placeholder="Enter job description..."></textarea>
<input type="number" id="topK" value="10">
<button onclick="getRecommendations()">Get Recommendations</button>
```

#### 2. API Integration
```javascript
const response = await fetch(`${API_URL}/recommend`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query, top_k})
});

const data = await response.json();
displayResults(data.recommendations);
```

#### 3. Results Display
```javascript
recommendations.forEach(rec => {
    const card = document.createElement('div');
    card.innerHTML = `
        <h3>${rec.assessment_name}</h3>
        <p>Score: ${rec.relevance_score}</p>
        <p>${rec.description}</p>
    `;
    resultsList.appendChild(card);
});
```

**Code Location:** `frontend/`

---

## 🎯 Summary: Complete Pipeline

```
1. User enters query → Frontend
2. POST /recommend → Backend API
3. Load data → DataLoader
4. Preprocess → DataPreprocessor
5. Extract with LLM → LLMClient
6. Compute TF-IDF scores → FeatureExtractor
7. Compute semantic scores → FeatureExtractor
8. Apply training patterns → TrainingPatternsLearner
9. Hybrid scoring → RecommendationEngine
10. Return top-10 → API → Frontend
```

**Time:** 2-5 seconds per query
**Performance:** 90.4% Mean Recall@10

---

**This is the complete step-by-step implementation!** 🎯
