
class Parser:
    IN_FILE          : str
    VALUES_STRING    : str = " "
    
    def __init__(self, infile : str): 
        self.IN_FILE = infile
    
    def add_to_hash(self, count, capital):
        self.VALUES_STRING += f"('{count}', '{capital}'), "

    def parse(self) :
        with open(self.IN_FILE, "r") as f:
            data = f.read().split("\n")
        
        for line in data:
            dt  = line.split(":")
            if len(dt) != 2 :
                continue
            if dt[1] == "#":
                continue
            self.add_to_hash(*dt)
        return self.flush()

    def flush(self) -> dict:
        return self.VALUES_STRING[:-2]
