from datetime import datetime


def current_datetime():

    now = datetime.now()

    return now.strftime("%d-%m-%Y %I:%M:%S %p")