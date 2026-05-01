import io
import httpx
import urllib.parse
from aiogram import Router, types
from aiogram.filters import Command

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
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(image_url)
            response.raise_for_status()

            photo_bytes = io.BytesIO(response.content)
            photo_bytes.seek(0)

            from aiogram.types import BufferedInputFile
            photo_file = BufferedInputFile(
                file=response.content,
                filename="generated.jpg"
            )

            await message.reply_photo(
                photo=photo_file,
                caption=f"✨ Сгенерировано по запросу: {prompt[:200]}"
            )

    except httpx.TimeoutException:
        await message.answer("❌ Превышено время ожидания. Попробуйте более простой запрос.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
