# Complete System Architecture

**Document 5: System Overview, File Structure & Component Connections**

---

## 📁 **Complete Project Structure**

```
SHL_Submission/
├── modules/                          # Core modular components (7 files)
│   ├── __init__.py                  # Package exports
│   ├── data_loader.py              # Data ingestion
│   ├── preprocessor.py              # Data cleaning
│   ├── feature_extractor.py         # TF-IDF + Embeddings
│   ├── llm_client.py                # Groq LLM integration
│   ├── training_patterns.py         # Pattern learning
│   ├── recommender.py               # Main engine
│   ├── evaluator.py                 # Performance evaluation
│   ├── logger.py                    # Logging system
│   ├── exceptions.py                # Custom exceptions
│   └── storage_manager.py           # Vector & prediction storage
├── backend/                          # FastAPI application
│   ├── main.py                      # API endpoints
│   └── requirements.txt             # Backend dependencies
├── frontend/                         # Web interface
│   ├── index.html                   # Main page
│   ├── styles.css                   # Styling
│   └── app.js                       # Frontend logic
├── scraping/                         # Data collection scripts
│   ├── 01_basic_scraping.py        # Phase 1: Basic info
│   ├── 02_deep_scraping.py         # Phase 2: Full details
│   ├── 03_training_data_scraping.py # Phase 3: Training URLs
│   └── README.md                    # Scraping guide
├── data/                             # Datasets
│   ├── shl_individual_test_solutions.csv  # 377 assessments
│   └── Gen_AI Dataset (1).xlsx            # Train/test data
├── docs/                             # Documentation (7 guides)
│   ├── 01_STEP_BY_STEP_APPROACH.md
│   ├── 02_CHALLENGES_AND_SOLUTIONS.md
│   ├── 03_JOURNEY_10_TO_90_PERCENT.md
│   ├── 04_WHY_NO_VECTOR_DATABASES.md
│   ├── 05_SYSTEM_ARCHITECTURE.md    # This file
│   ├── 06_SETUP_GUIDE.md
│   └── 07_DEPLOYMENT_GUIDE.md
├── vector_storage/                   # Auto-created on first run
│   ├── tfidf_matrix.npz            # Sparse TF-IDF matrix
│   ├── semantic_embeddings.npy      # Dense embeddings
│   └── assessment_mapping.csv       # URL mapping
├── predicted_test_csv/               # Auto-created on first run
│   └── test_predictions.csv         # Submission file
├── logs/                             # Auto-created on first run
│   └── shl_recommender_YYYYMMDD.log # Daily logs
├── main.py                           # Main entry point
├── .env                              # Environment variables
├── .gitignore                        # Git ignore rules
└── README.md                         # Project overview

**Total:** 40+ files across 8 directories
```

---

## 🏗️ **Architecture Overview**

### **Three-Tier Architecture**

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│     (Frontend - HTML/CSS/JS)        │
└──────────────┬──────────────────────┘
               │ HTTP/JSON
               ↓
┌─────────────────────────────────────┐
│         Application Layer           │
│        (FastAPI Backend)            │
└──────────────┬──────────────────────┘
               │ Python Imports
               ↓
┌─────────────────────────────────────┐
│          Business Logic             │
│      (Modular Components)           │
└──────────────┬──────────────────────┘
               │ File I/O
               ↓
┌─────────────────────────────────────┐
│          Data Layer                 │
│     (CSV/Excel/NumPy files)         │
└─────────────────────────────────────┘
```

---

## 📦 **Module-by-Module Breakdown**

### **1. data_loader.py** (Data Ingestion Layer)

**Purpose:** Load all data from files

**Responsibilities:**
- Load scraped assessments CSV
- Load training/test Excel data
- Validate data integrity
- Handle file errors

**Key Classes:**
```python
class DataLoader:
    def load_scraped_assessments() -> pd.DataFrame
    def load_train_test_data() -> Dict[str, pd.DataFrame]
    def get_all_data() -> Dict[str, pd.DataFrame]
```

**Input:** File paths
**Output:** Pandas DataFrames
**Used by:** Recommender, Evaluator
**Dependencies:** pandas, openpyxl

---

### **2. preprocessor.py** (Data Cleaning Layer)

**Purpose:** Clean and normalize data

**Responsibilities:**
- URL normalization (remove `/solutions/`)
- Duplicate removal
- Data merging (train + assessments)
- Missing value handling

**Key Classes:**
```python
class DataPreprocessor:
    def normalize_url(url: str) -> str
    def clean_scraped_data(df: pd.DataFrame) -> pd.DataFrame
    def prepare_train_data(train_df: pd.DataFrame) -> pd.DataFrame
    def merge_train_with_assessments(...) -> pd.DataFrame
```

**Input:** Raw DataFrames
**Output:** Cleaned DataFrames
**Used by:** Recommender
**Dependencies:** pandas

---

### **3. feature_extractor.py** (Feature Engineering Layer)

**Purpose:** Build TF-IDF and semantic embeddings

**Responsibilities:**
- Build TF-IDF matrix (377 × 10K)
- Build semantic embeddings (377 × 384)
- Compute query scores
- Strategic field weighting

**Key Classes:**
```python
class FeatureExtractor:
    def build_tfidf_features(...) -> np.ndarray
    def build_semantic_embeddings(...) -> np.ndarray
    def get_query_tfidf_scores(query: str) -> np.ndarray
    def get_query_semantic_scores(query: str) -> np.ndarray
```

**Input:** Assessment text data
**Output:** Feature matrices
**Used by:** Recommender
**Dependencies:** scikit-learn, sentence-transformers

---

### **4. llm_client.py** (LLM Integration Layer)

**Purpose:** Query understanding with Groq Llama 3.3 70B

**Responsibilities:**
- Extract technical/soft skills
- Identify role type
- Extract keywords
- Handle API errors & retries

**Key Classes:**
```python
class LLMClient:
    def extract_requirements(query: str) -> Dict
    # Returns: {technical_skills, soft_skills, role_type, keywords}
```

**Input:** Natural language query
**Output:** Structured requirements JSON
**Used by:** Recommender
**Dependencies:** groq, python-dotenv

**Retry Logic:** 2 retries with exponential backoff

---

### **5. training_patterns.py** (Pattern Learning Layer)

**Purpose:** Learn from training data

**Responsibilities:**
- Build assessment frequency map
- Build keyword → assessment patterns
- Calculate training boosts

**Key Classes:**
```python
class TrainingPatternsLearner:
    def learn_patterns(train_df: pd.DataFrame) -> None
    def get_training_boost(url: str, query: str) -> float
```

**Input:** Training data (merged)
**Output:** Boost scores (0-1)
**Used by:** Recommender
**Dependencies:** None (pure Python)

---

### **6. recommender.py** (Core Recommendation Engine)

**Purpose:** Main recommendation logic

**Responsibilities:**
- Orchestrate all components
- Hybrid scoring (5 signals)
- Rank and return top-K

**Key Classes:**
```python
class RecommendationEngine:
    # Components
    data_loader: DataLoader
    preprocessor: DataPreprocessor
    feature_extractor: FeatureExtractor
    llm_client: LLMClient
    training_learner: TrainingPatternsLearner
    
    def initialize() -> None
    def recommend(query: str, top_k: int) -> List[Dict]
```

**Hybrid Scoring Formula:**
```python
final_score = (
    0.35 * tfidf_score +
    0.18 * semantic_score +
    0.20 * training_boost +
    0.12 * technical_boost +
    0.05 * soft_boost +
    0.10 * test_type_boost
)
```

**Input:** Query string
**Output:** List of recommendations
**Used by:** Backend API, Main script
**Dependencies:** All above modules

---

### **7. evaluator.py** (Evaluation Layer)

**Purpose:** Measure system performance

**Responsibilities:**
- Calculate Mean Recall@10
- Generate test predictions
- Performance reporting

**Key Classes:**
```python
class Evaluator:
    def __init__(recommender: RecommendationEngine)
    def evaluate_recall_at_k(k: int) -> float
```

**Input:** Recommender engine
**Output:** Performance metrics
**Used by:** Main script, Testing
**Dependencies:** numpy

---

### **8. logger.py** (Logging Infrastructure)

**Purpose:** Centralized logging

**Responsibilities:**
- Configure logging format
- File + console output
- Daily log rotation

**Key Functions:**
```python
def setup_logger(name: str, log_file: str, level) -> logging.Logger
```

**Output:** `logs/shl_recommender_YYYYMMDD.log`
**Used by:** All modules
**Dependencies:** logging

---

### **9. exceptions.py** (Error Handling)

**Purpose:** Custom exception hierarchy

**Classes:**
```python
class SHLRecommenderException(Exception)
class DataLoadException(SHLRecommenderException)
class DataPreprocessingException(SHLRecommenderException)
class FeatureExtractionException(SHLRecommenderException)
class LLMException(SHLRecommenderException)
class RecommendationException(SHLRecommenderException)
class EvaluationException(SHLRecommenderException)
```

**Used by:** All modules
**Dependencies:** None

---

### **10. storage_manager.py** (Persistence Layer)

**Purpose:** Save vectors and predictions

**Responsibilities:**
- Save TF-IDF matrix to disk
- Save semantic embeddings
- Save test predictions CSV
- Save assessment mapping

**Key Classes:**
```python
class StorageManager:
    def save_tfidf_matrix(matrix, filename)
    def save_semantic_embeddings(embeddings, filename)
    def save_test_predictions(predictions_df, filename)
    def save_assessment_mapping(df, filename)
```

**Output Directories:**
- `vector_storage/` - TF-IDF & embeddings
- `predicted_test_csv/` - Test predictions

**Used by:** Recommender
**Dependencies:** numpy, pandas, scipy

---

## 🔄 **Data Flow Diagram**

### **Complete Pipeline**

```
1. USER INPUT
   "I need Java developers who collaborate"
          ↓
2. FRONTEND (frontend/app.js)
   POST /recommend
          ↓
3. BACKEND API (backend/main.py)
   Receives JSON request
          ↓
4. RECOMMENDER ENGINE (modules/recommender.py)
   ├→ DataLoader → Load 377 assessments
   ├→ Preprocessor → Clean & normalize
   ├→ FeatureExtractor → Build features
   │                      ├→ TF-IDF (377×10K)
   │                      └→ Semantic (377×384)
   ├→ LLMClient → Extract requirements
   │              {"technical": ["Java"],
   │               "soft": ["collaborate"]}
   ├→ Compute scores
   │  ├→ TF-IDF scores (377 values)
   │  ├→ Semantic scores (377 values)
   │  └→ Training boosts (377 values)
   ├→ Hybrid fusion
   │  Score = 0.35*tfidf + 0.18*semantic + 0.20*training + ...
   ├→ Rank by score
   └→ Return top-10
          ↓
5. BACKEND RESPONSE
   JSON with 10 recommendations
          ↓
6. FRONTEND DISPLAY
   Show results to user
```

---

## 🔗 **Module Dependencies**

### **Dependency Graph**

```
main.py
  └─> RecommendationEngine
       ├─> DataLoader
       │    └─> pandas, exceptions, logger
       ├─> DataPreprocessor
       │    └─> pandas, exceptions, logger
       ├─> FeatureExtractor
       │    └─> sklearn, sentence-transformers, exceptions, logger
       ├─> LLMClient
       │    └─> groq, dotenv, exceptions, logger
       ├─> TrainingPatternsLearner
       │    └─> collections, logger
       └─> StorageManager
            └─> numpy, pandas, scipy, logger

Evaluator
  └─> RecommendationEngine (all above)
```

### **External Dependencies**

```
Core:
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- sentence-transformers >= 2.2.0

LLM:
- groq >= 0.4.0
- python-dotenv >= 1.0.0

Data:
- openpyxl >= 3.1.0

API:
- fastapi >= 0.104.0
- uvicorn[standard] >= 0.24.0
- pydantic >= 2.0.0
```

---

## 🎯 **Component Interaction Example**

### **Example: Processing One Query**

```python
# 1. Initialize system
engine = RecommendationEngine()
engine.initialize()
  # └→ DataLoader loads CSV/Excel
  # └→ Preprocessor cleans data
  # └→ FeatureExtractor builds matrices
  # └→ TrainingLearner analyzes patterns

# 2. User query
query = "Java developer who collaborates"

# 3. LLM extraction
llm_data = engine.llm_client.extract_requirements(query)
# Returns: {technical: ["Java"], soft: ["collaborate"]}

# 4. Feature scoring
tfidf_scores = engine.feature_extractor.get_query_tfidf_scores(query)
# 377 scores based on keyword match

semantic_scores = engine.feature_extractor.get_query_semantic_scores(query)
# 377 scores based on semantic similarity

# 5. Training boosts
for i, assessment in enumerate(assessments):
    training_boost = engine.training_learner.get_training_boost(
        assessment.url, query
    )
    # Boost popular assessments

# 6. Hybrid scoring
for i in range(377):
    scores[i] = (
        0.35 * tfidf_scores[i] +
        0.18 * semantic_scores[i] +
        0.20 * training_boost +
        ... # other boosts
    )

# 7. Rank and return
top_10_indices = np.argsort(scores)[-10:]
return [assessments[i] for i in top_10_indices]
```

---

## 📊 **Performance Characteristics**

### **Time Complexity**

| Operation | Complexity | Time (377 items) |
|-----------|------------|------------------|
| Initialize | O(n²) | 3-5 seconds |
| TF-IDF build | O(n*m) | 1-2 seconds |
| Semantic build | O(n*d) | 2-3 seconds |
| Query TF-IDF | O(m) | 0.01 seconds |
| Query Semantic | O(n*d) | 0.05 seconds |
| LLM call | O(1) | 1-2 seconds |
| Scoring | O(n) | 0.01 seconds |
| **Total per query** | | **2-3 seconds** |

n = 377 (assessments)
m = 10,000 (TF-IDF features)
d = 384 (embedding dimensions)

### **Space Complexity**

| Component | Size | Storage |
|-----------|------|---------|
| TF-IDF matrix | 377×10K sparse | 1.5 MB |
| Semantic embeddings | 377×384 dense | 579 KB |
| Assessment data | 377 rows | ~200 KB |
| **Total** | | **~2.3 MB** |

---

## 🎨 **Design Patterns Used**

### **1. Singleton Pattern**
```python
# Backend API - single recommender instance
recommender = None

def get_recommender():
    global recommender
    if recommender is None:
        recommender = RecommendationEngine()
        recommender.initialize()
    return recommender
```

### **2. Strategy Pattern**
```python
# Different scoring strategies combined
scores = (
    tfidf_strategy.score(query) +
    semantic_strategy.score(query) +
    training_strategy.score(query)
)
```

### **3. Dependency Injection**
```python
class RecommendationEngine:
    def __init__(self):
        self.data_loader = DataLoader()        # Injected
        self.preprocessor = DataPreprocessor()  # Injected
        # Easy to mock for testing
```

### **4. Factory Pattern**
```python
def setup_logger(name, log_file, level):
    # Creates configured logger
    logger = logging.getLogger(name)
    # ... configuration ...
    return logger
```

---

## 🔐 **Security & Configuration**

### **Environment Variables (.env)**
```bash
GROQ_API_KEY=your_key_here
```

### **Configuration Management**
- API keys in `.env` (not committed)
- `.gitignore` excludes sensitive files
- Pydantic for input validation
- CORS configured for frontend

---

## ✅ **Quality Assurance**

### **Logging**
- Every module logs operations
- File + console output
- Daily log rotation
- Error tracking

### **Exception Handling**
- Custom exceptions for each layer
- Try-except blocks throughout
- Graceful degradation (LLM fails → continue)
- Retry logic (LLM: 2 retries)

### **Input Validation**
- Pydantic models in API
- Data type checks
- Empty data handling
- URL validation

---

## 🚀 **Scalability Considerations**

### **Current Scale (377 items)**
- ✅ In-memory works perfectly
- ✅ Fast queries (2-3s)
- ✅ Low resource usage (2.3 MB)

### **If scaled to 10K+ items**
- Consider: Redis caching
- Consider: Vector database
- Consider: Async processing
- Consider: Load balancing

---

**This architecture achieves 90.4% Mean Recall@10 with clean, modular, maintainable code!** 🎯
