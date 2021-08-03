
import logging

import telebot
import os

import pdf2image
# Read  Bot Token From File

with open("key1.txt", "r") as key:
    token = key.read().strip()
API_TOKEN = token

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(func=lambda msg: True)
def get_msgs(msg):
    name = msg.chat.first_name
    lastname = msg.chat.last_name
    chat_id = msg.chat.id

    if msg.text == '/start':
        bot.send_message(
            msg.chat.id, u'به ربات تبدیل pdf خوش امدید  \n فایل خود را ارسال کنید')
        bot.register_next_step_handler(msg, handle_docs)

# Handles all sent documents and audio files


@bot.message_handler(content_types=['document'])
def handle_docs(msg):

    print(msg.chat.first_name)
    print(msg.document.file_name)
    print( bot.get_file(msg.document.file_id))
    try:
        # get file from user and download it
        pdf = bot.get_file(msg.document.file_id)

        downloaded_file = bot.download_file(pdf.file_path)

        with open('botpdf.pdf', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(msg.chat.id, 'Download completed!')

        # convert it to jpg
        print('here')
        print("document", msg.document)
        
        os.mkdir('./{0}'.format(msg.document.file_unique_id),mode = 0o777, dir_fd = None)
        print('path: ',os.path.dirname(__file__) + './{0}'.format(msg.document.file_unique_id))
        pdf2image.convert_from_path(
            pdf_path='botpdf.pdf', output_folder='./{0}'.format(msg.document.file_unique_id), fmt='ppm')
        print('here2')

        x = 0
        photo_dir = os.path.dirname(__file__) + './{0}'.format(msg.document.file_unique_id)
        extension = ".ppm"
        for i in os.listdir(photo_dir):
            if i.endswith(extension):
                os.rename(photo_dir + i, photo_dir + str(x) + extension)
                x += 1

        bot.send_message(msg.chat.id, u'Done! 2')
    except Exception as e:
        print(e)
        bot.send_message(msg.chat.id, u'Error',)



#########
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=False, interval=0)

