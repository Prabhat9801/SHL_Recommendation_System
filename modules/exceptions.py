"""
Custom Exceptions
Define application-specific exceptions for better error handling
"""

class SHLRecommenderException(Exception):
    """Base exception for SHL Recommender"""
    pass

class DataLoadException(SHLRecommenderException):
    """Raised when data loading fails"""
    pass

class DataPreprocessingException(SHLRecommenderException):
    """Raised when data preprocessing fails"""
    pass

class FeatureExtractionException(SHLRecommenderException):
    """Raised when feature extraction fails"""
    pass

class LLMException(SHLRecommenderException):
    """Raised when LLM API call fails"""
    pass

class RecommendationException(SHLRecommenderException):
    """Raised when recommendation generation fails"""
    pass

class EvaluationException(SHLRecommenderException):
    """Raised when evaluation fails"""
    pass
