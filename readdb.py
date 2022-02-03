import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

hours_datetime_tpl = '%Y-%m-%d %H:00:00'
days_datetime_tpl = '%Y-%m-%d 00:00:00'

hours_tpl = '''
select 
    strftime("{datetime_tpl}",  datetime(dt+1600000000, "unixepoch")), 
    sum(value)
from 
    {tablename} 
where 
    dt+1600000000 between 
        cast(strftime("%s", "{min_t}") as integer) and 
        cast(strftime("%s", "{max_t}") as integer)
group by 1
'''

tablename='d_35478F91'
min_t='2022-01-01'
max_t='2022-02-02'

def devices():
    con = sqlite3.connect('data.sqlite')
    res = list(con.execute('select * from devices'))
    con.close()
    return json.dumps(res)



def hours_in_day(tablename, day):
    day = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S.%fZ")
    min_t = day.replace(hour=0, minute=0, second=0, microsecond=0)
    max_t = min_t + timedelta(1)
    con = sqlite3.connect('data.sqlite')
    res = list(con.execute(hours_tpl.format(datetime_tpl=hours_datetime_tpl, tablename=tablename, min_t=min_t, max_t=max_t)))
    con.close()
    return json.dumps(res)

def days_in_week(tablename, day_in_week):
    day_in_week = datetime.strptime(day_in_week, "%Y-%m-%dT%H:%M:%S.%fZ")
    min_t = day_in_week.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(day_in_week.weekday())
    max_t = min_t + timedelta(7)
    con = sqlite3.connect('data.sqlite')
    res = list(con.execute(hours_tpl.format(datetime_tpl=days_datetime_tpl, tablename=tablename, min_t=min_t, max_t=max_t)))
    con.close()
    return json.dumps(res)

def days_in_month(tablename, day_in_month):
    day_in_month = datetime.strptime(day_in_month, "%Y-%m-%dT%H:%M:%S.%fZ")
    min_t = day_in_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0) 
    max_t = min_t + relativedelta(months=1)
    con = sqlite3.connect('data.sqlite')
    res = list(con.execute(hours_tpl.format(datetime_tpl=days_datetime_tpl, tablename=tablename, min_t=min_t, max_t=max_t)))
    con.close()
    return json.dumps(res)


if __name__ == '__main__':
    print( hours_in_day(tablename, datetime.now()-timedelta(1)))
    print( days_in_week(tablename, datetime.now()))