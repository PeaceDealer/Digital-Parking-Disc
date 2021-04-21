from datetime import datetime, timedelta

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

now = datetime.now()
print(now)    
print(ceil_dt(now, timedelta(minutes=30)))