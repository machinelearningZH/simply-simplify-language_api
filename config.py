import os

from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# Access the variables.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
MAX_TOKENS = os.getenv("MAX_TOKENS")
SITE_URL = os.getenv("SITE_URL", "")  # Optional: Your site URL
SITE_NAME = os.getenv("SITE_NAME", "")  # Optional: Your site name
