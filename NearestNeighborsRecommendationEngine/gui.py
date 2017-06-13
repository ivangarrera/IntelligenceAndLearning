from json import *
from tkinter import *
import math


class Gui:
    def __init__(self):
        # Load data
        self.data = loads(open("movies.json").read())
        self.person1 = ""
        self.person2 = ""

        self.lb1, self.lb2, self.btn, self.root = self.create_interface()

        # Get users information and users name.
        self.users = self._get_users_by_name(self.data)
        self.users_name = self._get_users_name(self.data)

        self.fill_list_box(self.lb1, self.lb2)
        self.pack_items(self.lb1, self.lb2, self.btn)
        self.root.mainloop()

    #  This functions creates the graphic interface and add the items.
    def create_interface(self):
        root = Tk()
        root.config(bg='black')
        root.geometry('500x500')
        lb1 = Listbox(bg='black', fg='white', exportselection=0)
        lb2 = Listbox(bg='black', fg='white', exportselection=0)
        btn = Button(root, text="SUBMIT", command=self.euclidean_similarity)
        return lb1, lb2, btn, root

    def fill_list_box(self, lb1, lb2):
        for i in range(len(self.users_name)):
            lb1.insert(i+1, self.users_name[i])
            lb2.insert(i+1, self.users_name[i])

    def pack_items(self, lb1, lb2, btn):
        btn.pack(side=BOTTOM)
        lb1.pack(side=LEFT, fill=BOTH, expand=1)
        lb2.pack(side=LEFT, fill=BOTH, expand=1)
        lb1.bind('<<ListboxSelect>>', self.onselect_lb1)
        lb2.bind('<<ListboxSelect>>', self.onselect_lb2)

    #  Functions called when an item is chosen
    def onselect_lb1(self, evt):
        w = evt.widget
        index_list1 = int(w.curselection()[0])
        self.person1 = w.get(index_list1)

    def onselect_lb2(self, evt):
        w = evt.widget
        index_list2 = int(w.curselection()[0])
        self.person2 = w.get(index_list2)

    #  Function called when button is pressed. This function calculates
    #  the similarities between actors.
    def euclidean_similarity(self):
        u1 = self.users[self.person1]
        u2 = self.users[self.person2]
        self.clean_name_and_timestamp(u1)
        self.clean_name_and_timestamp(u2)
        sum = 0
        for i, j in zip(u1, u2):
            num_movies_first = u1[i]
            num_movies_second = u2[j]
            if num_movies_first is not None and num_movies_second is not None:
                difference = num_movies_first - num_movies_second
            if num_movies_first is None:
                difference = 0 - num_movies_second
            if num_movies_second is None:
                difference = num_movies_first - 0
            sum += math.pow(difference, 2)

        distance = math.sqrt(sum)
        similarity = 1/(1+distance)
        print(similarity)

    #  Functions to manage JSON data
    def _get_users_by_name(self, data):
        users = {}
        for i in range(len(data['users'])):
            users[data['users'][i]['name']] = data['users'][i]
        return users

    def _get_users_name(self, data):
        list = []
        for i in range(len(data['users'])):
            list.append(data['users'][i]['name'])
        return list

    def clean_name_and_timestamp(self, dict):
        dict.pop('name', None)
        dict.pop('timestamp', None)

gui = Gui()
