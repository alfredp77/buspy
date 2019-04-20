import datetime
import pytz

def set_minutes(minutes):
    return TimeHelper(minutes)

def now():
    d_naive = datetime.datetime.now()
    timezone = pytz.timezone("Asia/Singapore")
    return timezone.localize(d_naive)    

def gettime(time_str, current_time=None):
    current_time = current_time or now()
    split_time = time_str.split(":")
    hour = int(split_time[0])
    minute = int(split_time[1])
    try:
        return current_time.replace(hour=hour,minute=minute,second=0,microsecond=0)         
    except:
        return None

def diff_in_minutes(from_time, to_time):
    if not to_time:
        return None
    return int((to_time - from_time).total_seconds()/60)

class TimeHelper:
    def __init__(self, minutes_offset):
        self.minutes_offset = minutes_offset

    def before(self, ref_datetime):
        return ref_datetime - datetime.timedelta(minutes=self.minutes_offset)

    def after(self, ref_datetime):
        return ref_datetime + datetime.timedelta(minutes=self.minutes_offset)