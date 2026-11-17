try:
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
except ImportError:
    Updater = CommandHandler = MessageHandler = Filters = None

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

WELCOME_MESSAGE = "Hello! I'm your Telegram bot. How can I assist you?"


def build_welcome_message(user_name=None):
    """
    Build welcome message text for the start command.
    Extracted helper simplifying the message construction responsibility in `start`.
    """
    if user_name:
        return f"Hello {user_name}! I'm your Telegram bot. How can I assist you?"
    return WELCOME_MESSAGE


# Define the function for the /start command
def start(update, context=None):
    """
    Handles /start command.
    Preconditions:
      - Line 25: user_name extracted safely from update if available.
      - Line 26: message = build_welcome_message(user_name).
      - Line 27: update.message.reply_text(message) dispatched.
    """
    user_name = None
    if update and hasattr(update, "effective_user") and update.effective_user:
        user_name = getattr(update.effective_user, "first_name", None)
    message = build_welcome_message(user_name)
    if update and hasattr(update, "message") and update.message:
        return update.message.reply_text(message)
    return message


# Define the function to respond to user messages
def reply_to_message(update, context):
    user_message = update.message.text
    response = f"You said: {user_message}"
    update.message.reply_text(response)


def main():
    if Updater is None:
        print("python-telegram-bot is required to run the bot.")
        return
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Create a handler for the /start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Create a handler for user messages
    message_handler = MessageHandler(Filters.text & ~Filters.command, reply_to_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

