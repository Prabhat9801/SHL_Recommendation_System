"""
Pre-download required models during deployment
This script downloads all required models before the application starts
"""
import os
from sentence_transformers import SentenceTransformer

def download_models():
    """Download all required models during build/deployment"""
    
    print("=" * 80)
    print("DOWNLOADING REQUIRED MODELS FOR DEPLOYMENT")
    print("=" * 80)
    
    # Set cache directory
    cache_dir = os.path.join(os.getcwd(), '.model_cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Set environment variable for transformers cache
    os.environ['TRANSFORMERS_CACHE'] = cache_dir
    os.environ['SENTENCE_TRANSFORMERS_HOME'] = cache_dir
    
    try:
        # Download the sentence-transformers model
        model_name = 'all-MiniLM-L6-v2'
        print(f"\n📦 Downloading model: {model_name}")
        print(f"📁 Cache directory: {cache_dir}")
        print("-" * 80)
        
        # This will download and cache the model
        model = SentenceTransformer(model_name, cache_folder=cache_dir)
        
        print("-" * 80)
        print(f"✅ Model '{model_name}' downloaded successfully!")
        print(f"📊 Model cached at: {cache_dir}")
        
        # Test the model to ensure it works
        print("\n🧪 Testing model...")
        test_embedding = model.encode(["Test sentence"])
        print(f"✅ Model test successful! Embedding shape: {test_embedding.shape}")
        
        print("\n" + "=" * 80)
        print("✅ ALL MODELS DOWNLOADED SUCCESSFULLY")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading models: {e}")
        print("=" * 80)
        return False

if __name__ == "__main__":
    success = download_models()
    exit(0 if success else 1)
