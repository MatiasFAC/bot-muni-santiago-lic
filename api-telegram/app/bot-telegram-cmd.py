from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
from loguru import logger
import os

env = os.environ.get("ENV", "prod")
env_token = os.environ.get("TOKEN", None)
env_users_file = os.environ.get("USERS_FILE", "/users/users.json")


def env_validations() -> None:
    logger.debug(f"env: {env}")
    
    if env not in ['prod', 'dev']:
        logger.error("Invalid ENV provided. env not set.")
        exit(1)

    if env_token is None:
        logger.error("Invalid TOKEN provided. TOKEN not set.")
        exit(1)

    if env_users_file is None:
        logger.error("Invalid USERS_FILE provided. USERS_FILE not set.")
        exit(1)


def loguro_config() -> None:
    if env == 'prod':
        logger.add("./log/{time:YYYY-MM-DD}.log", rotation="250 MB", level="WARNING")
    else:
        logger.add("./log/{time:YYYY-MM-DD}.log", rotation="250 MB", level="DEBUG")
    # logger.debug("This is a debug message")
    # logger.info("This is an info message")
    # logger.success("This is a success message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
'''
- Use /add to subscribe to notifications.
- Use /remove to cancel notifications.
'''
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    users = []
    user_json = { "id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name}

    # read from file
    try:
        with open(env_users_file, 'r') as f:
            users = json.load(f)
    except Exception as e:
        users = []

    # check if user already exists
    for u in users:
        if u['id'] == user.id:
            await update.message.reply_text(f"{user.first_name} {user.last_name} is already subscribed.")
            logger.info(f"{user.first_name} {user.last_name} is already subscribed.")
            return
        
    users.append(user_json)

    # write to file
    try:
        with open(env_users_file, 'w') as f:
            json.dump(users, f)
        
        await update.message.reply_text(f"Completed subscription for {user.first_name} {user.last_name}.")
        logger.info(f"Completed subscription for {user.first_name} {user.last_name}.")
    except Exception as e:
        await update.message.reply_text("An error occurred while trying to subscribe.")
        logger.error(f"An error occurred while trying to subscribe. {e}")


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    users = []
    user_json = { "id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name}

    # read from file
    try:
        with open(env_users_file, 'r') as f:
            users = json.load(f)
    except Exception as e:
        users = []

    # check if user exists
    for u in users:
        if u['id'] == user.id:
            users.remove(u)
            break
    else:
        await update.message.reply_text(f"{user.first_name} {user.last_name} is not subscribed.")
        logger.info(f"{user.first_name} {user.last_name} is not subscribed.")
        return
    
    # write to file
    try:
        with open(env_users_file, 'w') as f:
            json.dump(users, f)
        
        await update.message.reply_text(f"Completed unsubscription for {user.first_name} {user.last_name}.")
        logger.info(f"Completed unsubscription for {user.first_name} {user.last_name}.")
    except Exception as e:
        await update.message.reply_text("An error occurred while trying to unsubscribe.")
        logger.error(f"An error occurred while trying to unsubscribe. {e}")
    

def main():
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = Application.builder().token(env_token).build()

    # Add command handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("remove", remove))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    loguro_config()
    env_validations()
    main()
