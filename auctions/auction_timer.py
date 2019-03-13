import datetime

# PERIOD_CLOSES = datetime.datetime(2019, 4, 20, 16, 20, 0, 420)

def period_end():
# 
    # return PERIOD_CLOSES
    return datetime.datetime.now() + datetime.timedelta(days=1)
    