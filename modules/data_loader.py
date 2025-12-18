"""
Data Loader Module
Handles all data loading and initial ingestion
"""
import pandas as pd
from pathlib import Path
from typing import Dict
from modules.logger import setup_logger
from modules.exceptions import DataLoadException

logger = setup_logger(__name__)

class DataLoader:
    """
    Responsible for loading scraped assessment data and train/test datasets
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.scraped_data = None
        self.train_data = None
        self.test_data = None
        logger.info(f"DataLoader initialized with data_dir: {self.data_dir}")
    
    def load_scraped_assessments(self) -> pd.DataFrame:
        """Load scraped SHL assessments"""
        try:
            csv_path = self.data_dir / "shl_individual_test_solutions.csv"
            
            if not csv_path.exists():
                raise DataLoadException(f"Assessment file not found: {csv_path}")
            
            logger.info(f"Loading scraped assessments from {csv_path}")
            self.scraped_data = pd.read_csv(csv_path)
            
            if len(self.scraped_data) == 0:
                raise DataLoadException("Loaded 0 assessments - file may be empty")
            
            logger.info(f"✅ Loaded {len(self.scraped_data)} assessments successfully")
            return self.scraped_data
            
        except pd.errors.EmptyDataError as e:
            logger.error(f"CSV file is empty: {e}")
            raise DataLoadException(f"Empty CSV file: {csv_path}") from e
        except Exception as e:
            logger.error(f"Failed to load scraped assessments: {e}")
            raise DataLoadException(f"Error loading assessments: {str(e)}") from e
    
    def load_train_test_data(self) -> Dict[str, pd.DataFrame]:
        """Load training and test datasets"""
        try:
            excel_path = self.data_dir / "Gen_AI Dataset (1).xlsx"
            
            if not excel_path.exists():
                raise DataLoadException(f"Excel file not found: {excel_path}")
            
            logger.info(f"Loading train/test data from {excel_path}")
            
            self.train_data = pd.read_excel(excel_path, sheet_name='Train-Set')
            self.test_data = pd.read_excel(excel_path, sheet_name='Test-Set')
            
            logger.info(f"✅ Loaded {len(self.train_data)} training examples")
            logger.info(f"✅ Loaded {len(self.test_data)} test queries")
            
            return {
                'train': self.train_data,
                'test': self.test_data
            }
            
        except ValueError as e:
            logger.error(f"Sheet name not found in Excel: {e}")
            raise DataLoadException(f"Missing sheet in Excel: {str(e)}") from e
        except Exception as e:
            logger.error(f"Failed to load train/test data: {e}")
            raise DataLoadException(f"Error loading Excel data: {str(e)}") from e
    
    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all datasets"""
        try:
            logger.info("Loading all data...")
            scraped = self.load_scraped_assessments()
            train_test = self.load_train_test_data()
            
            logger.info("✅ All data loaded successfully")
            return {
                'scraped': scraped,
                'train': train_test['train'],
                'test': train_test['test']
            }
        except DataLoadException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            raise DataLoadException(f"Failed to load data: {str(e)}") from e
