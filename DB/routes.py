import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from scipy.sparse.csgraph import yen
from graph import *
from utils import *
from json import load


def init_graph():
    try:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'graph.json')), "r") as file:
            routes_graph = Graph(adjacency_list=load(file, object_pairs_hook=parse_to_dict))
    except FileNotFoundError:
        routes_graph = Graph()
    
    return routes_graph



def search_route(routes_graph:Graph, match:int, destination:int):
    match_index = matches_and_destinations.index(match)
    destination_index = matches_and_destinations.index(destination)

    shortest_paths, predecessors_mtx = yen(routes_graph.sparse_matrix, source = match_index, sink = destination_index, K=3, return_predecessors=True)

    paths = []
    for i in range(len(shortest_paths)):
        if(shortest_paths[i] > 9999): #checking for
            continue
        
        new_path = []
        current_node = destination_index
        while current_node != match_index:
            new_path.append(int(current_node))
            current_node = predecessors_mtx[i,current_node]
        new_path.append(match_index)
        new_path.reverse()
        paths.append(new_path)
    return convert_paths(paths)


def convert_paths(paths:list):
    routes = []
    for i in range(len(paths)):
        routes.append([])
        for j in range(len(paths[i])-1):
            key = (paths[i][j], paths[i][j+1])
            routes[i].append(flights.get(key).to_string())
    print(routes)
    return routes