import json
def load_zones(path="zone/zones.json"):
    with open(path, "r") as file:
        return json.load(file)
