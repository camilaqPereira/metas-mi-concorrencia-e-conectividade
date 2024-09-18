import os
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

NODES_FILE_PATH = PARENT_DIR+'/DB/matches_and_destinations.txt'
ROUTES_DATA_FILE_PATH = PARENT_DIR+'/DB/routes_data.json'


def parse_to_dict(item):
    loaded_dict = {int(key): value for key, value in item}
    for key in loaded_dict:
        loaded_dict[key] = [tuple(row) for row in loaded_dict[key]]
    return loaded_dict

