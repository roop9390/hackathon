import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    # Gemini Model Configuration
    GEMINI_MODEL = "gemini-2.0-flash-exp"  # Using experimental version for better performance
    
    # API Keys (if using external services)
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
    
    # Constants
    MAX_TEAM_MEMBERS = 10
    REQUEST_TIMEOUT = 30
    
    # Google APIs (will use application default credentials)
    @property
    def vertexai_project(self):
        return self.GOOGLE_CLOUD_PROJECT
    
    @property 
    def vertexai_location(self):
        return "us-central1"