import json
from buspy.checker_builder import build_checker
from buspy.datetime_helpers import gettime
from bots.explain_arrivals import explain

rel_path="../buspy/tokens.json"
with open(rel_path) as f:
    tokens = json.load(f)

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

def get_message(result):
    message = explain(result)
    return message.replace('<text>','').replace('</text>','')

@bot.timer(10)
def check(bot):
    tocheck = subscriptions.copy()
    for checker in tocheck:
        result = checker.time_to_be_at_bus_stop()
        range_ok = result.within_range or result.outside_range_may_be_acceptable or result.after_requested
        if range_ok: 
            message = get_message(result)
            bot.chat(checker.owner_id).send(message)

        if range_ok or checker.expired():
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
    checker, message = build_checker(busstop, busno, departuretime.isoformat(), args[2], chat.id)
    
    if message:
        chat.send(message)
        return

    first_result = checker.time_to_be_at_bus_stop()
    message = get_message(first_result)
    if first_result.within_range or first_result.outside_range_may_be_acceptable or first_result.after_requested:
        chat.send(message)
        return
    
    subscriptions.append(checker)
    chat.send(f"I will let you know once the bus {busno} is coming to {busstop} before {departuretime}" )


if __name__ == "__main__":
    bot.run()
