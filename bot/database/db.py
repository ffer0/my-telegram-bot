from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, func, and_
from datetime import datetime, date
from bot.config import config
from bot.database.models import User, Generation, VoiceMessage, Payment

# Создаём асинхронный движок
engine = create_async_engine(
    config.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=True
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ============ USER ============
async def get_user(telegram_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

async def create_user(telegram_id: int, username: str = None, full_name: str = None):
    async with AsyncSessionLocal() as session:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            credits=10  # Бесплатные генерации при регистрации
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def update_credits(telegram_id: int, delta: int):
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                credits=User.credits + delta
            )
        )
        await session.commit()

async def get_today_generations(telegram_id: int) -> int:
    async with AsyncSessionLocal() as session:
        today = date.today()
        result = await session.execute(
            select(func.count(Generation.id)).where(
                and_(
                    Generation.user_id == telegram_id,
                    func.date(Generation.created_at) == today
                )
            )
        )
        return result.scalar() or 0

async def increment_total_generations(telegram_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                total_generations=User.total_generations + 1
            )
        )
        await session.commit()

# ============ GENERATION ============
async def add_generation(telegram_id: int, prompt: str, model: str, style: str, size: str, image_url: str = ""):
    async with AsyncSessionLocal() as session:
        # Получаем user_id из БД
        user = await get_user(telegram_id)
        if not user:
            return None
        
        gen = Generation(
            user_id=user.id,
            prompt=prompt,
            model=model,
            style=style,
            size=size,
            image_url=image_url
        )
        session.add(gen)
        
        # Уменьшаем кредиты
        await session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                credits=User.credits - 1,
                total_generations=User.total_generations + 1
            )
        )
        await session.commit()
        return gen

# ============ VOICE ============
async def add_voice_message(telegram_id: int, transcribed_text: str, response_text: str, duration: int = None):
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id)
        if not user:
            return None
        
        voice = VoiceMessage(
            user_id=user.id,
            transcribed_text=transcribed_text,
            response_text=response_text,
            duration=duration
        )
        session.add(voice)
        
        # Увеличиваем счётчик голосовых
        await session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                total_voice=User.total_voice + 1
            )
        )
        await session.commit()
        return voice

# ============ PAYMENT ============
async def add_payment(telegram_id: int, amount_stars: int, credits_added: int, telegram_payment_id: str):
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id)
        if not user:
            return None
        
        payment = Payment(
            user_id=user.id,
            amount_stars=amount_stars,
            credits_added=credits_added,
            telegram_payment_id=telegram_payment_id,
            status="completed"
        )
        session.add(payment)
        
        # Добавляем кредиты
        await session.execute(
            update(User).where(User.telegram_id == telegram_id).values(
                credits=User.credits + credits_added
            )
        )
        await session.commit()
        return payment

# ============ STATS ============
async def get_user_stats(telegram_id: int):
    async with AsyncSessionLocal() as session:
        user = await get_user(telegram_id)
        if not user:
            return None
        
        today_gens = await get_today_generations(telegram_id)
        
        return {
            "credits": user.credits,
            "total_generations": user.total_generations,
            "total_voice": user.total_voice,
            "today_generations": today_gens,
            "subscription_active": user.subscription_until and user.subscription_until > datetime.now()
        }
