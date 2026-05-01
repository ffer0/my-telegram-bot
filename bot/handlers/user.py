import io
import httpx
import urllib.parse
from aiogram import Router, types
from aiogram.filters import Command

# ЭТА СТРОЧКА БЫЛА ПРОПУЩЕНА
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎨 Привет! Я бот для генерации изображений.\n"
        "Отправь команду /image и описание.\n"
        "Пример: /image красный цветок"
    )

@router.message(Command("image"))
async def generate_image(message: types.Message):
    prompt = message.text.replace("/image", "").strip()

    if not prompt:
        await message.answer("❌ Напиши описание после команды /image")
        return

    await message.answer(f"🎨 Генерирую: {prompt[:100]}...")

    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"

    try:
        await message.reply_photo(
            photo=image_url,
            caption=f"✨ Сгенерировано по запросу: {prompt[:200]}"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
