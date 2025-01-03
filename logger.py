import logging

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Logs to console
    ]
)

# Create and configure a logger instance
logger = logging.getLogger("fastapi_app")

# Optional: Adjust log level here if needed
logger.setLevel(logging.DEBUG)