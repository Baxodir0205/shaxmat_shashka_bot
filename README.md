♟️ Shaxmat & Shashka Telegram WebApp Bot

Telegram uchun yaratilgan Shashka (Checkers) va Shaxmat (Chess) o‘yin bot.
Bot Telegram WebApp texnologiyasi orqali ishlaydi va foydalanuvchilarga AI bilan o‘ynash imkonini beradi.

🚀 Loyiha haqida

Bu loyiha:

Telegram bot backend (Python)

SQLite ma’lumotlar bazasi

Telegram WebApp integratsiyasi

Shashka va Shaxmat o‘yin interfeysi (HTML/JS frontend)

Bot foydalanuvchini ro‘yxatdan o‘tkazadi, faoliyatini saqlaydi va WebApp orqali o‘yinni ishga tushiradi.

🧠 Asosiy imkoniyatlar

👑 Shashka o‘yini

♟️ Shaxmat o‘yini

🤖 AI bilan o‘ynash

👤 Foydalanuvchini avtomatik ro‘yxatdan o‘tkazish

📊 SQLite database orqali user saqlash

🔑 Admin panel (foydalanuvchilar ro‘yxatini ko‘rish)

🔐 WebApp uchun maxsus hash generatsiyasi

🏗 Backend Texnologiyalar

Python 3.10+

python-telegram-bot

SQLite3

Hashlib (WebApp validation uchun)

Logging

📂 Loyiha strukturasi
shaxmat_shashka_bot/
│
├── main.py
├── bot_data.db
├── requirements.txt
├── README.md
├── index.html
├── chess.html
⚙️ O‘rnatish va ishga tushirish
1️⃣ Repository’ni klon qilish
git clone https://github.com/USERNAME/shaxmat_shashka_bot.git
cd shaxmat_shashka_bot
2️⃣ Virtual muhit yaratish
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
3️⃣ Kerakli kutubxonalarni o‘rnatish
pip install -r requirements.txt
4️⃣ Token va sozlamalarni o‘rnatish

main.py ichida quyidagilarni o‘zgartiring:

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WEB_APP_BASE_URL = "YOUR_WEBAPP_URL"
ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"
5️⃣ Botni ishga tushirish
python main.py

Bot polling rejimida ishlaydi.

🔐 Admin Panel

Bot ichida /admin komandasi orqali admin panelga kirish mumkin.

Admin imkoniyatlari:

Jami foydalanuvchilar sonini ko‘rish

Ro‘yxatdan o‘tgan userlar ro‘yxatini ko‘rish
