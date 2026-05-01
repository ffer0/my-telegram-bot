from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.config import config, client
import io
import httpx

router = Router()

# Машина состояний для ожидания промпта
class GenerateState(StatesGroup):
    waiting_for_prompt = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎨 Привет! Я бот для генерации изображений через DALL-E 3\n\n"
        "📝 Как использовать:\n"
        "• Отправь /image - начнём генерацию\n"
        "• Или просто напиши описание после /image\n\n"
        "Пример: /image кот в космосе в стиле киберпанк\n\n"
        "💰 Пока все генерации бесплатные!"
    )

@router.message(Command("image"))
async def cmd_image(message: types.Message, state: FSMContext):
    prompt = message.text.replace("/image", "").strip()
    
    if not prompt:
        await message.answer("❌ Напиши описание после /image\nПример: /image кот в космосе")
        return
    
    await message.answer(f"🎨 Генерирую: {prompt}\nОбычно 10-20 секунд...")
    
    try:
        # Генерируем картинку через DALL-E 3 (используем клиент из config)
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        
        # Скачиваем изображение
        async with httpx.AsyncClient() as http_client:
            img_response = await http_client.get(image_url)
            img_bytes = io.BytesIO(img_response.content)
            img_bytes.seek(0)
            
            # Отправляем фото
            await message.answer_photo(
                photo=types.BufferedInputFile(
                    img_bytes.getvalue(), 
                    filename="generated.png"
                ),
                caption=f"✨ Сгенерировано по запросу:\n{prompt[:200]}"
            )
        
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\n\nПроверьте баланс в ProxyAPI или попробуйте другой промпт.")
    
    await state.clear()