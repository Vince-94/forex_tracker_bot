import logging
import textwrap
import asyncio

from telegram import Bot, Update
from telegram import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters, Updater


# Set logging
logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)


class ForexTrackerBot():
    def __init__(self, forex_tracker, name, period, token, api_url = None, chat_id = None) -> None:
        self.forex_tracker = forex_tracker
        self._username = "@" + name
        self.period = period
        self._token = token
        self._api_url = api_url + token
        self._chat_id = chat_id

        self._send_message_url = self._api_url + "/sendMessage"
        self._get_updates_url = self._api_url + "/getUpdates"

    #! Periodic message
    async def send_message_periodically(self, app):
        message = self.forex_tracker.track()
        while True:  #TODO it is needed a while loop?
            if message:
                await self.send_message(message, app)
            await asyncio.sleep(self.period)

    async def send_message(self, message: str, app):
        logging.info(message)
        await app.bot.send_message(chat_id=self._chat_id, text=message)


    #! Commands handles
    # Start
    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm a bot, please talk to me!"
        )

    # Help
    async def help_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = textwrap.dedent("""
            Commands:
              /start:   start the bot
              /info:    bot description
              /help:    print out this message

            Text:
              set threshold/bounds <lower_value> <upper_value>
              set margin <value>
              sell <value>
              buy <value>
              status
        """)
        await update.message.reply_text(text)

    # Info
    async def info_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = f"{self.forex_tracker.name}: {self.forex_tracker.value}"
        logging.info(text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text
        )

    #! Messages handles
    # text_msg_handler
    def text_msg_logic(self, msg):
        text = msg.lower()

        if "set" in text:
            arg = text[4:].strip()
            if ("thresholds" or "bounds") in arg:
                thresholds = arg.split(" ")
                print(thresholds)
                if len(thresholds) != 3:
                    return "Set thresholds failed"
                lower_thresholds = thresholds[1]
                upper_thresholds = thresholds[2]
                self.forex_tracker.thresholds = [lower_thresholds, upper_thresholds]
                return f"Set thresholds: {lower_thresholds} ~ {upper_thresholds}"
            elif "margin" in arg:
                margin = arg.split(" ")
                margin = float(margin[1])
                self.forex_tracker.target_margin = margin
                return f"Set target margin: {margin}"
            else:
                return "Option not recognized"

        elif "sell" in text:
            arg = text[5:].strip()
            sell_point = float(arg)
            self.forex_tracker.sell = sell_point
            return f"Set sell point: {sell_point}"

        elif "buy" in text:
            arg = text[4:].strip()
            buy_point = float(arg)
            self.forex_tracker.buy = buy_point
            return f"Set buy point: {buy_point}"

        elif "status" in text:
            info = self.forex_tracker.show_info()
            return info

        else:
            return "Text not recognized"

    async def text_msg_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text = update.message.text
        print(f"User: {update.message.chat.id} in {message_type}: {text}")

        # handle chat types
        if message_type == "group":
            return

        response = self.text_msg_logic(text)
        print(f"Bot response:\n  {response}")

        await update.message.reply_text(response)


    #! Main run
    def run(self):

        app = Application.builder().token(self._token).build()

        # Commands handlres
        app.add_handler(CommandHandler("start", self.start_cmd))
        app.add_handler(CommandHandler("help", self.help_cmd))
        app.add_handler(CommandHandler("info", self.info_cmd))

        # Message handlers
        app.add_handler(MessageHandler(filters.TEXT, self.text_msg_handler))

        # Periodic asynchronous
        asyncio.ensure_future(self.send_message_periodically(app))

        # Keep polling
        app.run_polling(allowed_updates=Update.ALL_TYPES)
