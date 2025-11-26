import asyncio
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

import accounts.models as user_models

bot = Bot("8324626703:AAFrald_VmXTDhs6osCOvVmP-wZR7rQr0Gs")
dp = Dispatcher()

@dp.message(CommandStart())
async def handler_start(message: Message):
    user_id = message.from_user.id
    if not user_models.CustomUser.objects.filter(telegram_id=user_id).exists():
        await message.answer(f"Assalomu Aleykum, {message.from_user.id}")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())