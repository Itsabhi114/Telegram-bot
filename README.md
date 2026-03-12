import telebot
from telebot import types
import random

TOKEN = "8626952361:AAFeEkhS4vrk6Dro7A5ZfbYGynQFv4LwtMk"

bot = telebot.TeleBot(TOKEN)

# verification channel
ADMIN_CHANNEL = "@backup897"

# team link
TEAM_LINK = "https://t.me/botchat876"

user_data = {}


# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):

    name = message.from_user.first_name

    text = f"Hello {name} 👋\n\nWelcome to our bot.\n\nPlease choose an option."

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = "📖 Stories"
    btn2 = "🧠 General Knowledge"
    btn3 = "🖼 Verification"
    btn4 = "💬 Team se baat karein"

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(message.chat.id, text, reply_markup=markup)


# TEAM CHAT
@bot.message_handler(func=lambda m: m.text == "💬 Team se baat karein")
def team(message):

    bot.send_message(
        message.chat.id,
        f"Team se baat karne ke liye yahan join karein:\n{TEAM_LINK}"
    )


# GENERAL KNOWLEDGE
gk_list = [
    "India ka national animal Tiger hai.",
    "Sun ek star hai.",
    "Water ka formula H2O hai.",
    "Earth sun ke around ghoomti hai.",
    "Light ki speed approx 3 lakh km/s hai."
]


@bot.message_handler(func=lambda m: m.text == "🧠 General Knowledge")
def gk(message):

    fact = random.choice(gk_list)

    bot.send_message(message.chat.id, f"🧠 GK Fact:\n\n{fact}")


# STORIES
stories = [
    "Ek ladka jungle me gaya aur use ek purana khazana mil gaya...",
    "Ek funny incident hua jab ek bandar ne mobile chura liya...",
    "Ek romantic kahani jahan do log train me mile..."
]


@bot.message_handler(func=lambda m: m.text == "📖 Stories")
def story(message):

    s = random.choice(stories)

    bot.send_message(message.chat.id, f"📖 Story:\n\n{s}")


# VERIFICATION START
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


# RECEIVE PHONE
@bot.message_handler(content_types=['contact'])
def get_contact(message):

    phone = message.contact.phone_number

    user_data[message.chat.id] = phone

    bot.send_message(
        message.chat.id,
        "Ab verification ke liye ek selfie photo bheje."
    )


# RECEIVE PHOTO
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


bot.infinity_polling()
