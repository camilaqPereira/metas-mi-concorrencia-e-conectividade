from json import dump, load
from utils import *
import os

'''
file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'graph.json'))

serialized_list = {str(key): value for key, value in adjacency_list.items()}
with open(file_name, "w") as file:
    dump(serialized_list, file)
'''

serialized = {str(key): value.to_string() for key, value in flights.items()}

with open(ROUTES_DATA_FILE_PATH, 'w') as file:
    dump(serialized, file)
