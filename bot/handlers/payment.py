from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("buy"))
async def cmd_buy(message: types.Message):
    await message.answer(
        "⭐️ Покупка кредитов через Telegram Stars\n\n"
        "Функция оплаты будет добавлена позже.\n"
        "Пока все генерации бесплатные! 🎁\n\n"
        "Используй /image для создания картинок"
    )