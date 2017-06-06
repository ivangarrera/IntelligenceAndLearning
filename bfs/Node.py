class Node:
    def __init__(self, element):
        self.element = element
        self.edges = []
        self.searched = False
        self.parent = None

    def add_edge(self, neighbor):
        self.edges.append(neighbor)

