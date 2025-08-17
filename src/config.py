"""
Configuration management for the Fear & Greed Trading Framework.

This module uses pydantic-settings to load configuration from environment
variables and .env files, providing a centralized and validated source of
settings for the application.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Defines the application's configuration settings.

    Pydantic-settings will automatically search for a .env file in the
    project's root directory and load the variables defined here.
    Environment variables will always override values from a .env file.
    """
    # -- Core Settings --
    LOG_LEVEL: str = "INFO"

    # -- Database (PostgreSQL) --
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/trading_framework"

    # -- Redis --
    REDIS_URL: str = "redis://localhost:6379"

    # -- API Keys --
    FEAR_GREED_API_KEY: str = "your_api_key_here"
    MARKET_DATA_API_KEY: str = "your_api_key_here"
    EXCHANGE_API_KEY: str = "your_api_key_here"
    EXCHANGE_API_SECRET: str = "your_api_secret_here"
    TWITTER_API_KEY: str = "your_api_key_here"
    REDDIT_CLIENT_ID: str = "your_client_id_here"
    REDDIT_CLIENT_SECRET: str = "your_client_secret_here"

    # model_config is used to configure the behavior of the BaseSettings class.
    # Here, we specify the name of the .env file to look for.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single, reusable instance of the Settings class.
# Other modules should import this `settings` object.
settings = Settings()

if __name__ == '__main__':
    # Example of how to access the settings
    # This block will only run when the script is executed directly
    print("--- Application Settings ---")
    print(f"Log Level: {settings.LOG_LEVEL}")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Redis URL: {settings.REDIS_URL}")
    print("--------------------------")
