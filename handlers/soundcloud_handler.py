import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from telebot import TeleBot
from urllib.parse import urlparse

# Ініціалізація пулу потоків для обробки кількох запитів одночасно
executor = ThreadPoolExecutor(max_workers=5)  # Кількість одночасних запитів

def register_handlers(bot):
    @bot.message_handler(func=lambda message: "soundcloud.com" in message.text)
    def handle_message(message):
        # Виклик асинхронної обробки запиту
        executor.submit(handle_soundcloud_message, bot, message)

def is_playlist_url(url):
    """Перевірка, чи URL є плейлистом SoundCloud."""
    parsed_url = urlparse(url)
    return '/sets/' in parsed_url.path

def handle_soundcloud_message(bot, message):
    url = message.text.strip()

    if is_playlist_url(url):
        download_message = bot.reply_to(message, "Завантаження плейлиста з SoundCloud розпочато. Це може зайняти деякий час залежно від кількості треків у плейлисті.")
    else:
        download_message = bot.reply_to(message, "Завантаження треку з SoundCloud розпочато. Це може зайняти деякий час.")

    # Створення унікальної папки для кожного користувача
    user_folder = f'downloads/{message.from_user.id}'
    os.makedirs(user_folder, exist_ok=True)

    try:
        # Завантаження треків або плейлистів
        process = subprocess.Popen([
            'yt-dlp',
            '-x',
            '--audio-format', 'mp3',
            '--audio-quality', '320K',
            '--output', f'{user_folder}/%(title)s.%(ext)s',
            url
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            bot.reply_to(message, f"Помилка завантаження: {stderr.decode('utf-8')}")
            return

        files = os.listdir(user_folder)
        if files:
            for file in files:
                file_path = os.path.join(user_folder, file)
                with open(file_path, 'rb') as f:
                    if is_playlist_url(url):
                        # Для плейлистів використовується метод send_audio з caption
                        playlist_id = url.split('/')[-1].split('?')[0]  # Витягуємо ID плейлиста
                        bot.send_audio(
                            message.chat.id,
                            f,
                            title=os.path.splitext(file)[0],
                            caption=f"#playlist_{playlist_id}"
                        )
                    else:
                        # Для окремих треків використовується метод reply_to без caption
                        bot.send_audio(
                            message.chat.id,
                            f,
                            title=os.path.splitext(file)[0],
                            reply_to_message_id=message.message_id
                        )

            bot.delete_message(message.chat.id, download_message.message_id)

            # Очистка файлів і папки
            for file in files:
                os.remove(os.path.join(user_folder, file))
            
            os.rmdir(user_folder)

        else:
            bot.reply_to(message, "Не вдалося завантажити музику. Спробуйте ще раз.")

    except Exception as e:
        bot.reply_to(message, f"Сталася помилка: {str(e)}")
