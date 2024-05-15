import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./conversations.db")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

    @classmethod
    def log_config(cls):
        print(f"OPENAI_API_KEY: {'Loaded' if cls.OPENAI_API_KEY else 'Not Loaded'}")
        print(f"DATABASE_URL: {cls.DATABASE_URL}")
        print(f"GOOGLE_API_KEY: {'Loaded' if cls.GOOGLE_API_KEY else 'Not Loaded'}")
        print(f"GOOGLE_CSE_ID: {'Loaded' if cls.GOOGLE_CSE_ID else 'Not Loaded'}")

# Log the configuration values when the module is imported
Config.log_config()
