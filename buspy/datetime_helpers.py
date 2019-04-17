import datetime
import pytz

def set_minutes(minutes):
    return TimeHelper(minutes)

def now():
    d_naive = datetime.datetime.now()
    timezone = pytz.timezone("Asia/Singapore")
    return timezone.localize(d_naive)    

class TimeHelper:
    def __init__(self, minutes_offset):
        self.minutes_offset = minutes_offset

    def before(self, ref_datetime):
        return ref_datetime - datetime.timedelta(minutes=self.minutes_offset)

    def after(self, ref_datetime):
        return ref_datetime + datetime.timedelta(minutes=self.minutes_offset)