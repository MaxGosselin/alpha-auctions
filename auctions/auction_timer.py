from django.utils import timezone
import datetime
import pytz


PERIOD_CLOSES = datetime.datetime(2019, 3, 16, 17, 30, 0, 0, tzinfo=pytz.UTC)

def period_end():
# 
    # return PERIOD_CLOSES
    return PERIOD_CLOSES
    