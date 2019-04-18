import json
from incoming_bus_checker import IncomingBusChecker
from buspy.datamall_query import RequestSender, ArrivalFetcher

request_sender = RequestSender()
arrival_fetcher = ArrivalFetcher(request_sender)

rel_path="../buspy/tokens.json"
with open(rel_path) as f:
    tokens = json.load(f)

import botogram
bot = botogram.create(tokens["telegram"])

@bot.command("hello")
def hello_command(chat, message, args):
    """Welcome to buspy. I can help you to find the next bus arrival!"""
    chat.send("Hello world")


@bot.prepare_memory
def init(shared):
    shared["subs"] = []


@bot.timer(10)
def check(bot, shared):
    for checker in shared["subs"]:
        message = checker.check()
        if message: 
            bot.chat(checker.owner_id).send(message)


@bot.command("nextbus")
def nextbus_command(shared, chat, message, args):
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
    departuretime  = args[2]
  
    checker = IncomingBusChecker(busstop, busno, departuretime, arrival_fetcher.get_arrival_time, owner_id=chat.id)
    subs = shared["subs"]
    subs.append(checker)
    shared["subs"] = subs
    chat.send(f"I will let you know once the bus {busno} is coming to {busstop} before {departuretime}" )


if __name__ == "__main__":
    bot.run()
