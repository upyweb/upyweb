import time

def format_datetime(timestamp):
    # From: aiohttp
    # Weekday and month names for HTTP date/time formatting; always English!
    _weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    _monthname = [None,  # Dummy so we can use 1-based month numbers
                  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    return "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
        _weekdayname[wd], day, _monthname[month], year, hh, mm, ss
    )