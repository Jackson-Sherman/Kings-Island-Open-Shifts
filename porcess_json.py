import json
import datetime as dt
import re

class Shift:
    def __init__(self, obj):
        self.id = obj["id"]
        self.start = dt.datetime.fromisoformat(obj["startDateTime"])
        self.end = dt.datetime.fromisoformat(obj["endDateTime"])
        self.ride_orgJobRef_id, (self.ride_id, self.ride) = Shift._get_ride_info(obj)
        try:
            self.desc = obj["commentNotes"][0]["notes"][0]["text"]
        except:
            self.desc = None
        self.count = obj["totalSimilarShifts"]
    
    def _get_ride_info(obj):
        def process_qualifier(qualifier):
            qualifier = str(qualifier)
            searched = re.search("^CF/KI/OPS/RID/[^/]*/(4[01]\d\d) ([^/]*)/Ride Operator$",qualifier).groups()
            return int(searched[0]), searched[1]
        for segment in obj["segments"]:
            if segment["segmentTypeRef"]["id"] == 1:
                return segment["orgJobRef"]["id"], process_qualifier(segment["orgJobRef"]["qualifier"])
    
    def __str__(self):
        return "{:0>2}:{:0>2} - {:0>2}:{:0>2} [{}] {} {}".format(
            self.start.time().hour,
            self.start.time().minute,
            self.end.time().hour,
            self.end.time().minute,
            self.count,
            self.ride,
            self.desc
        )

if __name__ == "__main__":
    date = "2023-04-14"
    with open("raw.json", "r") as file:
        data = json.load(file)
    shifts = {}
    for d in data:
        ids = d["openByDate"][date]
        for i in ids:
            if i not in shifts:
                shifts[i] = Shift(d["openById"][i])

    for shift in sorted(shifts.values(), key=lambda s: s.start):
        print(shift)
    
    print(sum([shift.count for shift in shifts.values()]))
