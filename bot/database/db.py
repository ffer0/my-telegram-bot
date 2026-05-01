from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, func
from datetime import datetime, timedelta
from bot.config import config
from bot.database.models import User, Generation, VoiceMessage, init_db

# Инициализация БД
init_db()

engine = create_async_engine(config.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        return result.scalar_one_or_none()

async def create_user(user_id: int, username: str, full_name: str):
    async with AsyncSessionLocal() as session:
        user = User(telegram_id=user_id, username=username, full_name=full_name, credits=10)
        session.add(user)
        await session.commit()
        return user

async def add_generation(user_id: int, prompt: str, model: str, style: str, image_url: str):
    async with AsyncSessionLocal() as session:
        gen = Generation(user_id=user_id, prompt=prompt, model=model, style=style, image_url=image_url)
        session.add(gen)
        
        # Увеличиваем счётчик
        await session.execute(update(User).where(User.telegram_id == user_id).values(
            total_generations=User.total_generations + 1,
            credits=User.credits - 1
        ))
        await session.commit()

async def get_today_generations(user_id: int):
    async with AsyncSessionLocal() as session:
        today = datetime.now().date()
        result = await session.execute(
            select(func.count(Generation.id)).where(
                Generation.user_id == user_id,
                func.date(Generation.created_at) == today
            )
        )
        return result.scalar() or 0
