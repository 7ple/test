import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# ⚠️ ВСТАВТЕ СВОЇ ДАНІ СЮДИ:
API_TOKEN = '8645421510:AAEllgh-22H5mzNgwpXg9DRE0KMuzfzvths'
ADMIN_CHAT_ID = 8645421510  # Ваш ID з кроку 2

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Привіт! Це редакційна скринька проєкту MatchRoom.**\n\n"
        "📩 Надсилай сюди ваші повідомлення, запитання, новини, інсайди, ідеї "
        "чи помічені помилки - текст, фото, відео.\n\n"
        "✍️ Адміністратори обов'язково прочитають та нададуть відповідь."
    )

@dp.message()
async def handle_messages(message: types.Message):
    if message.chat.id == ADMIN_CHAT_ID:
        if message.reply_to_message and message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
            try:
                await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=ADMIN_CHAT_ID,
                    message_id=message.message_id
                )
            except Exception:
                await message.reply("❌ Не вдалося надіслати відповідь (користувач заблокував бота).")
        return

    try:
        await bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.answer("✅ **Дякуємо! Твоя пропозиція надіслана редакції.**")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
