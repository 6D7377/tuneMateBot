from database.db_utils import add_user, user_exists

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        if not user_exists(user_id):
            add_user(user_id, username, first_name, last_name)
        
        welcome_message = (
            "Привіт! Це бот для завантаження музики. Підтримувані платформи:\n"
            "- YouTube\n"
            "- Spotify\n"
            "- SoundCloud\n\n"
            "Просто надішліть посилання на трек або плейлист, і бот завантажить його для вас."
        )
        
        bot.reply_to(message, welcome_message)
