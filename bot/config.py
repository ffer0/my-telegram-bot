import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    
    # База данных
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/bot.db")
    
    # API ключи
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # Настройки генерации по умолчанию
    DEFAULT_MODEL = "flux"
    DEFAULT_SIZE = "1024x1024"
    DEFAULT_QUALITY = "standard"
    FREE_GENERATIONS_PER_DAY = 10
    
    # Цены в Telegram Stars
    PRICES = {
        "100_generations": 200,   # 200 Stars ≈ $4
        "500_generations": 800,   # 800 Stars ≈ $16
        "unlimited_month": 2000   # 2000 Stars ≈ $40
    }

config = Config()
