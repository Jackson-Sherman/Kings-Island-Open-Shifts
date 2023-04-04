import datetime as dt
import re
import json

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
        return "{:>18} [{}] {} {}".format(self.time_str,self.count, self.ride_num, self.ride)

if __name__ == "__main__":
    # file can be selected from days/wed.txt or days/raw.txt which represent
    # 4/12/23 and 4/15/23 respectively. This is the info as of 7:00pm EDT on
    # 4/4/23. Very interesting how they are scheduling us at the beginning of
    # this year. I don't know what they're doing honestly. Also 4/15 and 4/16
    # have the exact same availible open shifts...
    with open("days/sat.txt", "r") as file:
        all_lines = file.read().splitlines()
    
    with open("crews.json", "r") as file:
        crews = json.load(file)
    
    shifts = [Shift(all_lines[i:i+2]) for i in range(0, len(all_lines), 2)]
    count_of_crews = {}
    for shift in shifts:
        crew = crews[shift.ride]
        if crew not in count_of_crews:
            count_of_crews[crew] = 0
        count_of_crews[crew] += shift.count
    
    for crew in sorted(count_of_crews.keys()):
        print(count_of_crews[crew], crew)
    print(sum([v for _,v in count_of_crews.items()]))

    for shift in sorted(sorted(shifts, key=lambda s: s.times[0]), key=lambda s: crews[s.ride]):
        print(shift)