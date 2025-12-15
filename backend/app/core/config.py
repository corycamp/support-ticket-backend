import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "support-ticket-backend")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()
