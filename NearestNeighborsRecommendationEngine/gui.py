from json import *
from tkinter import *
import math


class Gui:
    def __init__(self):
        # Load data
        self._data = loads(open("movies.json").read())
        self._person1 = ""
        self._person2 = ""

        self._lb1, self._lb2, self._btn, self._root = self._create_interface()

        # Get users information and users name.
        self._users = self._get_users_by_name(self._data)
        self._users_name = self._get_users_name(self._data)

        self._fill_list_box(self._lb1, self._lb2)
        self._pack_items(self._lb1, self._lb2, self._btn)
        self._root.mainloop()

    #  This functions creates the graphic interface and add the items.
    def _create_interface(self):
        root = Tk()
        root.config(bg='black')
        root.geometry('500x500')
        lb1 = Listbox(bg='black', fg='white', exportselection=0)
        lb2 = Listbox(bg='black', fg='white', exportselection=0)
        btn = Button(root, text="SUBMIT", command=self._euclidean_similarity)
        return lb1, lb2, btn, root

    def _fill_list_box(self, lb1, lb2):
        for i in range(len(self._users_name)):
            lb1.insert(i+1, self._users_name[i])
            lb2.insert(i+1, self._users_name[i])

    def _pack_items(self, lb1, lb2, btn):
        btn.pack(side=BOTTOM)
        lb1.pack(side=LEFT, fill=BOTH, expand=1)
        lb2.pack(side=LEFT, fill=BOTH, expand=1)
        lb1.bind('<<ListboxSelect>>', self._onselect_lb1)
        lb2.bind('<<ListboxSelect>>', self._onselect_lb2)

    #  Functions called when an item is chosen
    def _onselect_lb1(self, evt):
        w = evt.widget
        index_list1 = int(w.curselection()[0])
        self._person1 = w.get(index_list1)

    def _onselect_lb2(self, evt):
        w = evt.widget
        index_list2 = int(w.curselection()[0])
        self._person2 = w.get(index_list2)

    #  Function called when button is pressed. This function calculates
    #  the similarities between actors.
    def _euclidean_similarity(self):
        u1 = self._users[self._person1]
        u2 = self._users[self._person2]
        self._clean_name_and_timestamp(u1)
        self._clean_name_and_timestamp(u2)
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

    def _clean_name_and_timestamp(self, dict):
        dict.pop('name', None)
        dict.pop('timestamp', None)

gui = Gui()
