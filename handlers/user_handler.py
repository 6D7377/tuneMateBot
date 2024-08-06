import os
from dotenv import load_dotenv
from telebot import TeleBot

# Завантаження змінних середовища з .env файлу
load_dotenv()

# Зчитування ADMIN_GROUP_ID з .env
admin_group_id = int(os.getenv('ADMIN_GROUP_ID'))

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['message'])
    def handle_user_message(message):
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_username = message.from_user.username or ""
        user_message = message.text[len('/message '):].strip()
        
        if not user_message:
            bot.reply_to(message, "Будь ласка, вкажіть повідомлення для відправки адміністратору, цей рядок не може бути порожнім.")
            return

        # Генерація унікального ID для повідомлення
        unique_id = f"{user_id}-{message.message_id}"

        # Пересилаємо повідомлення адміністраторам
        bot.send_message(
            admin_group_id, 
            f"Message ID: {unique_id}\n"
            f"First Name: {user_first_name}\n"
            f"Username: @{user_username}\n"
            f"Message: {user_message}\n\n"
            "Reply in the group chat with the command:\n"
            f"/reply {unique_id} <your response>"
        )
        bot.reply_to(message, "Ваше повідомлення надіслано адміністратору. Він дасть вам відповідь найближчим часом.")

    @bot.message_handler(commands=['reply'])
    def handle_admin_reply(message):
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            bot.reply_to(message, "Usage: /reply <unique_id> <response>")
            return
        
        unique_id = parts[1]
        admin_reply = parts[2].strip()
        if not admin_reply:
            bot.reply_to(message, "Будь ласка, надайте відповідь користувачу.")
            return
        
        # Розбираємо унікальний ID
        user_id = unique_id.split('-')[0]

        # Надсилаємо відповідь користувачеві
        bot.send_message(
            user_id, 
            f"Відповідь адміна:\n \n{admin_reply}"
        )
        bot.reply_to(message, "Відповідь надіслано.")
