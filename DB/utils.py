import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Server.RouteClass import Route
A=0
B=1
C=2
D=3

matches_and_destinations = ['A', 'B', 'C','D']

adjacency_list = {
    0: [(1,1), (2,1)],
    1: [(0,1)],
    2:[(1,1),(3,1)],
    3: [(2,1)]
}

flights = {
    (A, B): Route('A', 'B', 10, '001'),
    (A, C): Route('A', 'C', 10, '002'),
    (B, A): Route('B', 'A', 10, '003'),
    (C, B): Route('C', 'B', 10, '004'),
    (C, D): Route('C', 'D', 10, '005'),
    (D, C): Route('D', 'C', 10, '006') 
}

def parse_to_dict(item):
    loaded_dict = {int(key): value for key, value in item}
    for key in loaded_dict:
        loaded_dict[key] = [tuple(row) for row in loaded_dict[key]]
    return loaded_dict
