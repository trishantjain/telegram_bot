import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
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
ADDRESS, PHONE = range(2)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    update.message.reply_text('Hi!')
    return ADDRESS


# def help(update, context):
#     update.message.reply_text('''
#         /profile - Profile of our business.
# /freshners - list of room freshners.
#        ''')


# def freshners(update, context):
#     update.message.reply_text('''
#         1. Bonanza
# 2. Lemon
# 3. Grapes
#     ''')


# def order(update: Update, context):
#     user_id = update.message.from_user.id
#     context.user_data[user_id] = {}
#     context.user_data[user_id]['order_list'] = None

#     update.message.reply_text('''Please give order with name and its quantity.
# Name of room freshner - Quantity
# Address
# Phone Numbner

# Start your order with below line
# "Order Placement"
#     ''')


def set_address(update, context):
    address = update.message.text
    context.user_data['address'] = address
    update.message.reply_text("Address set as: " + address)
    return PHONE


def set_phone(update, context):
    update.message.reply_text("Please enter your phone number: ")
    phone = update.message.text
    context.user_data['phone'] = phone
    update.message.reply_text("PHone set as: " + phone)
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Command canceled.')
    return ConversationHandler.END


def echo(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_input = update.message.text

    if "how are you" in user_input.lower():
        update.message.reply_text(
            f"I am fine {user_name}. How can I help you?")

    elif any(word in user_input.lower() for word in ["hi", "hii", "hello"]):
        update.message.reply_text(
            f"Hii {user_name}. Welcome to Royale Freshners Bot.")

    elif "order placement" in user_input.lower():
        context.user_data[user_id]['order_list'] = user_input
        update.message.reply_text("Give your address")

    elif "address" in user_input.lower():
        context.user_data[user_id]['address'] = user_input
        update.message.reply_text("Give your phone number")

    elif context.user_data[user_id]['order_list'] is not None and 'address' in context.user_data[user_id] and 'phone_number' not in context.user_data[user_id]:
        context.user_data[user_id]['phone_number'] = user_input

        record = {
            "title": user_name,
            "description": context.user_data[user_id]['order_list'],
            "address": context.user_data[user_id]['address'],
            "phone_number": context.user_data[user_id]['phone_number']
        }
        mycollection.insert_one(record)

        update.message.reply_text(
            "Thanks for placing your order. We will contact you soon.")

        # Clear user data
        context.user_data[user_id] = {}


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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('address', start)],
        states={
            ADDRESS: [MessageHandler(Filters.text, set_address)],
            PHONE: [MessageHandler(Filters.text, set_phone)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
