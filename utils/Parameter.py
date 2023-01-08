import json
import pathlib


def get_parameter(parameter):
    with open((str(pathlib.Path.cwd()) + "/Config/config.json"), 'r') as f:
        config = json.load(f)
    parameter = config[parameter]
    return parameter
