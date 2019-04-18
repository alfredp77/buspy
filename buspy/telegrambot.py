import json
from incoming_bus_checker import IncomingBusChecker
from datamall_query import RequestSender, ArrivalFetcher
from datetime_helpers import gettime, now

request_sender = RequestSender()
arrival_fetcher = ArrivalFetcher(request_sender)

rel_path="../buspy/tokens.json"
with open(rel_path) as f:
    tokens = json.load(f)

rel_path2="../buspy/data/bus_stops.json"
with open(rel_path2) as f:
    bus_stops = json.load(f)    

import botogram
bot = botogram.create(tokens["telegram"])

subscriptions = []

@bot.command("hello")
def hello_command(chat, message, args):
    """Welcome to buspy. I can help you to find the next bus arrival!"""
    chat.send("Hello world")


@bot.prepare_memory
def init(shared):
    print("subs is about to be set")
    shared["subs"] = []


@bot.timer(10)
def check(bot):
    tocheck = subscriptions.copy()
    for checker in tocheck:
        message = checker.check()
        if message: 
            bot.chat(checker.owner_id).send(message)

        if message or checker.expired():
            subscriptions.remove(checker)


@bot.command("nextbus")
def nextbus_command(chat, message, args):
    """Scheduler reminder when the next bus is coming."""
    
    usage = """
    Usage: /nextbus <busno> <busstop> <departuretime>
     Example:  /nextbus 372 67379 10:00
    """
    if len(args) < 3: 
        chat.send(usage)
        return

    busno  = args[0]
    busstop  = args[1]
    departuretime  = gettime(args[2])

    if busstop not in bus_stops:
        chat.send(f"I couldn't find your bus stop {args[1]}. Please try again.")
        return       


    if not departuretime:
        chat.send(f"I don't understand your time {args[2]}. Please try again.")
        return

    if departuretime < now():
        chat.send(f"Your time {args[2]} is in the past. Please try again.")
        return
  
    checker = IncomingBusChecker(busstop, busno, departuretime, arrival_fetcher.get_arrival_time, owner_id=chat.id)

    message = checker.firstcheck() 
    if message:
        chat.send(message)
        return

    subscriptions.append(checker)
    chat.send(f"I will let you know once the bus {busno} is coming to {busstop} before {departuretime}" )


if __name__ == "__main__":
    bot.run()
