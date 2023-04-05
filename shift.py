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
        self.shift_type = Shift._generate_type(self.times)
    
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
    
    def _generate_type(times):
        start, end = times
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

    def __str__(self):
        return "{} {:>18} [{}] {} {}".format(self.shift_type,self.time_str,self.count, self.ride_num, self.ride)

def display_shift_table (shifts,crews,divider=" "):
    form = "{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {}"
    form = form.replace(" ",divider)
    sorted_crews = sorted({v for _,v in crews.items()})
    crew_order = {c: i for c,i in zip(sorted_crews, range(len(crews)))}
    header = {
        "O  ": "O",
        " S ": "S",
        "  C": "C",
        "OS ": "OS",
        " SC": "SC",
        "O C": "AD",
        "total": "AL"
    }
    header_order = ["total","OS "," SC","O C","O  "," S ","  C"]
    vals = {h: [0 for _ in range(len(crews))] for h in header_order}
    for shift in shifts:
        i = crew_order[crews[shift.ride]]
        typ = shift.shift_type
        vals[typ][i] += shift.count
        vals["total"][i] += shift.count
    print((form[:-2]).format(*[header[h] for h in header_order]))
    print("--+--+--+--+--+--+--+-")
    for crew in sorted_crews:
        i = crew_order[crew]
        these_vals = [vals[h][i] if vals[h][i]>0 else "" for h in header_order] + [crew]
        print(form.format(*these_vals))

    print()
    form = "|" + form.replace("2","3").replace(" ","|")
    print((form[:-2]).format(*[header[h] for h in header_order]))
    print("+---+---+---+---+---+---+---+-")
    print(form.format(*([sum(vals[h]) for h in header_order]+["total"])))

if __name__ == "__main__":
    # file can be selected from days/wed.txt or days/raw.txt which represent
    # 4/12/23 and 4/15/23 respectively. This is the info as of 11:45 am EDT on
    # 4/5/23. Very interesting how they are scheduling us at the beginning of
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
    
    print()
    display_shift_table(shifts, crews)