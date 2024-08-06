from telebot import TeleBot
from utils.admin_utils import is_admin
from database.db_utils import get_all_users

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['forallusers'])
    def send_message_to_all_users(message):
        if is_admin(message.from_user.id):
            text = message.text[len('/forallusers '):].strip()
            if not text:
                bot.reply_to(message, "Будь ласка, вкажіть повідомлення для відправки.")
                return
            users = get_all_users()
            notification = (
                "Системне повідомлення від адміністратора:\n"
                "-----------------------------------------\n"
                f"{text}\n"
                "-----------------------------------------\n"
                "Будь ласка, не відповідайте на це повідомлення, оскільки адміністратор не побачить вашої відповіді. (/help)"
            )
            for user_id in users:
                bot.send_message(user_id, notification)
            bot.reply_to(message, "Повідомлення надіслано всім користувачам.")
        else:
            bot.reply_to(message, "Ви не адмін.")
