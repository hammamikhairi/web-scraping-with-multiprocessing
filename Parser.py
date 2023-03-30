
class Parser:
    IN_FILE          : str
    DATA_DICT        : dict =  {}
    PER_COUNTRY_DICT : dict = {}

    def __init__(self, infile : str): 
        self.IN_FILE = infile
    
    def add_to_hash(self, count, city, temp):
        if count not in self.DATA_DICT:
            self.DATA_DICT[count]           = {}
            self.PER_COUNTRY_DICT[count]    = [0, 0] # 0 : temp / 1 : cities
        if temp != "#":
            self.PER_COUNTRY_DICT[count][1] += 1
            self.PER_COUNTRY_DICT[count][0] += int(temp)
            
        self.DATA_DICT[count][city] = temp

    def parse(self) :
        with open(self.IN_FILE, "r") as f:
            data = f.read().split("\n")
        
        total_temp   = 0
        total_cities = 0

        for line in data:
            dt  = line.split(":")
            if len(dt) != 3 :
                continue
            if dt[2] != "#":
                total_temp   += int(dt[2])
                total_cities += 1
            self.add_to_hash(*dt)
        mid, miid = self.flush()
        return mid, miid, total_temp / total_cities

    def flush(self) -> dict:
        return self.DATA_DICT, {country : vals[0]/vals[1] for country, vals in self.PER_COUNTRY_DICT.items()}
