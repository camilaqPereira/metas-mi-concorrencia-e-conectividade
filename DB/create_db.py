from json import dump, load
from utils import adjacency_list, parse_to_dict
import os

file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'graph.json'))

serialized_list = {str(key): value for key, value in adjacency_list.items()}
with open(file_name, "w") as file:
    dump(serialized_list, file)

