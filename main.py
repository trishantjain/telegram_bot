import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pymongo import MongoClient
from telegram import Update


client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
myDatabase = client["Order_list"]
mycollection = myDatabase["royale"]


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
token = "6258989185:AAEzPzeOPue371Qbbsz15MHSDTlSfuM0WUI"
freshner_list = ["Bonanza", "Lemon", "Grapes", "Mint"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('''
        /profile - Profile of our business.
/freshners - list of room freshners.     
       ''')


def freshners(update, context):
    update.message.reply_text('''
        1. Bonanza
2. Lemon
3. Grapes    
    ''')


def order(update: Update, context):
    update.message.reply_text('''Please give order with name and its quantity.
Name of room freshner - Quantity
Address
Phone Numbner

Start your order with below line
"Order Placement"
    ''')


def echo(update, context):
    user_name = update.message.from_user.first_name
    user_input = update.message.text

    if "how are you" in user_input.lower():
        update.message.reply_text(
            f"I am fine {user_name}. How can I help you?")

    elif ("hi" or "hii" or "hello") in user_input.lower():
        update.message.reply_text(
            f"Hii {user_name}. Welcome to Royale Freshners Bot.")

    elif ("order placement") in user_input.lower():
        order_list = user_input
        record = {
            "title": user_name,
            "description": order_list,
            # "address:":,
            "viewers": 104
        }
        myDatabase.royale.insert_one(record)
        update.message.reply_text("Give Your address")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("freshners", freshners))
    dp.add_handler(CommandHandler("order", order))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
