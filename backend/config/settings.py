from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    GOOGLE_APPLICATION_CREDENTIALS: str
    PROJECT_ID: str
    LOCATION: str = "us-central1" # Example: "us-central1", "europe-west1"
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash" # Or "gemini-1.5-pro" for more advanced tasks

    # Configure Pydantic to load from .env file
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()

# --- IMPORTANT: Guide for .env file ---
# This block is for user guidance during setup.
# In a production environment, ensure these variables are set externally.
env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
if not os.path.exists(env_file_path):
    print("\n--- Setup Warning ---")
    print(f"'.env' file not found at '{env_file_path}'.")
    print("Please create one in the 'backend' directory with the following content:")
    print("-----------------------------------------------------------------")
    print("GOOGLE_APPLICATION_CREDENTIALS=\"/path/to/your/service-account-key.json\"")
    print("PROJECT_ID=\"your-gcp-project-id\"")
    print("# LOCATION=\"us-central1\"")
    print("# GEMINI_MODEL_NAME=\"gemini-1.5-flash\"")
    print("-----------------------------------------------------------------")
    print("Ensure you replace the placeholder values with your actual GCP credentials and project ID.")
    print("-----------------------------------------------------------------\n")