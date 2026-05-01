import io
import httpx
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎨 Привет! Я бот для генерации изображений.\n"
        "Отправь команду /image и описание.\n"
        "Пример: /image красный цветок на белом фоне"
    )

@router.message(Command("image"))
async def generate_image(message: types.Message):
    # Получаем текст после команды
    prompt = message.text.replace("/image", "").strip()

    if not prompt:
        await message.answer("❌ Напиши описание после команды /image")
        return

    await message.answer(f"🎨 Генерирую: {prompt[:100]}... (обычно 10-20 секунд)")

    # Кодируем промпт для URL
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)

    # Используем Pollinations API (бесплатно, без ключей)
    url = f"https://pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            # Отправляем изображение пользователю
            photo_bytes = io.BytesIO(response.content)
            photo_bytes.seek(0)

            await message.reply_photo(
                photo=photo_bytes,
                caption=f"✨ Сгенерировано по запросу: {prompt[:200]}"
            )

    except httpx.TimeoutException:
        await message.answer("❌ Превышено время ожидания. Попробуйте более простой запрос.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
