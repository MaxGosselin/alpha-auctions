from django.utils import timezone
import datetime
import pytz

PERIOD_CLOSES = datetime.datetime(2019, 3, 15, 3, 35, 0, 0, tzinfo=pytz.UTC)

def period_end():
# 
    # return PERIOD_CLOSES
    return min(PERIOD_CLOSES, timezone.now() + datetime.timedelta(hours=1))
    