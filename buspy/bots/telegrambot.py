import json
from buspy.checker_builder import build_checker
from buspy.datetime_helpers import gettime
from buspy.bots.explain_arrivals import explain

rel_path="../buspy/tokens.json"
with open(rel_path) as f:
    tokens = json.load(f)

import botogram
bot = botogram.create(tokens["telegram"])

subscriptions = []

@bot.command("hello")
def hello_command(chat, message, args):
    """Welcome to buspy. I can help you to find and send reminder when the next bus is coming!"""
    chat.send("Welcome to buspy. I can help you to find and send reminder when the next bus is coming")

def check_and_send_message(chat, checker):
    result = checker.time_to_be_at_bus_stop()
    can_use_result = (result.within_range 
                    or (result.outside_range and result.outside_range_may_be_acceptable)
                    or (not result.outside_range and result.after_requested))

    if can_use_result:
        message = explain(result).replace('<text>','').replace('</text>','')
        chat.send(message)
        return True
    return False

@bot.timer(10)
def check(bot):
    tocheck = subscriptions.copy()
    for checker in tocheck:
        message_sent = check_and_send_message(bot.chat(checker.owner_id), checker)
        if message_sent or checker.expired():
            subscriptions.remove(checker)

@bot.command("nextbus")
def nextbus_command(chat, message, args):
    """Scheduler reminder when the next bus is coming."""
    
    usage = """
    Usage: /nextbus <busno> <busstop> <departuretime HH:mm format>
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

    message_sent = check_and_send_message(chat, checker)
    if message_sent:
        return
    
    subscriptions.append(checker)
    chat.send(f"I will let you know once the bus {busno} is coming to {busstop} before {departuretime}" )


if __name__ == "__main__":
    bot.run()
