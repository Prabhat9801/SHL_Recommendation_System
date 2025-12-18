"""
LLM Client Module with Logging & Exception Handling
Handles all LLM interactions for query understanding
"""
import json
from groq import Groq
from typing import Dict
from dotenv import load_dotenv
import os
from modules.logger import setup_logger
from modules.exceptions import LLMException

load_dotenv()
logger = setup_logger(__name__)

class LLMClient:
    """
    Responsible for LLM-based query understanding
    Extracts skills, keywords, and role information
    """
    
    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.model = model
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set - LLM functionality will be limited")
        else:
            logger.info(f"LLMClient initialized with model: {model}")
        
        try:
            self.client = Groq(api_key=self.api_key) if self.api_key else None
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise LLMException(f"Groq client initialization failed: {str(e)}") from e
    
    def extract_requirements(self, query: str, max_retries: int = 2) -> Dict:
        """
        Extract structured information from natural language query
        
        Args:
            query: Natural language query
            max_retries: Number of retry attempts
        
        Returns:
            {
                "technical_skills": ["skill1", "skill2"],
                "soft_skills": ["skill1", "skill2"],
                "role_type": "developer/analyst/etc",
                "keywords": ["key1", "key2"]
            }
        """
        if not self.client:
            logger.warning("LLM client not available - returning empty requirements")
            return {
                "technical_skills": [],
                "soft_skills": [],
                "role_type": "unknown",
                "keywords": []
            }
        
        prompt = f"""Extract from job query. Return ONLY valid JSON:

Query: "{query}"

{{
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "role_type": "developer/analyst/manager/sales/etc",
    "keywords": ["key1", "key2"]
}}

JSON:"""
        
        for attempt in range(max_retries + 1):
            try:
                logger.debug(f"LLM extraction attempt {attempt + 1}/{max_retries + 1} for query: {query[:50]}...")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Extract requirements from job queries. Return only JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0,
                    max_tokens=500
                )
                
                text = response.choices[0].message.content.strip()
                
                # Clean JSON from markdown
                if '```json' in text:
                    text = text.split('```json')[1].split('```')[0].strip()
                elif '```' in text:
                    text = text.split('```')[1].split('```')[0].strip()
                
                result = json.loads(text)
                logger.info(f"✅ LLM extraction successful: {len(result.get('technical_skills', []))} technical, "
                           f"{len(result.get('soft_skills', []))} soft skills")
                
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse error (attempt {attempt + 1}): {e}")
                if attempt < max_retries:
                    continue
                else:
                    logger.error("All retry attempts failed - returning empty requirements")
                    return {
                        "technical_skills": [],
                        "soft_skills": [],
                        "role_type": "unknown",
                        "keywords": []
                    }
            
            except Exception as e:
                logger.error(f"LLM API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries:
                    continue
                else:
                    logger.warning("LLM extraction failed - falling back to empty requirements")
                    return {
                        "technical_skills": [],
                        "soft_skills": [],
                        "role_type": "unknown",
                        "keywords": []
                    }
        
        # Should never reach here, but just in case
        return {
            "technical_skills": [],
            "soft_skills": [],
            "role_type": "unknown",
            "keywords": []
        }
