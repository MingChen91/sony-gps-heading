import datetime

import pynmea2
from matplotlib import pyplot as plt


def parse_nmea_messages():
    nmea_messages = []
    gps1 = open('data/june-16-moving-test/gps-1.csv', 'r')
    lines = gps1.readlines()

    for line in lines:
        try:
            # remove first character as csv has extra comma
            nmeaMessage = pynmea2.parse(line.strip()[1:])
            nmea_messages.append(nmeaMessage)
        except pynmea2.ParseError as e:
            print(f'Parse error {e}')
            continue

    return nmea_messages


if __name__ == "__main__":
    nmea_messages = parse_nmea_messages()

    # draw all times
    timestamp = []
    value = []
    for message in nmea_messages:
        try:
            timestamp.append(message.timestamp)
            value.append(1)
        finally:
            continue

    my_date = datetime.date(1991, 7, 15)
    x_dt = [datetime.datetime.combine(my_date, t) for t in timestamp]

    print(type(timestamp[1]))
    plt.plot(x_dt, value)
    plt.show()
