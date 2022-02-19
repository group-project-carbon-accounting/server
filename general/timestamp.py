import time

TIMESTAMP_OF_2020 = 1577836800

def generate_timestamp():
    return int(time.time()) - TIMESTAMP_OF_2020