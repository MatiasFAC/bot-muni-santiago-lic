from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Define a function that will be called when the bot receives a message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Respond with "version 2" to the user
    await update.message.reply_text("version 2")

def main():
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = Application.builder().token('5866543315:AAG545cq0uVoQcIwXEb7svDmxCKNG--kbaI').build()

    # Create a message handler that will handle all text messages
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # Add the message handler to the application
    application.add_handler(echo_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
