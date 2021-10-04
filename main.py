import datetime

import matplotlib.pyplot as plt
import pynmea2

import simple_geo


def parse_nmea_messages(path: str):
    nmea_messages = []
    gps = open(path, 'r')
    lines = gps.readlines()

    for line in lines:
        try:
            # remove first character as csv has extra comma
            nmea_message = pynmea2.parse(line.strip()[1:])
            nmea_messages.append(nmea_message)
        except pynmea2.ParseError as e:
            print(f'Parse error {e}')
            continue

    return nmea_messages


def get_gga_messages(nmea_messages) -> [pynmea2.GGA]:
    messages = []

    for nmea_message in nmea_messages:
        if isinstance(nmea_message, pynmea2.GGA):
            messages.append(nmea_message)

    return messages


def get_rmc_messages(nmea_messages) -> [pynmea2.RMC]:
    messages = []

    for nmea_message in nmea_messages:
        if isinstance(nmea_message, pynmea2.RMC):
            print(nmea_message)
            messages.append(nmea_message)

    return messages


def parse_gga_heading(gga_list: [pynmea2.GGA]):
    last_position = None
    headings = []
    date_times = []

    for gga in gga_list:
        if last_position is None:
            last_position = simple_geo.GeoPostion(gga.latitude, gga.longitude)
        else:
            current_position = simple_geo.GeoPostion(gga.latitude, gga.longitude)
            heading = simple_geo.calculate_delta(current_position, last_position)[1]
            headings.append(heading)

            # todo not hardcode this part
            date_prefix = datetime.date(2021, 6, 15)
            datetime_gga = datetime.datetime.combine(date_prefix, gga.timestamp)

            date_times.append(datetime_gga)

            last_position = simple_geo.GeoPostion(gga.latitude, gga.longitude)
    return date_times, headings


def parse_rmc_heading(rmc_list: [pynmea2.RMC]):
    headings = []
    date_times = []

    for rmc in rmc_list:
        headings.append(rmc.true_course)
        date_times.append(rmc.datetime)
    return date_times, headings


if __name__ == "__main__":
    nmea_messages = parse_nmea_messages('data/june-16-moving-test/gps-10-raw-5m.csv')
    nmea_messages2 = parse_nmea_messages('data/june-16-moving-test/gps-11-raw-5m.csv')
    nmea_messages3 = parse_nmea_messages('data/june-16-moving-test/gps-12-raw-5m.csv')

    rmc = get_rmc_messages(nmea_messages)
    rmc2 = get_rmc_messages(nmea_messages2)
    rmc3 = get_rmc_messages(nmea_messages3)

    # gga = get_gga_messages(nmea_messages)
    # gga2 = get_gga_messages(nmea_messages2)
    # gga3 = get_gga_messages(nmea_messages3)

    rmc_date_times, rmc_headings = parse_rmc_heading(rmc)
    rmc_date_times2, rmc_headings2 = parse_rmc_heading(rmc2)
    rmc_date_times3, rmc_headings3 = parse_rmc_heading(rmc3)

    # gga_date_times, gga_headings = parse_gga_heading(gga)
    # gga_date_times2, gga_headings2 = parse_gga_heading(gga2)
    # gga_date_times3, gga_headings3 = parse_gga_heading(gga3)

    plt.plot(rmc_date_times, rmc_headings, '.')
    plt.plot(rmc_date_times2, rmc_headings2, '.')
    plt.plot(rmc_date_times3, rmc_headings3, '.')
    plt.show()

    # plt.plot(gga_date_times, gga_headings, '.')
    # plt.plot(gga_date_times2, gga_headings2, '.')
    # plt.plot(gga_date_times3, gga_headings3, '.')
    # plt.show()
