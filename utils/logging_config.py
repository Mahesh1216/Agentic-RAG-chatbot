import logging
import os
from config.settings import settings

def setup_logging():
    """Configures the logging for the application."""
    log_dir = os.path.join(settings.BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Set up a logger for the application
    logger = logging.getLogger(__name__)
    logger.info("Logging configured.")

    return logger

# Initialize logging when this module is imported
logger = setup_logging()