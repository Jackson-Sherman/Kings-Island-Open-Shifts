import datetime as dt

def get_type_osc(start, end):
    if isinstance(start, dt.datetime):
        start = start.time()
    if isinstance(end, dt.datetime):
        end = end.time()
    if start < dt.time(11,15):
        if end < dt.time(18):
            return "O  "
        elif end < dt.time(20,15):
            return "OS "
        else:
            return "O C"
    elif start < dt.time(13,30):
        if end < dt.time(20,15):
            return " S "
        else:
            return " SC"
    else:
        return "  C"