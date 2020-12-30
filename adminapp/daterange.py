import datetime
from datetime import timedelta, date
def Daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


	
