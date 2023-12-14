# Forex Tracker Bot


## Dependencies

```sh
pip3 install requests beautifulsoup4 python-dateutil PyYAML
pip3 install python-telegram-bot
```

## API

### Forex tracker
```py
forex_tracker = ForexTracker(forex, thresholds, target_margin, safe_margin)
```

### Telegram Bot
```py
forex_bot = ForexTrackerBot(forex_tracker, name, period, token, api_url, chat_id)
forex_bot.run()
```


## Roadmap
- [x] async loop
- [ ] plot graph
- [ ] gui


## Reference
- [Telegram bot API](https://core.telegram.org/bots/api)
- [Deploy in AWS](https://www.youtube.com/watch?v=ZfU0IifQSjA&t=61s)
