from musicDownloader.spotify import handle_spotify_message
from musicDownloader.youtube import handle_youtube_message
from musicDownloader.soundcloud import handle_soundcloud_message

def is_valid_url(url):
    return url.startswith("https://")

def register_handlers(bot):
    @bot.message_handler(commands=['start', 'help', 'other_commands'])  # Додайте інші команди, які підтримуються ботом
    def handle_commands(message):
        # Команди обробляються окремо
        pass

    @bot.message_handler(content_types=['text'])
    def filter_messages(message):
        if is_valid_url(message.text):
            if "spotify.com" in message.text:
                handle_spotify_message(bot, message)
            elif "youtube.com" in message.text or "youtu.be" in message.text:
                handle_youtube_message(bot, message)
            elif "soundcloud.com" in message.text:
                handle_soundcloud_message(bot, message)
            else:
                bot.reply_to(message, "Посилання не підтримується. Підтримувані платформи: YouTube, Spotify, SoundCloud.")
        else:
            bot.reply_to(message, "Будь ласка, надішліть правильне посилання. Підтримувані платформи: YouTube, Spotify, SoundCloud.")
