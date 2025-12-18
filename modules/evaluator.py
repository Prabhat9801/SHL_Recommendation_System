"""
Evaluator Module
Handles performance evaluation
"""
import numpy as np
import pandas as pd
from typing import Dict
from modules.recommender import RecommendationEngine

class Evaluator:
    """
    Responsible for evaluating recommendation performance
    """
    
    def __init__(self, recommender: RecommendationEngine):
        self.recommender = recommender
    
    def evaluate_recall_at_k(self, k: int = 10) -> float:
        """
        Evaluate Mean Recall@K on training data
        
        Returns:
            Mean recall across all queries
        """
        if not self.recommender.initialized:
            self.recommender.initialize()
        
        print(f"\nEvaluating Recall@{k}...")
        
        train_data = self.recommender.data_loader.train_data
        train_clean = self.recommender.preprocessor.prepare_train_data(train_data)
        
        recalls = []
        available_urls = set(self.recommender.df_assessments['normalized_url'])
        
        for query, group in train_clean.groupby('Query'):
            ground_truth = group['normalized_url'].tolist()
            ground_truth_available = [url for url in ground_truth if url in available_urls]
            
            if len(ground_truth_available) == 0:
                continue
            
            # Get predictions
            predicted = self.recommender.recommend(query, top_k=k)
            predicted_urls = [
                r['assessment_url'].replace('/solutions/products/', '/products/')
                for r in predicted
            ]
            
            # Calculate recall
            found = set(predicted_urls).intersection(set(ground_truth_available))
            recall = len(found) / len(ground_truth_available)
            recalls.append(recall)
            
            print(f"  Query: {query[:50]}... | Recall: {recall:.3f}")
        
        mean_recall = np.mean(recalls)
        print(f"\n✅ Mean Recall@{k}: {mean_recall:.4f} ({mean_recall*100:.1f}%)\n")
        
        return mean_recall
