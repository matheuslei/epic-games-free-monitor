import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # URLs
    EPIC_GAMES_URL = 'https://store.epicgames.com/pt-BR/free-games'
    
    # Email Settings
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    
    # Workflow
    WORKFLOW_FILE_PATH = '.github/workflows/epic_games_check.yml'
    
    # Browser
    HEADLESS = True
    VIEWPORT = {'width': 1920, 'height': 1080}
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    LOCALE = 'pt-BR'
    TIMEZONE = 'America/Sao_Paulo'
