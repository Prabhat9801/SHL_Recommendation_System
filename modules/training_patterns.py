"""
Training Patterns Module
Learns patterns from training data
"""
import pandas as pd
from collections import defaultdict
from typing import Dict, List

class TrainingPatternsLearner:
    """
    Responsible for learning patterns from training data
    - Which assessments are popular
    - Which keywords map to which assessments
    """
    
    def __init__(self):
        self.assessment_freq = defaultdict(int)
        self.keyword_to_assessments = defaultdict(list)
    
    def learn_patterns(self, train_df_merged: pd.DataFrame) -> None:
        """
        Learn patterns from merged training data
        
        Args:
            train_df_merged: Training data merged with assessment details
        """
        print("Learning patterns from training data...")
        
        # Build assessment frequency map
        for url in train_df_merged['normalized_url']:
            self.assessment_freq[url] += 1
        
        # Build query-keyword to assessment patterns
        for _, row in train_df_merged.iterrows():
            query = str(row['Query']).lower()
            url = row['normalized_url']
            
            # Extract keywords (simple: words > 3 chars)
            for word in query.split():
                if len(word) > 3:
                    self.keyword_to_assessments[word].append(url)
        
        print(f"✅ Learned {len(self.assessment_freq)} popular assessments")
        print(f"✅ Learned {len(self.keyword_to_assessments)} keyword patterns")
    
    def get_training_boost(self, url: str, query_lower: str) -> float:
        """
        Calculate training pattern boost for an assessment
        
        Returns:
            Float between 0 and 1 indicating boost strength
        """
        boost = 0.0
        
        # Frequency boost (popular assessments)
        if url in self.assessment_freq:
            boost += min(self.assessment_freq[url] * 0.08, 0.4)
        
        # Keyword pattern boost
        for word in query_lower.split():
            if word in self.keyword_to_assessments:
                if url in self.keyword_to_assessments[word]:
                    boost += 0.15
        
        return min(boost, 1.0)
