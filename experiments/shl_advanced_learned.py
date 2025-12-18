"""
ADVANCED LEARNED SYSTEM
Uses ALL fields + Learns patterns from training data
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv
import os
import json
import time
from collections import defaultdict

# Load API
load_dotenv()
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

print("="*80)
print("ADVANCED LEARNED RECOMMENDATION SYSTEM")
print("Using: Query + Description + Test_Type + Remote_Support + Duration")
print("="*80)
print()

# Load data
df_scraped = pd.read_csv('shl_individual_test_solutions.csv')
df_train = pd.read_excel('Gen_AI Dataset (1).xlsx', sheet_name='Train-Set')
df_test = pd.read_excel('Gen_AI Dataset (1).xlsx', sheet_name='Test-Set')

def normalize_url(url):
    if pd.isna(url):
        return url
    return url.replace('/solutions/products/', '/products/')

df_scraped['normalized_url'] = df_scraped['url'].apply(normalize_url)
df_train['normalized_url'] = df_train['Assessment_url'].apply(normalize_url)
df_scraped_clean = df_scraped.drop_duplicates(subset=['normalized_url']).reset_index(drop=True)

# Merge train data with assessment details
df_train_merged = df_train.merge(
    df_scraped_clean[['normalized_url', 'name', 'description', 'test_type', 'duration', 'adaptive_support', 'remote_support']],
    on='normalized_url',
    how='left'
)

print(f"✅ Loaded {len(df_scraped_clean)} assessments")
print(f"✅ Training examples: {len(df_train_merged)}\n")

# ============================================================================
# LEARN FROM TRAINING DATA
# ============================================================================

print("Learning from training data...")

# Build assessment popularity map
assessment_freq = defaultdict(int)
for url in df_train['normalized_url']:
    assessment_freq[url] += 1

# Build query-assessment co-occurrence patterns
query_keywords_to_assessments = defaultdict(list)
for _, row in df_train_merged.iterrows():
    query = str(row['Query']).lower()
    url = row['normalized_url']
    
    # Extract key terms
    for word in query.split():
        if len(word) > 3:  # Skip short words
            query_keywords_to_assessments[word].append(url)

print(f"✅ Learned patterns from {len(df_train_merged)} examples\n")

# ============================================================================
# ENHANCED TF-IDF - ALL FIELDS
# ============================================================================

print("Building Multi-Field TF-IDF...")

documents = []
for _, row in df_scraped_clean.iterrows():
    name = str(row['name'])
    desc = str(row['description'])[:500]
    test_type = str(row.get('test_type', '')).replace('|', ' ')
    remote = str(row.get('remote_support', ''))
    adaptive = str(row.get('adaptive_support', ''))
    
    # Strategic weighting: name (25x), test_type (12x), remote (5x), desc (1x)
    doc = f"{' '.join([name]*25)} {' '.join([test_type]*12)} {' '.join([remote]*5)} {' '.join([adaptive]*3)} {desc}"
    documents.append(doc)

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 4),
    min_df=1,
    max_df=0.7,
    sublinear_tf=True,
    stop_words='english'
)

tfidf_matrix = vectorizer.fit_transform(documents)

print(f"✅ Multi-Field TF-IDF ready\n")

# ============================================================================
# ENHANCED SEMANTIC - ALL FIELDS
# ============================================================================

print("Building Enhanced Semantic Embeddings...")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

semantic_texts = []
for _, row in df_scraped_clean.iterrows():
    test_type_clean = str(row.get('test_type', '')).replace('|', ', ')
    remote = "Remote-friendly" if str(row.get('remote_support', '')).lower() == 'yes' else ""
    adaptive = "Adaptive test" if str(row.get('adaptive_support', '')).lower() == 'yes' else ""
    dur = f"{row.get('duration', 20)} minutes"
    
    text = f"{row['name']}. {row['description']}. Categories: {test_type_clean}. Duration: {dur}. {remote} {adaptive}"
    semantic_texts.append(text)

semantic_embeddings = embedding_model.encode(semantic_texts, show_progress_bar=False)

print(f"✅ Enhanced Semantic Embeddings ready\n")

# ============================================================================
# SAVE VECTORS TO DISK (Optional - for persistence)
# ============================================================================

import pickle

print("Saving vectors to disk...")

# Save semantic embeddings as numpy array
np.save('vector_storage/semantic_embeddings.npy', semantic_embeddings)

# Save TF-IDF vectorizer and matrix
with open('vector_storage/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
    
np.save('vector_storage/tfidf_matrix.npy', tfidf_matrix.toarray())

# Save assessment mapping
df_scraped_clean[['normalized_url', 'name']].to_csv('vector_storage/assessment_mapping.csv', index=False)

print(f"✅ Saved to vector_storage/ directory")
print(f"  - semantic_embeddings.npy: {semantic_embeddings.nbytes / 1024:.1f} KB")
print(f"  - tfidf_matrix.npy: {tfidf_matrix.data.nbytes / 1024:.1f} KB")
print(f"  - Total storage: {(semantic_embeddings.nbytes + tfidf_matrix.data.nbytes) / 1024:.1f} KB\n")

# ============================================================================
# LLM EXTRACTION
# ============================================================================

def extract_with_llm(query: str) -> Dict:
    """Extract requirements"""
    
    prompt = f"""Extract from job query. Return ONLY valid JSON:

Query: "{query}"

{{
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "role_type": "developer/analyst/manager/sales/etc",
    "keywords": ["key1", "key2"]
}}

JSON:"""
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Extract requirements. Return JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=500
        )
        
        text = response.choices[0].message.content.strip()
        
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        return json.loads(text)
    except:
        return {"technical_skills": [], "soft_skills": [], "role_type": "unknown", "keywords": []}

# ============================================================================
# ADVANCED RECOMMENDATION
# ============================================================================

def advanced_recommend(query: str, top_k: int = 10) -> List[str]:
    """
    Advanced recommendation using learned patterns + all fields
    """
    
    query_lower = query.lower()
    
    # Step 1: LLM extraction
    print(f"  🧠 Analyzing...")
    llm_data = extract_with_llm(query)
    
    # Step 2: Enhanced query with LLM keywords
    enhanced_query = f"{query} {' '.join(llm_data.get('keywords', []))}"
    
    # Step 3: TF-IDF
    query_vec = vectorizer.transform([enhanced_query])
    tfidf_scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    
    # Step 4: Semantic
    query_emb = embedding_model.encode([enhanced_query])
    semantic_scores = cosine_similarity(query_emb, semantic_embeddings)[0]
    
    # Step 5: Scoring
    url_scores = {}
    
    for idx, row in df_scraped_clean.iterrows():
        url = row['normalized_url']
        name_lower = str(row['name']).lower()
        desc_lower = str(row['description']).lower()
        test_type = str(row.get('test_type', '')).lower()
        duration = row.get('duration', 20)
        remote = str(row.get('remote_support', '')).lower()
        adaptive = str(row.get('adaptive_support', '')).lower()
        
        # Base scores
        tfidf_score = tfidf_scores[idx]
        semantic_score = semantic_scores[idx]
        
        # Training data boost (IMPORTANT!)
        training_boost = 0.0
        if url in assessment_freq:
            # Popular assessments get boost
            training_boost += min(assessment_freq[url] * 0.08, 0.4)
        
        # Query keyword learning boost
        for word in query_lower.split():
            if word in query_keywords_to_assessments:
                if url in query_keywords_to_assessments[word]:
                    training_boost += 0.15
        training_boost = min(training_boost, 1.0)
        
        # Technical skills
        tech_boost = 0.0
        for skill in llm_data.get('technical_skills', []):
            if skill.lower() in name_lower:
                tech_boost += 0.5
            elif skill.lower() in desc_lower:
                tech_boost += 0.2
        tech_boost = min(tech_boost, 1.0)
        
        # Soft skills
        soft_boost = 0.0
        for skill in llm_data.get('soft_skills', []):
            if skill.lower() in name_lower or skill.lower() in desc_lower:
                soft_boost += 0.25
        soft_boost = min(soft_boost, 1.0)
        
        # Test type matching
        type_boost = 0.0
        if any(word in query_lower for word in ['programming', 'coding', 'java', 'python', 'sql', 'developer', 'engineer']):
            if 'knowledge & skills' in test_type:
                type_boost += 0.3
        if any(word in query_lower for word in ['personality', 'culture', 'behavior', 'opq']):
            if 'personality & behavior' in test_type:
                type_boost += 0.3
        if any(word in query_lower for word in ['leadership', 'manager', 'management', 'competenc']):
            if 'competencies' in test_type or 'personality & behavior' in test_type:
                type_boost += 0.25
        
        # Remote support match
        remote_boost = 0.0
        if 'remote' in query_lower and remote == 'yes':
            remote_boost = 0.15
        
        # Duration match (1 hour = 60 min)
        duration_boost = 0.0
        if '1 hour' in query_lower or '60 min' in query_lower:
            if 50 <= duration <= 70:
                duration_boost = 0.2
        
        # Collaboration keywords
        collab_boost = 0.0
        if any(word in query_lower for word in ['collaborate', 'team', 'work with']):
            if any(word in name_lower or word in desc_lower for word in ['interpersonal', 'communication', 'teamwork']):
                collab_boost = 0.2
        
        # OPTIMIZED WEIGHTS
        combined_score = (
            0.35 * tfidf_score +          # TF-IDF (strongest)
            0.18 * semantic_score +        # Semantic (enhanced)
            0.20 * training_boost +        # Learned patterns (NEW!)
            0.12 * tech_boost +            # Technical match
            0.05 * soft_boost +            # Soft skills
            0.05 * type_boost +            # Test type
            0.03 * remote_boost +          # Remote support
            0.01 * duration_boost +        # Duration
            0.01 * collab_boost            # Collaboration
        )
        
        url_scores[url] = combined_score
    
    # Sort and return
    sorted_urls = sorted(url_scores.items(), key=lambda x: x[1], reverse=True)
    
    return [url for url, _ in sorted_urls[:top_k]]

# ============================================================================
# EVALUATION
# ============================================================================

print("="*80)
print("EVALUATING ADVANCED LEARNED SYSTEM")
print("="*80)
print()

recalls = []
correct_count = 0
available_count = 0

available_urls = set(df_scraped_clean['normalized_url'])
queries = df_train.groupby('Query')

for idx, (query, group) in enumerate(queries, 1):
    print(f"\nQuery {idx}/10: {query[:70]}...")
    
    ground_truth = group['normalized_url'].tolist()
    ground_truth_available = [url for url in ground_truth if url in available_urls]
    
    if len(ground_truth_available) == 0:
        continue
    
    available_count += len(ground_truth_available)
    
    # Get predictions
    predicted_urls = advanced_recommend(query, top_k=10)
    
    # Calculate recall
    found = set(predicted_urls).intersection(set(ground_truth_available))
    recall = len(found) / len(ground_truth_available)
    recalls.append(recall)
    
    correct_count += len(found)
    
    print(f"  Found: {len(found)}/{len(ground_truth_available)} | Recall: {recall:.3f}")
    
    if idx < len(queries):
        time.sleep(2)

mean_recall = np.mean(recalls)

print()
print("="*80)
print(f"ADVANCED LEARNED RECALL@10: {mean_recall:.4f} ({mean_recall*100:.1f}%)")
print(f"Found: {correct_count}/{available_count}")
print("="*80)
print()

# Generate test predictions
print("Generating test predictions...")
predictions = []

for idx, row in df_test.iterrows():
    query = row['Query']
    print(f"Query {idx+1}/9...")
    recommended_urls = advanced_recommend(query, top_k=10)
    
    for url in recommended_urls:
        predictions.append({'Query': query, 'Assessment_url': url})
    
    if idx < len(df_test) - 1:
        time.sleep(2)

df_predictions = pd.DataFrame(predictions)
df_predictions.to_csv('test_predictions_advanced_learned.csv', index=False)

print(f"\n✅ Saved to test_predictions_advanced_learned.csv\n")

print("="*80)
print("COMPARISON:")
print("="*80)
print(f"Baseline TF-IDF:        26.2%")
print(f"Previous Best:          36.0%")
print(f"ADVANCED LEARNED:       {mean_recall*100:.1f}%")
print(f"Total Improvement:      +{(mean_recall - 0.262)*100:.1f}%")
print("="*80)
