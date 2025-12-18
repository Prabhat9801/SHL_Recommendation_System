"""
Data Preprocessor Module
Handles data cleaning, normalization, and structuring
"""
import pandas as pd
from typing import Tuple
from modules.logger import setup_logger
from modules.exceptions import DataPreprocessingException

logger = setup_logger(__name__)

class DataPreprocessor:
    """
    Responsible for cleaning and preparing data for feature extraction
    """
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL format for consistency"""
        try:
            if pd.isna(url):
                return url
            return url.replace('/solutions/products/', '/products/')
        except Exception as e:
            logger.warning(f"Failed to normalize URL: {url}, error: {e}")
            return url
    
    def clean_scraped_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare scraped assessment data
        - Normalize URLs
        - Remove duplicates
        - Handle missing values
        """
        try:
            logger.info("Preprocessing scraped data...")
            
            if df is None or len(df) == 0:
                raise DataPreprocessingException("Input dataframe is empty")
            
            original_count = len(df)
            
            # Normalize URLs
            logger.debug("Normalizing URLs...")
            df['normalized_url'] = df['url'].apply(self.normalize_url)
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['normalized_url']).reset_index(drop=True)
            duplicates_removed = original_count - len(df)
            
            if duplicates_removed > 0:
                logger.info(f"Removed {duplicates_removed} duplicate assessments")
            
            logger.info(f"✅ {len(df)} clean assessments ready")
            return df
            
        except DataPreprocessingException:
            raise
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise DataPreprocessingException(f"Failed to clean data: {str(e)}") from e
    
    def prepare_train_data(self, train_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare training data with normalized URLs"""
        try:
            logger.debug("Preparing training data...")
            train_df['normalized_url'] = train_df['Assessment_url'].apply(self.normalize_url)
            logger.debug("✅ Training data prepared")
            return train_df
        except Exception as e:
            logger.error(f"Failed to prepare training data: {e}")
            raise DataPreprocessingException(f"Training data prep failed: {str(e)}") from e
    
    def merge_train_with_assessments(
        self,
        train_df: pd.DataFrame,
        assessments_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Merge training data with full assessment details"""
        try:
            logger.debug("Merging training data with assessments...")
            
            merged = train_df.merge(
                assessments_df[[
                    'normalized_url', 'name', 'description', 
                    'test_type', 'duration', 'adaptive_support', 'remote_support'
                ]],
                on='normalized_url',
                how='left'
            )
            
            missing_count = merged['name'].isna().sum()
            if missing_count > 0:
                logger.warning(f"{missing_count} training examples missing assessment details")
            
            logger.debug(f"✅ Merged {len(merged)} training examples")
            return merged
            
        except Exception as e:
            logger.error(f"Failed to merge data: {e}")
            raise DataPreprocessingException(f"Merge failed: {str(e)}") from e
