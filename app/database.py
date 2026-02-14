import json






def save_data():
    with open (data.json, "w") as f:
        data = json.dump()



def load_data():
     with open (data.json, "r") as f:
        data = json.load()