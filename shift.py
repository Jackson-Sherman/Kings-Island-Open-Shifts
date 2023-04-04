import datetime as dt
import re

class Shift:
    def __init__(self, lines):
        searched = re.search(r"^\[(\d+)\] • ", lines[0])
        self.count = 1
        if searched:
            self.count = int(searched.group(1))
            lines[0] = lines[0][len(searched.group(0)):]
        self.times, self.duration = Shift._generate_times(lines[0])
        self.time_str = re.search(r"^([^[]*)",lines[0]).group(1)[:-1]
        line = str(lines[1])
        self.ride_num = int(re.search(r"^\d+",line).group(0))
        self.ride = re.search(r"^\d+\s([^/]*)/", line).group(1)
        self.type = re.search(r"^[^/]+/(.*)",line).group(1)
    
    def _generate_times(line):
        def get_time(gs,i):
            i = 3 if i else 0
            hr = int(gs[i])
            mi = int(gs[i+1])
            ap = gs[i+2]
            if hr == 12 and ap == "A":
                hr -= 12
            if hr != 12 and ap == "P":
                hr += 12
            return dt.time(hr, mi)
        groups = re.search(r"^[^0-9]*(1?\d):([0-5]\d) (A|P)M - (1?\d):([0-5]\d) (A|P)M \[(1?\d[.]\d{4})\]",str(line)).groups()
        return (get_time(groups, False), get_time(groups, True)), float(groups[6])

    def __str__(self):
        return "{} [{}] {} {}".format(self.time_str,self.count, self.ride_num, self.ride)

if __name__ == "__main__":
    with open("raw.txt", "r") as file:
        all_lines = file.read().splitlines()
    
    shifts = [Shift(all_lines[i:i+2]) for i in range(0, len(all_lines), 2)]
    count_of_rides = {}
    for shift in shifts:
        if shift.ride not in count_of_rides:
            count_of_rides[shift.ride] = 0
        count_of_rides[shift.ride] += shift.count
    
    for ride in sorted(count_of_rides.keys()):
        print(count_of_rides[ride], ride)
    print(sum([v for _,v in count_of_rides.items()]))

    for shift in sorted(shifts, key=lambda s: s.times[0]):
        print(shift)