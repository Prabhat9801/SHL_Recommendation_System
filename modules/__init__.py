"""
Modular Recommendation System
"""
from modules.data_loader import DataLoader
from modules.preprocessor import DataPreprocessor
from modules.feature_extractor import FeatureExtractor
from modules.llm_client import LLMClient
from modules.training_patterns import TrainingPatternsLearner
from modules.recommender import RecommendationEngine
from modules.evaluator import Evaluator

__all__ = [
    'DataLoader',
    'DataPreprocessor',
    'FeatureExtractor',
    'LLMClient',
    'TrainingPatternsLearner',
    'RecommendationEngine',
    'Evaluator'
]
