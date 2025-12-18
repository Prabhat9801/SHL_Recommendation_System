"""
Storage Manager - Saves vectors and predictions
"""
import numpy as np
import pandas as pd
from pathlib import Path
from modules.logger import setup_logger

logger = setup_logger(__name__)

class StorageManager:
    """
    Manages saving of:
    - TF-IDF matrices
    - Semantic embeddings
    - Test predictions
    """
    
    def __init__(self, vector_dir: str = "vector_storage", predictions_dir: str = "predicted_test_csv"):
        self.vector_dir = Path(vector_dir)
        self.predictions_dir = Path(predictions_dir)
        
        # Create directories
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        self.predictions_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"StorageManager initialized: vectors={self.vector_dir}, predictions={self.predictions_dir}")
    
    def save_tfidf_matrix(self, matrix, filename: str = "tfidf_matrix.npz"):
        """Save TF-IDF sparse matrix"""
        try:
            from scipy import sparse
            path = self.vector_dir / filename
            sparse.save_npz(path, matrix)
            logger.info(f"✅ Saved TF-IDF matrix to {path} ({path.stat().st_size / 1024:.1f} KB)")
        except Exception as e:
            logger.error(f"Failed to save TF-IDF matrix: {e}")
    
    def save_semantic_embeddings(self, embeddings: np.ndarray, filename: str = "semantic_embeddings.npy"):
        """Save semantic embeddings"""
        try:
            path = self.vector_dir / filename
            np.save(path, embeddings)
            logger.info(f"✅ Saved semantic embeddings to {path} ({path.stat().st_size / 1024:.1f} KB)")
        except Exception as e:
            logger.error(f"Failed to save embeddings: {e}")
    
    def save_test_predictions(self, predictions_df: pd.DataFrame, filename: str = "test_predictions.csv"):
        """Save test set predictions"""
        try:
            path = self.predictions_dir / filename
            predictions_df.to_csv(path, index=False)
            logger.info(f"✅ Saved test predictions to {path} ({len(predictions_df)} rows)")
        except Exception as e:
            logger.error(f"Failed to save predictions: {e}")
    
    def save_assessment_mapping(self, df: pd.DataFrame, filename: str = "assessment_mapping.csv"):
        """Save assessment ID to URL mapping"""
        try:
            path = self.vector_dir / filename
            df[['name', 'url', 'normalized_url']].to_csv(path, index=False)
            logger.info(f"✅ Saved assessment mapping to {path}")
        except Exception as e:
            logger.error(f"Failed to save mapping: {e}")
