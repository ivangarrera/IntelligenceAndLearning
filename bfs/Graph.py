class Graph:
    def __init__(self):
        self.nodes = []
        self.graph = {}
        self.start = None
        self.end = None

    def add_node(self, node):
        self.nodes.append(node)
        self.graph[node] = node

    def reset(self):
        for i in range(len(self.nodes)):
            self.nodes[i].searched = False
            self.nodes[i].parent = None

    def get_node(self, name):
        for i in self.graph:
            if self.graph[i].element == name:
                return self.graph[i]
        return None

    def set_start(self, start):
        self.start = self.get_node(start)
        return self.start

    def set_end(self, end):
        self.end = self.get_node(end)
        return self.end
