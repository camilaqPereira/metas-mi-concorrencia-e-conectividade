from enum import Enum
from json import load
import os
import numpy as np
from scipy.sparse import csr_matrix, csgraph


class FilePathsManagement(Enum):
    PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    NODES_FILE_PATH = PARENT_DIR+'\\DB\\matches_and_destinations.txt'
    ROUTES_DATA_FILE_PATH = PARENT_DIR+'\\DB\\routes_data.json'
    USERS_FILE_PATH = PARENT_DIR+'\\DB\\users.json'
    TICKETS_FILE_PATH = PARENT_DIR+'\\DB\\tickets.json'
    GRAPH_FILE_PATH = PARENT_DIR+'\\DB\\graph.json'


class Route:

    def __init__(self, match = '', destination = '', sits = 0, id = None):
        self.match = match
        self.destination = destination
        self.sits = sits
        self.id = id

    def to_string(self):
        return {'match': self.match, 'destination': self.destination, 'sits': self.sits, 'id': self.id}
    
    def from_string(self, data):
        self.match = data['match']
        self.destination = data['destination']
        self.sits = data['sits']
        self.id = data['id']


class ServerData:
    def __init__(self):
        self.adjacency_list = self.__init_adjacency_list()
        self.sparse_matrix = self.__create_sparse_matrix()
        self.matches_and_destinations = self.__init_matches_and_destinations()
        self.flights = self.__init_flights()

    def __parse_to_dict(self, item):
        loaded_dict = {int(key): value for key, value in item}
        for key in loaded_dict:
            loaded_dict[key] = [tuple(row) for row in loaded_dict[key]]
        return loaded_dict

    def __init_adjacency_list(self):
        try:
            with open(FilePathsManagement.GRAPH_FILE_PATH.value, 'r') as file:
                adj_list = load(file, object_pairs_hook=self.__parse_to_dict)
        except:
            adj_list = {}
        return adj_list


    def __create_sparse_matrix(self):
        nodes_count = len(self.adjacency_list.keys())
        mtx = np.zeros((nodes_count, nodes_count))

        for vertex, neighbor in self.adjacency_list.items():
            for item in neighbor:
                mtx[vertex, item[0]] = item[1]
        return csr_matrix(mtx, dtype=int)
    
    def __init_matches_and_destinations(self):
        try:
            with open(FilePathsManagement.NODES_FILE_PATH.value, 'r') as nodes_file:
                nodes = nodes_file.read()
            nodes = list(nodes.split(","))
        except FileNotFoundError:
            nodes = []
        return nodes 
    
    def __init_flights(self):
        try:
            with open(FilePathsManagement.ROUTES_DATA_FILE_PATH.value, 'r') as flights_file:
                data = load(flights_file)
            flights = {}
            for key, value in data.items():
                flights[eval(key)] = Route(match=value['match'], destination=value['destination'], sits=value['sits'], id=value['id'])
        except FileNotFoundError:
            flights = {}
        return flights
    
    def add_graph_node(self, node:int):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
    
    def add_graph_edge(self, origin:int, destination:int, weight:int):
        self.add_graph_node(origin)
        self.add_graph_node(destination)
        self.adjacency_list[origin].append((destination, weight))
    
    def set_graph_edge_weight(self, origin:int, destination:int, new_weight:int):
        if origin in self.adjacency_list:
            for neighbor in self.adjacency_list.get(origin):
                if neighbor[0] == destination:
                    self.adjacency_list[origin][destination] = [destination, new_weight]
                    self.sparse_matrix[origin, destination] = new_weight

    def search_route(self, match:int, destination:int):
        match_index = self.matches_and_destinations.index(match)
        destination_index = self.matches_and_destinations.index(destination)

        shortest_paths, predecessors_mtx = csgraph.yen(self.sparse_matrix, source = match_index, sink = destination_index, K=3, return_predecessors=True)

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
        return self.__convert_paths(paths)
    
    def __convert_paths(self, paths:list):
        routes = []
        for i in range(len(paths)):
            routes.append([])
            for j in range(len(paths[i])-1):
                key = (paths[i][j], paths[i][j+1])
                routes[i].append(self.flights.get(key).to_string())
        return routes
    
    def parse_flights_to_str(self):
        return {f"{key}": value.to_string() for key, value in self.flights.items()}

def parse_to_dict(item):
    loaded_dict = {int(key): value for key, value in item}
    for key in loaded_dict:
        loaded_dict[key] = [tuple(row) for row in loaded_dict[key]]
    return loaded_dict

