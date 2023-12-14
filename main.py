from src.forex_tracker import ForexTracker
from utils.forex_tracker_bot import ForexTrackerBot

import logging
import time
import yaml


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


with open("config/config.yaml") as file:
    config = yaml.safe_load(file)

forex = config["Forex"]["name"]
thresholds = config["Forex"]["thresholds"]
period = config["Forex"]["period"]*60
target_margin = config["Forex"]["target_margin"]
safe_margin = config["Forex"]["safe_margin"]

bot_name = config["Telegram"]["BotName"]
api_token = config["Telegram"]["ApiToken"]
api_url = config["Telegram"]["ApiUrl"]
chat_id = config["Telegram"]["ChatId"]



def main():
    forex_tracker = ForexTracker(forex=forex, thresholds=thresholds, target_margin=target_margin, safe_margin=safe_margin)
    logger.info(f"{forex_tracker.title}")

    forex_bot = ForexTrackerBot(forex_tracker=forex_tracker, name=bot_name, period=period, token=api_token, api_url=api_url, chat_id=chat_id)
    forex_bot.run()


if __name__ == "__main__":
    main()
