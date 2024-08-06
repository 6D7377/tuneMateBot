from telebot import TeleBot




help_text = """
===============================
            Допомога
===============================

Для того, щоб надіслати повідомлення адміністрації використовуйте команду:

/message

Приклад:

/message Привіт, в мене проблема з завантаженням з Spotify
===============================
"""


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
