"""
Feature Extractor Module with Logging & Exception Handling
Handles TF-IDF and semantic embedding generation
"""
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import pandas as pd
from modules.logger import setup_logger
from modules.exceptions import FeatureExtractionException

logger = setup_logger(__name__)

class FeatureExtractor:
    """
    Responsible for extracting features from assessment data:
    - TF-IDF vectors for keyword matching
    - Semantic embeddings for meaning matching
    """
    
    def __init__(self):
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.embedding_model = None
        self.semantic_embeddings = None
        logger.info("FeatureExtractor initialized")
    
    def build_tfidf_features(
        self, 
        assessments_df: pd.DataFrame,
        max_features: int = 10000,
        ngram_range: Tuple[int, int] = (1, 4)
    ) -> np.ndarray:
        """
        Build TF-IDF matrix with strategic field weighting
        """
        try:
            logger.info(f"Building TF-IDF features (max_features={max_features}, ngram={ngram_range})...")
            
            if assessments_df is None or len(assessments_df) == 0:
                raise FeatureExtractionException("Empty assessments dataframe")
            
            # Create weighted documents
            documents = []
            for idx, row in assessments_df.iterrows():
                try:
                    name = str(row['name'])
                    desc = str(row.get('description', ''))[:500]
                    test_type = str(row.get('test_type', '')).replace('|', ' ')
                    remote = str(row.get('remote_support', ''))
                    adaptive = str(row.get('adaptive_support', ''))
                    
                    # Strategic weighting by repetition
                    doc = (
                        f"{' '.join([name]*25)} "
                        f"{' '.join([test_type]*12)} " 
                        f"{' '.join([remote]*5)} "
                        f"{' '.join([adaptive]*3)} "
                        f"{desc}"
                    )
                    documents.append(doc)
                except Exception as e:
                    logger.warning(f"Skipping assessment at index {idx}: {e}")
                    documents.append("")  # Add empty document to maintain alignment
            
            # Build TF-IDF
            logger.debug("Fitting TF-IDF vectorizer...")
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                min_df=1,
                max_df=0.7,
                sublinear_tf=True,
                stop_words='english'
            )
            
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
            
            logger.info(f"✅ TF-IDF matrix shape: {self.tfidf_matrix.shape}")
            return self.tfidf_matrix
            
        except FeatureExtractionException:
            raise
        except Exception as e:
            logger.error(f"TF-IDF feature extraction failed: {e}")
            raise FeatureExtractionException(f"Failed to build TF-IDF: {str(e)}") from e
    
    def build_semantic_embeddings(
        self,
        assessments_df: pd.DataFrame,
        model_name: str = 'all-MiniLM-L6-v2'
    ) -> np.ndarray:
        """
        Build semantic embeddings using Sentence-BERT
        """
        try:
            logger.info(f"Building semantic embeddings (model={model_name})...")
            
            if assessments_df is None or len(assessments_df) == 0:
                raise FeatureExtractionException("Empty assessments dataframe")
            
            # Initialize model from cache
            if self.embedding_model is None:
                logger.debug(f"Loading embedding model: {model_name}")
                
                # Use cached model directory
                cache_dir = os.path.join(os.getcwd(), '.model_cache')
                
                # Load model from cache (already downloaded during deployment)
                self.embedding_model = SentenceTransformer(
                    model_name, 
                    cache_folder=cache_dir
                )
            
            # Create rich text representations
            texts = []
            for idx, row in assessments_df.iterrows():
                try:
                    test_type_clean = str(row.get('test_type', '')).replace('|', ', ')
                    remote = "Remote-friendly" if str(row.get('remote_support', '')).lower() == 'yes' else ""
                    adaptive = "Adaptive test" if str(row.get('adaptive_support', '')).lower() == 'yes' else ""
                    duration = f"{row.get('duration', 20)} minutes"
                    
                    text = (
                        f"{row['name']}. {row['description']}. "
                        f"Categories: {test_type_clean}. Duration: {duration}. "
                        f"{remote} {adaptive}"
                    )
                    texts.append(text)
                except Exception as e:
                    logger.warning(f"Error creating text for assessment {idx}: {e}")
                    texts.append(f"{row.get('name', 'Unknown')}")
            
            # Generate embeddings
            logger.debug(f"Encoding {len(texts)} texts...")
            self.semantic_embeddings = self.embedding_model.encode(
                texts,
                show_progress_bar=False
            )
            
            logger.info(f"✅ Semantic embeddings shape: {self.semantic_embeddings.shape}")
            return self.semantic_embeddings
            
        except FeatureExtractionException:raise
        except Exception as e:
            logger.error(f"Semantic embedding generation failed: {e}")
            raise FeatureExtractionException(f"Failed to build embeddings: {str(e)}") from e
    
    def get_query_tfidf_scores(self, query: str) -> np.ndarray:
        """Compute TF-IDF similarity scores for a query"""
        try:
            if self.tfidf_vectorizer is None or self.tfidf_matrix is None:
                raise FeatureExtractionException("TF-IDF not initialized. Call build_tfidf_features first.")
            
            logger.debug(f"Computing TF-IDF scores for query: {query[:50]}...")
            query_vec = self.tfidf_vectorizer.transform([query])
            
            from sklearn.metrics.pairwise import cosine_similarity
            scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            
            logger.debug(f"TF-IDF scores computed (max: {scores.max():.3f})")
            return scores
            
        except FeatureExtractionException:
            raise
        except Exception as e:
            logger.error(f"TF-IDF scoring failed: {e}")
            raise FeatureExtractionException(f"Failed to compute TF-IDF scores: {str(e)}") from e
    
    def get_query_semantic_scores(self, query: str) -> np.ndarray:
        """Compute semantic similarity scores for a query"""
        try:
            # Check if semantic embeddings exist
            if self.semantic_embeddings is None:
                raise FeatureExtractionException("Embeddings not initialized. Call build_semantic_embeddings first.")
            
            # Handle LOW_MEMORY mode (embedding_model is None, embeddings are zeros)
            if self.embedding_model is None:
                logger.debug("LOW_MEMORY mode: returning zero semantic scores")
                # Return all zeros (semantic matching disabled)
                num_assessments = self.semantic_embeddings.shape[0]
                return np.zeros(num_assessments)
            
            # Normal mode: compute actual semantic similarity
            logger.debug(f"Computing semantic scores for query: {query[:50]}...")
            query_emb = self.embedding_model.encode([query])
            
            from sklearn.metrics.pairwise import cosine_similarity
            scores = cosine_similarity(query_emb, self.semantic_embeddings)[0]
            
            logger.debug(f"Semantic scores computed (max: {scores.max():.3f})")
            return scores
            
        except FeatureExtractionException:
            raise
        except Exception as e:
            logger.error(f"Semantic scoring failed: {e}")
            raise FeatureExtractionException(f"Failed to compute semantic scores: {str(e)}") from e
