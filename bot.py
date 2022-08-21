from telegram.ext import Updater, CommandHandler
import os, requests

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I respond to /weather and /currency. Try these!')

def get_single_song(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    username = update.message.chat.username
    # logging.log(logging.INFO, f'start to query message {message_id} in chat:{chat_id} from {username}')

    # url = "'" + update.effective_message.text + "'"
    url = "'" + 'https://open.spotify.com/track/2XU0oxnq2qxCpomAAuJY8K' + "'"

    os.system(f'mkdir -p temp{message_id}_{chat_id}')
    os.chdir(f'./temp{message_id}_{chat_id}')

    # logging.log(logging.INFO, f'start downloading')
    bot.send_message(chat_id=chat_id, text="Fetching...")

    os.system(f'spotdl -f ../ffmpeg/ffmpeg query={url}')
    # logging.log(logging.ERROR, 'you should select one of downloaders')

    # logging.log(logging.INFO, 'sending to client')
    try:
        sent = 0 
        bot.send_message(chat_id=chat_id, text="Sending to You...")
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if os.path.splitext(f)[1] == '.mp3']
        for file in files:
            bot.send_audio(chat_id=chat_id, audio=open(f'./{file}', 'rb'), timeout=1000)
            sent += 1
    except:
        pass

    os.chdir('./..')
    os.system(f'rm -rf temp{message_id}_{chat_id}')

    if sent == 0:
       bot.send_message(chat_id=chat_id, text="It seems there was a problem in finding/sending the song.")
       raise Exception("dl Failed")
    # else:
        # logging.log(logging.INFO, 'sent')



def main():
    TOKEN = "5644770465:AAFYwX31K1QAXWrIzcGKPpVl0nhvaaLgC_U"
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start',start)
    gg_handler = CommandHandler('gg',get_single_song)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(gg_handler)

    updater.start_polling()
    # PORT = int(os.environ.get('PORT', '443'))
    # HOOK_URL = 'YOUR-CODECAPSULES-URL-HERE' + '/' + TOKEN
    # updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url=HOOK_URL)
    # updater.idle()

if __name__ == '__main__':
    main()
