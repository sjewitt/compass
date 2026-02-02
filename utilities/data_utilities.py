import json

compass_config_data = {"status":"unset", "configuration":{}}
def load_config_data():
    # This is the container filesystem path:
    with open(mode="r",file="/code/static/data/display_data_rationalised.json") as display_data:
        compass_config_data["configuration"] = json.load(display_data)
        compass_config_data["status"] = "set"
    return compass_config_data