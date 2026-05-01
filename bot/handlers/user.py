import io
import httpx
import urllib.parse
from aiogram import Router, types
from aiogram.filters import Command

@router.message(Command("image"))
async def generate_image(message: types.Message):
    prompt = message.text.replace("/image", "").strip()

    if not prompt:
        await message.answer("❌ Напиши описание после команды /image")
        return

    await message.answer(f"🎨 Генерирую: {prompt[:100]}...")

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            # Создаём объект InputFile из байтов
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
