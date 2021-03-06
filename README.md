# buspy.sg
Notify when next bus is coming - for use in Singapore only.

## Setting up
### Tokens
Please ensure that you put your API tokens in tokens.json (put it in checkout folder), with the following format:
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

### Features
* Set a reminder when bus is coming
  * Usage in telegram: /nextbus [bus no] [bus stop no] [departure time, HH:mm format]
  * Example: /nextbus 372 67379 16:00
  If any bus is within 10 minutes of the requested departure time, buspy bot will send a message
  If the departure time is within 10 minutes, buspy will respond immediately, else it will send a reminder message later
  * Not available in dialogflow due to its restriction (requiring user to start the interaction)
  
* Ask when is the next available bus closest to the requested time

### Planned features
* Add capability to automatically update the bus_stops and bus_routes static data
* Consider first-last bus time on the bus stop when suggesting next bus timing
* Allow user to define a set of origin-destination map, so user can tell the bot this:
  * goto [destination] at [departure time]
  * Example: goto MRT at 10am
  buspy will then suggest the bus to take, and when that bus will come.

* Estimate bus arrival when there is no "Next Bus" data from LTA Data Mall