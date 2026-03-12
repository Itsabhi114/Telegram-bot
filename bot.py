import telebot
from telebot import types
import random

TOKEN = "8662928183:AAGId-ZkRay6-UD8mhkEINojC4joLMshs7U"

bot = telebot.TeleBot(TOKEN)

# verification channel
ADMIN_CHANNEL = "@backup897"

# team chat link
TEAM_LINK = "https://t.me/botchat876"

user_data = {}

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):

    name = message.from_user.first_name

    text = f"""
Hello {name} 👋

Welcome to our bot.

Choose an option below:
"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = "📖 Stories"
    btn2 = "🧠 General Knowledge"
    btn3 = "🖼 Verification"
    btn4 = "💬 Team se baat karein"

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(message.chat.id, text, reply_markup=markup)

# ---------------- TEAM CHAT ----------------

@bot.message_handler(func=lambda m: m.text == "💬 Team se baat karein")
def team(message):

    bot.send_message(
        message.chat.id,
        f"Team se baat karne ke liye yahan join karein:\n{TEAM_LINK}"
    )

# ---------------- GENERAL KNOWLEDGE ----------------

gk_list = [

"India ka national animal Tiger hai.",
"Sun ek star hai.",
"Water ka formula H2O hai.",
"Earth sun ke around ghoomti hai.",
"Light ki speed approx 3 lakh km/s hai.",

"Mount Everest duniya ka sabse uncha pahad hai.",
"Human body me 206 bones hoti hain.",
"Computer ka brain CPU hota hai.",
"Shark machhliyon me sabse dangerous mani jati hai.",
"Jupiter solar system ka sabse bada planet hai."

]

@bot.message_handler(func=lambda m: m.text == "🧠 General Knowledge")
def gk(message):

    fact = random.choice(gk_list)

    bot.send_message(message.chat.id, f"🧠 GK Fact:\n\n{fact}")

# ---------------- STORIES ----------------

stories = [

"Ek ladka jungle me gaya aur use ek purana khazana mil gaya. Us khazane me sone ke sikke aur purane raaz chhupe the.",

"Ek bandar ne ek aadmi ka mobile chura liya aur ped par chadh gaya. Sab log hansne lage jab bandar selfie lene laga.",

"Ek train journey me do anjaan log mile aur dheere dheere unki dosti pyaar me badal gayi.",

"Ek gaon me raat ko ajeeb awaaz aati thi. Jab logon ne pata lagaya to ek purana khazana mila.",

"Ek chor ghar me ghusa lekin us ghar ka kutta uska dost ban gaya."

]

@bot.message_handler(func=lambda m: m.text == "📖 Stories")
def story(message):

    s = random.choice(stories)

    bot.send_message(message.chat.id, f"📖 Story:\n\n{s}")

# ---------------- VERIFICATION START ----------------

@bot.message_handler(func=lambda m: m.text == "🖼 Verification")
def verify_start(message):

    bot.send_message(
        message.chat.id,
        "Verification ke liye pehle apna phone number share karein.",
        reply_markup=contact_button()
    )

def contact_button():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    btn = types.KeyboardButton("📱 Phone number share karein", request_contact=True)

    markup.add(btn)

    return markup

# ---------------- RECEIVE PHONE ----------------

@bot.message_handler(content_types=['contact'])
def get_contact(message):

    phone = message.contact.phone_number

    user_data[message.chat.id] = phone

    bot.send_message(
        message.chat.id,
        "Ab verification ke liye ek selfie photo bheje."
    )

# ---------------- RECEIVE PHOTO ----------------

@bot.message_handler(content_types=['photo'])
def get_photo(message):

    file_id = message.photo[-1].file_id

    phone = user_data.get(message.chat.id, "unknown")

    caption = f"""
New Verification Request

Name: {message.from_user.first_name}
Username: @{message.from_user.username}
Phone: {phone}
User ID: {message.from_user.id}
"""

    bot.send_photo(
        ADMIN_CHANNEL,
        file_id,
        caption=caption
    )

    bot.send_message(
        message.chat.id,
        "✅ Verification request bhej diya gaya hai. Team jaldi check karegi."
    )

# ---------------- RUN BOT ----------------

bot.infinity_polling()
