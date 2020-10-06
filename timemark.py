# Copyright is waived. No warranty is provided. Unrestricted use and modification is permitted.

import sys
import datetime

base_year = 2020                    # Start year for timemark i.e. 2020 is year 0

# Custom base32 encoding consisting of letters and digits excluding the following characters;
# O, I and B are removed to avoid confusion with 0, 1 and 8 respectively
# U is removed to avoid accidental obscenity
base32_table = "0123456789ACDEFGHJKLMNPQRSTVWXYZ"


def base32_encode(value, num_digits):
    output = ""
    for i in range(num_digits):
        output = base32_table[value & 0x1f] + output
        value >>= 5
    return output


def base32_decode(value_string):
    accumulator = 0
    for i in range(len(value_string)-1):
        accumulator += base32_table.index(value_string[i])
        accumulator <<= 5
    accumulator += base32_table.index(value_string[-1])
    return accumulator


def timemark_encode():
    now = datetime.datetime.utcnow()
    # First part of the timemark consists of a single digit each for the year, month and day
    year = base32_table[(now.year - base_year) % 32]        # Wraps every 32 years
    month = base32_table[now.month]
    day = base32_table[now.day]
    # Second part of the timemark consists of 4 digits representing time of day divided in 2^20 units
    seconds_since_midnight = (now.hour*3600) + (now.minute*60) + now.second
    microseconds_since_midnight = (seconds_since_midnight * 1000000) + now.microsecond
    percent_of_day = float(microseconds_since_midnight) / 86400000000.0     # % of day that has passed from 0.0 to 1.0
    time_increment = int(percent_of_day * 1048576)                          # % of day times 2^20
    mark = year + month + day + "-" + base32_encode(time_increment, 4)
    return mark


def timemark_decode(mark):
    day_string, time_string = mark.split("-")
    # Decode first part of timemark to year, month and day
    year = base32_table.find(day_string[0]) + base_year
    month = base32_table.find(day_string[1])
    day = base32_table.find(day_string[2])
    # Decode second part of timemark to time of day
    time_increment = base32_decode(time_string)
    percent_of_day = float(time_increment) / 1048576.0
    microseconds_since_midnight = int(percent_of_day * 86400000000)
    seconds_since_midnight = microseconds_since_midnight / 1000000
    microseconds = int(microseconds_since_midnight % 1000000)
    seconds = int(seconds_since_midnight % 60)
    hours = int(seconds_since_midnight / 3600)
    minutes = int((seconds_since_midnight - (hours*3600)) / 60)
    decoded = "{0}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}.{6}".format(year, month, day, hours, minutes, seconds, microseconds)
    return decoded


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Current timemark is " + timemark_encode())
    else:
        mark = sys.argv[1].upper()
        decoded = timemark_decode(mark)
        print(mark + " decodes to " + decoded)
