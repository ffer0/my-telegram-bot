from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from bot.config import config

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    full_name = Column(String(200))
    credits = Column(Integer, default=10)
    total_generations = Column(Integer, default=0)
    subscription_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

class Generation(Base):
    __tablename__ = "generations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    prompt = Column(Text)
    model = Column(String(50))
    style = Column(String(100))
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)

class VoiceMessage(Base):
    __tablename__ = "voice_messages"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    transcribed_text = Column(Text)
    response_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

def init_db():
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine
