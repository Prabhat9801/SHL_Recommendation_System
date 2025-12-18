"""
Recommender Module
Main recommendation engine with hybrid scoring
"""
import pandas as pd
import numpy as np
from typing import List, Dict
from modules.data_loader import DataLoader
from modules.preprocessor import DataPreprocessor
from modules.feature_extractor import FeatureExtractor
from modules.llm_client import LLMClient
from modules.training_patterns import TrainingPatternsLearner

class RecommendationEngine:
    """
    Main recommendation engine
    Combines all components for hybrid scoring
    """
    
    # Scoring weights
    WEIGHT_TFIDF = 0.35
    WEIGHT_SEMANTIC = 0.18
    WEIGHT_TRAINING = 0.20
    WEIGHT_TECHNICAL = 0.12
    WEIGHT_OTHER = 0.15
    
    def __init__(self, data_dir: str = 'data'):
        self.data_loader = DataLoader(data_dir=data_dir)
        self.preprocessor = DataPreprocessor()
        self.feature_extractor = FeatureExtractor()
        self.llm_client = LLMClient()
        self.training_learner = TrainingPatternsLearner()
        
        self.df_assessments = None
        self.initialized = False
    
    def initialize(self) -> None:
        """Initialize the recommendation system"""
        if self.initialized:
            return
        
        print("="*80)
        print("INITIALIZING RECOMMENDATION SYSTEM")
        print("="*80)
        
        # 1. Load data
        data = self.data_loader.get_all_data()
        
        # 2. Preprocess
        self.df_assessments = self.preprocessor.clean_scraped_data(data['scraped'])
        train_clean = self.preprocessor.prepare_train_data(data['train'])
        
        # 3. Build features
        self.feature_extractor.build_tfidf_features(self.df_assessments)
        self.feature_extractor.build_semantic_embeddings(self.df_assessments)
        
        # 4. Learn training patterns
        train_merged = self.preprocessor.merge_train_with_assessments(
            train_clean, 
            self.df_assessments
        )
        self.training_learner.learn_patterns(train_merged)
        
        self.initialized = True
        print("\n✅ Recommendation system ready!\n")
    
    def recommend(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Generate recommendations for a query
        
        Args:
            query: Job description or requirements
            top_k: Number of recommendations to return
        
        Returns:
            List of recommended assessments with scores
        """
        if not self.initialized:
            self.initialize()
        
        query_lower = query.lower()
        
        # 1. Extract requirements with LLM
        llm_data = self.llm_client.extract_requirements(query)
        
        # 2. Enhanced query
        keywords = llm_data.get('keywords', [])
        enhanced_query = f"{query} {' '.join(keywords)}"
        
        # 3. Get retrieval scores
        tfidf_scores = self.feature_extractor.get_query_tfidf_scores(enhanced_query)
        semantic_scores = self.feature_extractor.get_query_semantic_scores(enhanced_query)
        
        # 4. Calculate combined scores for each assessment
        recommendations = []
        
        for idx, row in self.df_assessments.iterrows():
            url = row['normalized_url']
            name_lower = str(row['name']).lower()
            desc_lower = str(row['description']).lower()
            test_type = str(row.get('test_type', '')).lower()
            
            # Base retrieval scores
            tfidf_score = tfidf_scores[idx]
            semantic_score = semantic_scores[idx]
            
            # Training pattern boost
            training_boost = self.training_learner.get_training_boost(url, query_lower)
            
            # Technical skills boost
            tech_boost = self._calculate_tech_boost(llm_data, name_lower, desc_lower)
            
            # Other boosts (soft skills, test type)
            soft_boost = self._calculate_soft_boost(llm_data, name_lower, desc_lower)
            type_boost = self._calculate_type_boost(query_lower, test_type)
            
            # Hybrid scoring
            final_score = (
                self.WEIGHT_TFIDF * tfidf_score +
                self.WEIGHT_SEMANTIC * semantic_score +
                self.WEIGHT_TRAINING * training_boost +
                self.WEIGHT_TECHNICAL * tech_boost +
                0.05 * soft_boost +
                0.10 * type_boost
            )
            
            recommendations.append({
                'assessment_name': str(row['name']),
                'assessment_url': str(row['url']),
                'description': str(row['description'])[:500],
                'duration': int(row.get('duration', 20)),
                'test_type': self._parse_test_types(row.get('test_type')),
                'adaptive_support': str(row.get('adaptive_support', 'No')),
                'remote_support': str(row.get('remote_support', 'Yes')),
                'relevance_score': float(final_score)
            })
        
        # Sort and return top-k
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        return recommendations[:top_k]
    
    def _calculate_tech_boost(self, llm_data: Dict, name: str, desc: str) -> float:
        """Calculate technical skills boost"""
        boost = 0.0
        for skill in llm_data.get('technical_skills', []):
            if skill.lower() in name:
                boost += 0.5
            elif skill.lower() in desc:
                boost += 0.2
        return min(boost, 1.0)
    
    def _calculate_soft_boost(self, llm_data: Dict, name: str, desc: str) -> float:
        """Calculate soft skills boost"""
        boost = 0.0
        for skill in llm_data.get('soft_skills', []):
            if skill.lower() in name or skill.lower() in desc:
                boost += 0.25
        return min(boost, 1.0)
    
    def _calculate_type_boost(self, query: str, test_type: str) -> float:
        """Calculate test type matching boost"""
        boost = 0.0
        
        if any(word in query for word in ['programming', 'coding', 'developer']):
            if 'knowledge & skills' in test_type:
                boost += 0.3
        
        if any(word in query for word in ['personality', 'culture', 'behavior']):
            if 'personality & behavior' in test_type:
                boost += 0.3
        
        return boost
    
    @staticmethod
    def _parse_test_types(test_type_str) -> List[str]:
        """Parse test type string into list"""
        if pd.isna(test_type_str):
            return []
        return [t.strip() for t in str(test_type_str).split('|') if t.strip()]
