import datetime


def str_to_date(date):
    if date:
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        return None
