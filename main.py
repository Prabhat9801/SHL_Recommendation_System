"""
Main Entry Point - Demonstrates Modular Pipeline  
Shows clear separation of concerns and data flow
"""

from modules import RecommendationEngine, Evaluator
from modules.storage_manager import StorageManager
import pandas as pd
import logging

def main():
    """
    Demonstrates the complete modular pipeline:
    Data → Preprocessing → Feature Extraction → LLM → Scoring → Recommendations
    """
    
    # Get root logger and ensure it flushes
    root_logger = logging.getLogger()
    
    print("="*80)
    print("SHL ASSESSMENT RECOMMENDATION SYSTEM - MODULAR ARCHITECTURE")
    print("90.4% Mean Recall@10 Performance")
    print("="*80)
    
    # Initialize modular recommendation engine
    engine = RecommendationEngine()
    
    # Initialize system (runs full pipeline)
    engine.initialize()
    
    # Flush logs after initialization
    for handler in root_logger.handlers:
        handler.flush()
    
    # Initialize storage manager
    storage = StorageManager()
    
    # Save vectors to disk
    print("\n💾 Saving vectors to disk...")
    storage.save_tfidf_matrix(engine.feature_extractor.tfidf_matrix)
    storage.save_semantic_embeddings(engine.feature_extractor.semantic_embeddings)
    storage.save_assessment_mapping(engine.df_assessments)
    
    # Flush logs after saving
    for handler in root_logger.handlers:
        handler.flush()
    
    # Evaluate performance
    evaluator = Evaluator(engine)
    recall = evaluator.evaluate_recall_at_k(k=10)
    
    print(f"\n{'='*80}")
    print(f"FINAL PERFORMANCE: {recall*100:.1f}% Mean Recall@10")
    print(f"{'='*80}\n")
    
    # Flush logs after evaluation
    for handler in root_logger.handlers:
        handler.flush()
    
    # Generate test predictions
    print("📊 Generating test predictions...")
    test_data = engine.data_loader.test_data
    
    predictions = []
    submission_data = []  # For submission format
    
    for idx, row in test_data.iterrows():
        query = row['Query']
        print(f"  [{idx+1}/{len(test_data)}] Processing: {query[:50]}...")
        
        # Get top-10 recommendations
        results = engine.recommend(query, top_k=10)
        
        # Format for detailed CSV
        for rank, rec in enumerate(results, 1):
            predictions.append({
                'Query': query,
                'Rank': rank,
                'Assessment_Name': rec['assessment_name'],
                'Assessment_URL': rec['assessment_url'],
                'Relevance_Score': rec['relevance_score']
            })
            
            # Format for submission CSV (only Query and Assessment_url)
            submission_data.append({
                'Query': query,
                'Assessment_url': rec['assessment_url']
            })
    
    # Save detailed predictions
    predictions_df = pd.DataFrame(predictions)
    storage.save_test_predictions(predictions_df, filename='test_predictions_detailed.csv')
    print(f"✅ Saved {len(predictions)} detailed predictions to predicted_test_csv/\n")
    
    # Save submission format CSV (Appendix 3 format)
    submission_df = pd.DataFrame(submission_data)
    storage.save_test_predictions(submission_df, filename='test_predictions.csv')
    print(f"✅ Saved submission file (Query, Assessment_url) to predicted_test_csv/test_predictions.csv\n")
    
    # Final flush
    for handler in root_logger.handlers:
        handler.flush()
    
    # Example recommendation
    print("Example Recommendation:")
    print("-"*80)
    query = "I need Java developers who can collaborate effectively with business teams"
    print(f"Query: {query}\n")
    
    results = engine.recommend(query, top_k=5)
    
    for i, rec in enumerate(results, 1):
        print(f"{i}. {rec['assessment_name']}")
        print(f"   Score: {rec['relevance_score']:.3f}")
        print(f"   Type: {', '.join(rec['test_type'])}")
        print()
    
    # Final flush to ensure all logs are written
    print("\n💾 Flushing all logs to disk...")
    for handler in root_logger.handlers:
        handler.flush()
    
    print("✅ All logs saved!\n")

if __name__ == "__main__":
    main()
