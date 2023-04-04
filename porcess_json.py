import json
import datetime as dt

class Shift:
    def __init__(self, obj):
        self.id = obj["id"]
        self.start = dt.datetime.fromisoformat(obj["startDateTime"])
        self.end = dt.datetime.fromisoformat(obj["endDateTime"])
        try:
            self.ride = obj["commentNotes"][0]["notes"][0]["text"]
        except:
            self.ride = None
        self.count = obj["totalSimilarShifts"]
    
    def __str__(self):
        return "{:0>2}:{:0>2} - {:0>2}:{:0>2} [{}] {}".format(
            self.start.time().hour,
            self.start.time().minute,
            self.end.time().hour,
            self.end.time().minute,
            self.count,
            self.ride
        )

if __name__ == "__main__":
    with open("raw.json", "r") as file:
        data = json.load(file)
    shifts = {}
    for d in data:
        for k,v in d["openById"].items():
            if k not in shifts:
                shifts[k] = Shift(v)

    for shift in sorted(shifts.values(), key=lambda s: s.start):
        print(shift)
    
    print(sum([shift.count for shift in shifts.values()]))
