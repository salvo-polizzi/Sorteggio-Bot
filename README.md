# Sorteggio-Bot
Telegram Bot built with [python-telegram-bot](https://docs.python-telegram-bot.org/en/v20.0a4/index.html) library. This bot allow to **draw** one or more participants of a group choosing the number of participants.

---

## Setting up a local instance
If you want to set up a local insance you have to:

- **Install [system requirements](#systems-requirements)** 
- **Clone this repository** 
- **Send a message** to your bot on telegram
- **Set your token** with `python3 setup.py <token>` 
- **Launch** the bot with `python3 src/bot.py`

### Set up Botfather 

- If you don't have a token, send a message to [@BotFather](http://telegram.me/Botfather) to create a bot and get a token for it
- Type the command `\setprivacy` and choose your bot
- At the end type **disable** so that the bot will receive all the message that people send to the group

_NOTE: Set up botfather **before** adding the bot to a group_

### Systems requirements

- python 3
- python-pip3