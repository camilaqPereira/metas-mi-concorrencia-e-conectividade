import numpy as np
from  scipy.sparse import csr_matrix


class Graph():

    def __init__(self, adjacency_list:dict = {}):
        self.adjacency_list = adjacency_list
        self.sparse_matrix = self.__create_sparse_matrix()
    
    def __create_sparse_matrix(self):
        nodes_count = len(self.adjacency_list.keys())
        mtx = np.zeros((nodes_count, nodes_count))

        for vertex, neighbor in self.adjacency_list.items():
            for item in neighbor:
                mtx[vertex, item[0]] = item[1]
        return csr_matrix(mtx, dtype=int)
    
    def add_node(self, node:int):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
    
    def add_edge(self, origin:int, destination:int, weight:int):
        self.add_node(origin)
        self.add_node(destination)
        self.adjacency_list[origin].append((destination, weight))

    def set_edge_weight(self, origin:int, destination:int, new_weight:int):
        if origin in self.adjacency_list:
            for neighbor in self.adjacency_list.get(origin):
                if neighbor[0] == destination:
                    self.adjacency_list[origin][destination] = [destination, new_weight]
                    self.sparse_matrix[origin, destination] = new_weight
