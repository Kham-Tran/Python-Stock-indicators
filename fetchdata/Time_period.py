import datetime
import pandas as pb

DAY = 30


def get_date():
    return datetime.datetime.now().date()


def get_currrent_day():
    current = datetime.datetime.now()
    # return str(current.year) + "-" + str(current.month) + "-" + str(current.day + 1)
    return current


def get_timestamp(date):
    return pb.Timestamp(year=date.year, month=date.month, day=date.day, hour=date.hour+3, minute=date.minute, tz='America/New_York')


def date_by_month():
    current = datetime.datetime.now()
    ago = datetime.timedelta(days=DAY)
    date_N_day_ago = current - ago
    return date_N_day_ago.date()

