import logging
import time
import hashlib
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode


BOT_TOKEN = "TOKENINGNI_BU_YERGA_QOY"
WEB_APP_BASE_URL = "https://baxodir0205.github.io/shaxmat_shashka_bot"
ADMIN_PASSWORD = "0205"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_name="bot_data.db"):
        self.db_name = db_name
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    checkers_games INTEGER DEFAULT 0,
                    chess_games INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    registered_at REAL,
                    last_active REAL
                )
            ''')
            conn.commit()

    def add_user(self, user_id, username, first_name):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO users (id, username, first_name, registered_at, last_active)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, username or first_name, first_name, time.time(), time.time()))
                conn.commit()
                return True
        return False

    def update_activity(self, user_id):
        with self._get_connection() as conn:
            conn.execute("UPDATE users SET last_active = ? WHERE id = ?", (time.time(), user_id))
            conn.commit()

    def get_all_users(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return [dict(row) for row in cursor.fetchall()]


db = Database()


def generate_webapp_hash(user_id):
    return hashlib.md5(f"{user_id}{BOT_TOKEN}".encode()).hexdigest()[:16]


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 Admin panel. Parolni kiriting:")
    context.user_data['awaiting_admin_password'] = True


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_admin_password'):
        if update.message.text == ADMIN_PASSWORD:
            context.user_data['awaiting_admin_password'] = False
            users = db.get_all_users()
            count = len(users)

            response = f"✅ Admin Panel\n\nJami foydalanuvchilar: {count} ta\n\n"

            for u in users:
                reg_date = time.strftime("%Y-%m-%d", time.localtime(u['registered_at']))
                response += f"{u['first_name']} (@{u['username']})\n"
                response += f"ID: {u['id']} | Ro'yxatdan o'tgan: {reg_date}\n\n"

            await update.message.reply_text(response)
        else:
            await update.message.reply_text("❌ Parol noto'g'ri.")
        return


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)
    db.update_activity(user.id)

    keyboard = [
        [InlineKeyboardButton("👑 SHASHKA O'YNASH", callback_data="play_checkers")],
        [InlineKeyboardButton("♟️ SHAXMAT O'YNASH", callback_data="play_chess")],
        [InlineKeyboardButton("ℹ️ YORDAM", callback_data="help")]
    ]

    await update.message.reply_text(
        f"👑 Shaxmat Shashka ONLINE BOT\n\n"
        f"Xush kelibsiz, {user.first_name}!\n\n"
        f"O'yinni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    hash_code = generate_webapp_hash(user.id)

    if query.data == "play_checkers":
        url = f"{WEB_APP_BASE_URL}/index.html?user={user.id}&name={user.first_name}&game=checkers&mode=ai&hash={hash_code}"
        keyboard = [
            [InlineKeyboardButton("👑 SHASHKANI BOSHLASH", web_app=WebAppInfo(url=url))],
            [InlineKeyboardButton("🔙 ORQAGA", callback_data="back_to_main")]
        ]
        await query.edit_message_text(
            "SHASHKA O'YNASH\n\nAI bilan o'ynash uchun bosing:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "play_chess":
        url = f"{WEB_APP_BASE_URL}/chess.html?user={user.id}&name={user.first_name}&game=chess&mode=ai&hash={hash_code}"
        keyboard = [
            [InlineKeyboardButton("♟️ SHAXMATNI BOSHLASH", web_app=WebAppInfo(url=url))],
            [InlineKeyboardButton("🔙 ORQAGA", callback_data="back_to_main")]
        ]
        await query.edit_message_text(
            "SHAXMAT O'YNASH\n\nAI bilan o'ynash uchun bosing:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "help":
        help_text = (
            "BOT QANDAY ISHLAYDI?\n\n"
            "• SHASHKA o'ynash mumkin\n"
            "• SHAXMAT o'ynash mumkin\n"
            "• AI bilan o'ynaysiz\n\n"
            "O'yinni boshlash uchun kerakli tugmani bosing.\n"
            "O'yin Telegram WebApp orqali ishlaydi."
        )

        keyboard = [
            [InlineKeyboardButton("🔙 ORQAGA", callback_data="back_to_main")]
        ]

        await query.edit_message_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "back_to_main":
        keyboard = [
            [InlineKeyboardButton("👑 SHASHKA O'YNASH", callback_data="play_checkers")],
            [InlineKeyboardButton("♟️ SHAXMAT O'YNASH", callback_data="play_chess")],
            [InlineKeyboardButton("ℹ️ YORDAM", callback_data="help")]
        ]

        await query.edit_message_text(
            "Shaxmat Shashka ONLINE BOT\n\nO'yinni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()