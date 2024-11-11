import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes


from dotenv import load_dotenv
load_dotenv()
api_token=os.environ.get('API_TOKEN')

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the interactive Telegram Bot!')
    await show_option_buttons(update, context)


async def show_option_buttons(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard=[
        [InlineKeyboardButton("Option 1", callback_data="button_1")],
        [InlineKeyboardButton("Option 2", callback_data="button_2")],
        [InlineKeyboardButton("Option 3", callback_data="button_3")],
    ]
    reply_markup=InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)

async def button_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f'You selected option: {query.data.split("_")[1]}')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to the following commands:\n/start - Start the bot\n/help - Get help information'
    )


def main():
    application = Application.builder().token(api_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(button_selection_handler, pattern='^button_'))
    application.run_polling()

if __name__ == '__main__':
    main()