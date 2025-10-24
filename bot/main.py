import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
import asyncio

BOT_TOKEN = "8260223409:AAEJsckweSzRwJHW9ElLaAy1u_4lP5yen4U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Bazani tayyorlash ---
def init_db():
    con = sqlite3.connect("bot/database.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT,
            username TEXT
        )
    """)
    con.commit()
    con.close()

# --- Foydalanuvchini bazaga qo‘shish ---
def add_user(user_id, full_name, username):
    con = sqlite3.connect("bot/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    data = cur.fetchone()
    if not data:
        cur.execute("INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)", 
                    (user_id, full_name, username))
        con.commit()
    con.close()

# --- /start komandasi ---
@dp.message(CommandStart())
async def start_handler(message: Message):
    add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(f"Salom, {message.from_user.full_name}! 👋\nSiz bazaga qo‘shildingiz ✅")

# --- /users komandasi ---
@dp.message(F.text == "/users")
async def get_users(message: Message):
    con = sqlite3.connect("bot/database.db")
    cur = con.cursor()
    cur.execute("SELECT full_name, username FROM users")
    users = cur.fetchall()
    con.close()

    if users:
        text = "👥 Foydalanuvchilar ro‘yxati:\n\n"
        for u in users:
            text += f"👤 {u[0]} (@{u[1]})\n"
    else:
        text = "Hozircha foydalanuvchilar yo‘q 😅"
    
    await message.answer(text)

# --- Botni ishga tushirish ---
async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot iishga tushdi !")
    asyncio.run(main())
