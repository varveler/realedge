import datetime


def str_to_dt_stockNewsAPI(date_str):
    "converts string to datetime for example Fri, 07 May 2021 13:25:16 -0400 "
    return datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')


def str_to_epoch_stockNewsAPI(date_str):
    return datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z').timestamp()
