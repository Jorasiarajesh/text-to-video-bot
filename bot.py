from telegram.ext import Updater, MessageHandler, Filters
from telegram import InputFile
from moviepy.editor import TextClip
import os

import logging
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def text_to_video(text, filename='output.mp4'):
    clip = TextClip(text, fontsize=50, color='white', size=(720, 1280), bg_color='black', method='caption')
    clip = clip.set_duration(5)
    clip.write_videofile(filename, fps=24)
    return filename

def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    video_path = text_to_video(text)
    with open(video_path, 'rb') as video:
        context.bot.send_video(chat_id=chat_id, video=InputFile(video))
    os.remove(video_path)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
