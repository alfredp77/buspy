# buspy.sg
Notify when next bus is coming - for use in Singapore only.

## Setting up
### Tokens
Please ensure that you put your API tokens in tokens.json, with the following format:
```
{
    "lta": "tokenValue from LTA Data Mall",
    "telegram": "get this from botfather"
}
```
This file is git-ignored, and is NOT supposed to be pushed into git repo (unless you want the world to use your token)


### DialogFlow
Import DialogFlow_BusPy.zip to create the DialogFlow agent.

#### Running Flask server to serve DialogFlow's webhook
```
# from the checkout folder, run:
python dialogflow.py
```

### Telegram
#### Running the telegram bot
```
# from the checkout folder, run:
python -m buspy.bots.telegrambot
```