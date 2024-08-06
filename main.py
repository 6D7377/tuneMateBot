import telebot
from dotenv import load_dotenv
import os
from handlers import start_handler, help_handler, admin_handler, user_handler, spotify_handler, youtube_handler, soundcloud_handler
from handlers.message_filter_handler import register_handlers as register_filter_handlers
from database.db_utils import init_db
from utils.admin_utils import is_admin

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# Ініціалізуємо базу даних
init_db()

# Реєструємо хендлери
start_handler.register_handlers(bot)
help_handler.register_handlers(bot)
admin_handler.register_handlers(bot)
user_handler.register_handlers(bot)
spotify_handler.register_handlers(bot)
soundcloud_handler.register_handlers(bot)

# Реєструємо хендлер для фільтрації повідомлень
register_filter_handlers(bot)

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if is_admin(message.from_user.id):
        bot.reply_to(message, "Hello, Admin!")
    else:
        bot.reply_to(message, "You are not an admin.")

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True, allowed_updates=['message', 'edited_message', 'channel_post', 'edited_channel_post', 'inline_query', 'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query', 'poll', 'poll_answer'])
