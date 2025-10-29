import os
# This is the line that was missing
from datetime import timedelta

class AppConfig:
    """
    Application configuration class.
    Best practice is to load sensitive data from environment variables.
    """
    
    # Load sensitive values from environment variables. Do NOT commit secrets into source.
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set. Set it in your .env or environment.")

    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    if not ADMIN_PASSWORD:
        raise RuntimeError("ADMIN_PASSWORD environment variable is not set. Set it in your .env or environment.")

    DATABASE_PATH = os.environ.get("DATABASE_PATH",
                                 os.path.join(os.path.dirname(__file__), "..", "..", "data", "realer_ai.db"))

    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI environment variable is not set. Set it in your .env or environment.")

    # Application Settings that are not sensitive
    ADAPTATION_COOLDOWN = 60
    MAX_INSIGHTS_BEFORE_REVIEW = 100
    JWT_EXPIRY_SECONDS = int(timedelta(hours=24).total_seconds())
    SOUL_KEY_VENDOR_ID = 0x1234
    SOUL_KEY_PRODUCT_ID = 0x5678