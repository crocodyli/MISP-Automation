# MISP automation send information to Telegram

# Create a Bot in Telegram using BotFather.

1. Newbot
2. Enter the name of the Bot, in this case I used TeleMISPBot
3. It will display this message:

```
Done! Congratulations on your new bot. You will find it at t.me/TeleMISPBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
XXXXX:XXXXXXX
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

4. It is important that after this step, you need to create a group and add the bot to the group.
5. Give admin access to this bot, setting all possible permissions, except for “remain anonymous”
6. You need to extract the Bot’s information, such as the chat and group ID, using Telegram’s own API:

```
https://api.telegram.org/botXXXX:XXXXX/getUpdates
```

The bot's return will be:

```
         "chat": {
          "id": -XXXX,
          "title": "MISP",
          "type": "supergroup"
        },
        "date": XXXX,
        "new_chat_title": "MISP"
      }
```

## Evasive possibilities outside of MISP.

As the script and workflow presented many errors outside of MISP, it was necessary to work around it. In this case, I created a script to test sending messages by the Bot, to check if it would actually send the message to the Telegram channel.

```
import requests

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

# Exemplo de uso
bot_token = 'XXX:XXXX'
chat_id = '-XXXX'
message = '🚨 Testing messages on Telegram via MISP!'
print(send_telegram_message(bot_token, chat_id, message))
```

After receiving this message, I started incorporating other features into the script file, such as:

- Monitoring Events with specific TAGs.

- Monitoring and counting Event Attributes.

- Monitoring the Organization that published the event and/or target.

In addition, the script runs as a service in the system, which makes it easier to execute and there is no routine in the cron, I just put it to sleep for 12 hours. Therefore, every 12 hours a message is sent to my chat by the BOT!

The "final" script is attached in the repository, I hope it helped :)

For more tips and tweaks, contact me!


