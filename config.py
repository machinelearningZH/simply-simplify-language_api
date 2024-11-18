import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
MAX_TOKENS = os.getenv("MAX_TOKENS")
TEMPERATURE = os.getenv("TEMPERATURE")
MAX_CHARS_INPUT = os.getenv("MAX_CHARS_INPUT")