import os
import subprocess
from telebot import TeleBot
from mutagen.easyid3 import EasyID3
import re

def register_handlers(bot):
    @bot.message_handler(func=lambda message: "spotify.com" in message.text)
    def handle_message(message):
        url = message.text.strip()

        # Перевірка, чи є URL валідним
        if not url.startswith("https://"):
            bot.reply_to(message, "Будь ласка, надайте дійсне посилання на трек, плейлист або альбом Spotify.")
            return

        # Перевірка, чи це посилання на Spotify трек, плейлист або альбом
        if not any(substring in url for substring in ["spotify.com/track", "spotify.com/playlist", "spotify.com/album"]):
            bot.reply_to(message, "Це не посилання на трек, плейлист або альбом Spotify. Будь ласка, надайте відповідне посилання.")
            return

        # Відправка повідомлення про початок завантаження
        if "spotify.com/playlist" in url or "spotify.com/album" in url:
            download_message = bot.reply_to(message, "Завантаження плейлиста або альбому з Spotify розпочато. Це може зайняти деякий час залежно від його розміру.")
        else:
            download_message = bot.reply_to(message, "Завантаження треку з Spotify розпочато. Це може зайняти деякий час.")

        # Створення унікальної папки для кожного користувача
        user_folder = f'downloads/{message.from_user.id}'
        os.makedirs(user_folder, exist_ok=True)

        # Запуск spotdl для завантаження з параметрами якості
        try:
            process = subprocess.Popen(['spotdl', url, '--output', user_folder, '--bitrate', '320k'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Перевірка на помилки
            if process.returncode != 0:
                bot.reply_to(message, f"Помилка завантаження: {stderr.decode('utf-8')}")
                return

            # Перевірка наявності завантажених файлів
            files = os.listdir(user_folder)
            if files:
                playlist_or_album_name = None
                if "spotify.com/playlist" in url or "spotify.com/album" in url:
                    playlist_or_album_name = get_playlist_or_album_name(url)

                for file in files:
                    file_path = os.path.join(user_folder, file)
                    title, artist = get_track_info(file_path)

                    description = f"#{playlist_or_album_name}" if playlist_or_album_name else ""

                    with open(file_path, 'rb') as f:
                        if playlist_or_album_name:
                            bot.send_audio(
                                message.chat.id,
                                f,
                                title=title,
                                performer=artist,
                                caption=description
                            )
                        else:
                            bot.send_audio(
                                message.chat.id,
                                f,
                                title=title,
                                performer=artist,
                                reply_to_message_id=message.message_id
                            )

                bot.delete_message(message.chat.id, download_message.message_id)

                for file in files:
                    os.remove(os.path.join(user_folder, file))
                
                os.rmdir(user_folder)

            else:
                bot.reply_to(message, "Не вдалося завантажити музику. Спробуйте ще раз.")
        except Exception as e:
            bot.reply_to(message, f"Сталася помилка: {str(e)}")

def get_track_info(file_path):
    try:
        audio = EasyID3(file_path)
        title = audio.get('title', ['Unknown'])[0]
        artist = audio.get('artist', ['Unknown'])[0]
    except Exception as e:
        title = "Unknown Title"
        artist = "Unknown Artist"
    
    return title, artist

def get_playlist_or_album_name(url):
    match = re.search(r'playlist/([^?]+)', url)
    if match:
        playlist_id = match.group(1)
        return f"Playlist_{playlist_id}"
    match = re.search(r'album/([^?]+)', url)
    if match:
        album_id = match.group(1)
        return f"Album_{album_id}"
    return "Unknown_Playlist_or_Album"

# Для імпортування handle_spotify_message в message_filter_handler.py
def handle_spotify_message(message):
    handle_message(message)
