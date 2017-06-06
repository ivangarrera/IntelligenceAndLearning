from tkinter import *
from json import *
import Node
import Graph
from queue import Queue

graph = Graph.Graph()
t = Text()


class Gui:
    def __init__(self):
        # Data JSON
        data = loads(open('kevinBacon.json').read())
        movies = self.return_distinct_movies(data)
        actors = self.return_distinct_actors(data)
        # Add movies to the graph
        self.add_movies(movies)
        # Add actors to the graph and connect actors with movies
        self.add_actors_and_connect(actors, data, movies)
        graph.set_end("Kevin Bacon")

        root = Tk()
        root.config(bg="black")
        root.geometry("500x500")
        lb = Listbox(bg="black", fg="white")

        for i in range(len(actors)):
            lb.insert(i+1, actors[i])

        t.pack()
        lb.pack()
        lb.bind('<<ListboxSelect>>', self.onselect)
        root.mainloop()

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        start = graph.set_start(value)
        print(start.element)
        graph.reset()
        self.bfs_method(start, graph.end)
        path = self.create_complete_path()
        str = self.print_path(path)
        t.insert(END, str+"\n")


    def return_distinct_movies(self, data):
        movies = []
        for i in range(len(data['actors'])):
            for j in range(len(data['actors'][i]['movies'])):
                if data['actors'][i]['movies'][j] not in movies:
                    movies.append(data['actors'][i]['movies'][j])
        return movies

    def return_distinct_actors(self, data):
        actors = []
        for i in range(len(data['actors'])):
            if data['actors'][i]['name'] not in actors:
                actors.append(data['actors'][i]['name'])
        return actors

    def get_movies(self, data, index):
        return data['actors'][index]['movies']

    def add_movies(self, movies):
        for i in range(len(movies)):
            n = Node.Node(movies[i])
            graph.add_node(n)

    def add_actors_and_connect(self, actors, data, movies):
        for i in range(len(actors)):
            actors_with_movies = self.get_movies(data, i)
            movies_with_actors = self.movies_to_actors(data, movies, actors)
            n = Node.Node(actors[i])
            graph.add_node(n)
            for j in range(len(actors_with_movies)):
                node_movie = graph.get_node(actors_with_movies[j])
                n.add_edge(node_movie)
        # Add connection between movies and actors
        for i in range(len(movies)):
            node_movie = graph.get_node(movies[i])
            actors_movie = movies_with_actors[node_movie.element]
            for j in range(len(actors_movie)):
                node_actor = graph.get_node(actors_movie[j])
                node_movie.add_edge(node_actor)

    def bfs_method(self, start, end):
        queue = Queue(1000)
        start.searched = True
        queue.put_nowait(start)
        while not queue.empty():
            current = queue.get_nowait()
            if current.element == end.element:
                break
            edges = current.edges
            for i in range(len(edges)):
                neighbor = edges[i]
                if not neighbor.searched:
                    neighbor.searched = True
                    neighbor.parent = current
                    queue.put_nowait(neighbor)

    def movies_to_actors(self, data, movies, actors):
        mov_to_act = {}
        for i in range(len(movies)):
            act_movie = []
            for j in range(len(actors)):
                for k in range(len(data['actors'][j]['movies'])):
                    if data['actors'][j]['movies'][k] == movies[i]:
                        act_movie.append(actors[j])
            mov_to_act[movies[i]] = act_movie
        return mov_to_act

    def create_complete_path(self):
        path = []
        node = graph.end
        path.append(node)
        next = node.parent
        while next is not None:
            path.append(next)
            next = next.parent
        return path

    def print_path(self, path):
        str = ""
        for i in range(len(path)):
            str += path[len(path) - i - 1].element
            if i != len(path) - 1:
                str += " --> "
        return str


obj = Gui()
