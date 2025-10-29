import os
from datetime import timedelta

class ProductionConfig:
    """Production configuration"""
    
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32).hex())
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "CHANGE_THIS_IN_PRODUCTION")
    
    # Database - Use absolute path for production
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "/opt/r3aler-ai/data/realer_ai.db")
    
    # Application Settings
    ADAPTATION_COOLDOWN = 60
    MAX_INSIGHTS_BEFORE_REVIEW = 100
    JWT_EXPIRY_SECONDS = int(timedelta(hours=24).total_seconds())
    SOUL_KEY_VENDOR_ID = 0x1234
    SOUL_KEY_PRODUCT_ID = 0x5678
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "/opt/r3aler-ai/logs/app.log"