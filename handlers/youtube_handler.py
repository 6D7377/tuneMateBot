import os
import subprocess
import re
from telebot import TeleBot
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)  # Кількість одночасних запитів

def register_handlers(bot):
    @bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
    def handle_message(message):
        # Виклик асинхронної обробки запиту
        executor.submit(handle_youtube_message, bot, message)

def handle_youtube_message(bot, message):
    url = message.text.strip()

    # Перевірка, чи є URL валідним
    if not url.startswith("https://"):
        bot.reply_to(message, "Будь ласка, надайте дійсне посилання з YouTube.")
        return

    # Відправка повідомлення про початок завантаження
    if "playlist" in url:
        download_message = bot.reply_to(message, "Завантаження плейлиста з YouTube розпочато. Це може зайняти деякий час залежно від його розміру та кількості треків.")
    else:
        download_message = bot.reply_to(message, "Завантаження треку з YouTube розпочато. Це може зайняти деякий час.")

    # Створення унікальної папки для кожного користувача
    user_folder = f'downloads/{message.from_user.id}'
    os.makedirs(user_folder, exist_ok=True)

    # Отримання ідентифікатора плейлиста або альбому
    playlist_id = get_playlist_or_album_id(url) if "playlist" in url or "album" in url else None

    try:
        # Запуск yt-dlp для завантаження аудіо з параметрами якості
        process = subprocess.Popen([
            'yt-dlp', 
            '-x',  # Завантажити тільки аудіо
            '--audio-format', 'mp3',  # Формат аудіо
            '--audio-quality', '320K',  # Якість аудіо
            '--output', f'{user_folder}/%(title)s.%(ext)s',  # Шлях до збереження
            url
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Перевірка на помилки
        if process.returncode != 0:
            bot.reply_to(message, f"Помилка завантаження: {stderr.decode('utf-8')}")
            return

        # Перевірка наявності завантажених файлів
        files = os.listdir(user_folder)
        if files:
            for file in files:
                file_path = os.path.join(user_folder, file)

                # Видалення розширення .mp3 з назви
                title = os.path.splitext(file)[0]

                # Підпис для плейлиста або альбому
                caption = f"#playlist_{sanitize_id(playlist_id)}" if playlist_id else ""

                # Надсилаємо файл як аудіо з описом для плейлиста або альбому
                with open(file_path, 'rb') as f:
                    if playlist_id:
                        bot.send_audio(
                            message.chat.id,
                            f,
                            title=title,
                            caption=caption
                        )
                    else:
                        bot.send_audio(
                            message.chat.id,
                            f,
                            title=title,
                            reply_to_message_id=message.message_id
                        )

            bot.delete_message(message.chat.id, download_message.message_id)
        else:
            bot.reply_to(message, "Не вдалося завантажити музику. Спробуйте ще раз.")
    except Exception as e:
        bot.reply_to(message, f"Сталася помилка: {str(e)}")
    finally:
        # Видалення завантажених файлів та папки
        for file in os.listdir(user_folder):
            os.remove(os.path.join(user_folder, file))
        os.rmdir(user_folder)

def get_playlist_or_album_id(url):
    # Використання регулярних виразів для отримання ідентифікатора плейлиста або альбому
    match = re.search(r'(?:playlist|album)\?list=([^&]+)', url)
    if match:
        return match.group(1)
    return "Unknown"

def sanitize_id(playlist_id):
    # Видалення всіх небажаних символів з ідентифікатора плейлиста
    return re.sub(r'[^a-zA-Z0-9]', '', playlist_id)