import io
import os
import sys
import json
import logging
import zipfile
import argparse
from PIL import Image
from progress.bar import Bar
from telegram.bot import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler

# parse command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('--token', action='store', help='telegram bot access token.')
parser.add_argument('--url', action='store', help='telegram bot api url.')
parser.add_argument('--fileurl', action='store', help='telegram bot file api url.')
args = parser.parse_args()
if args.token == None:
    parser.print_help()
    sys.exit(0)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create a telegram bot instance
bot = Bot(args.token, args.url, args.fileurl)

def zip_handler(bot, update):
    ''' handle bot /zip command.
    '''
    try:
        message = update.message
        if message.reply_to_message == None:
            return
        sticker = message.reply_to_message.sticker
        if sticker == None:
            return
        filename = sticker.set_name + '.zip'
        sticker_set = bot.get_sticker_set(sticker.set_name)
        files, emojidict = download_stickers(sticker.set_name, sticker_set.stickers)
        files = convert_webp_to_png(sticker.set_name, files)
        data = create_compressed_file(sticker.set_name, files, emojidict)
        bot.send_document(message.chat.id, data, filename=filename, reply_to_message_id=message.message_id)
    except Exception as e:
        logging.warn('%s', str(e))

def download_stickers(set_name, stickers):
    ''' download sticker set all files.
    '''
    files = []
    emojidict = {}
    bar = Bar('Download {0}'.format(set_name), max=len(stickers))
    for sticker in stickers:
        buffer = io.BytesIO()
        file = bot.get_file(sticker.file_id)
        filename = os.path.basename(file.file_path)
        _basename, ext = os.path.splitext(filename)
        if ext == '':
            filename = filename + '.webp'
        if not sticker.emoji == None:
            array = []
            for emoji in sticker.emoji:
                array.append(emoji)
            emojidict[filename] = array
        file.download(out=buffer)
        files.append((filename, buffer))
        bar.next()
    bar.finish()
    return files, emojidict

def convert_webp_to_png(set_name, files):
    ''' convert .webp format image to .png format.
    '''
    newfiles = []
    bar = Bar('Convert {0} file format'.format(set_name), max=len(files))
    for file in files:
        bar.next()
        buffer = io.BytesIO()
        filename, fileio = file
        basename, _ext = os.path.splitext(filename)
        image = Image.open(fileio)
        image.save(buffer, 'png', quality=100)
        newfiles.append((basename + '.png', buffer))
    bar.finish()
    return newfiles

def create_compressed_file(set_name, files, emojidict):
    ''' create stickerset into a compressed file.
    '''
    buffer = io.BytesIO()
    bar = Bar('Compress {0}'.format(set_name), max=len(files))
    handle = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        bar.next()
        filename, fileio = file
        handle.writestr(filename, fileio.getvalue())
    handle.writestr('emoji.json', json.dumps(emojidict))
    handle.close()
    buffer.seek(0)
    bar.finish()
    return buffer

def main():
    updater = Updater(bot=bot)
    updater.dispatcher.add_handler(CommandHandler('zip', zip_handler))
    updater.start_polling()
    logging.info('getstickerset bot start working.')
    updater.idle()

if __name__ == '__main__':
    main()
