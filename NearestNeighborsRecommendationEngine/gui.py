from json import *
from tkinter import *
import math
import operator

class Gui:
    def __init__(self):
        # Load data
        self._data = loads(open("movies.json").read())
        self._person1 = ""
        self._person2 = ""
        self._person1_scnd = ""

        # Create both interfaces
        self._lb1, self._lb2, self._btn, self._txt, self._root = self._create_first_interface()
        self._lb1_scnd, self._btn_scnd, self._txt_scnd, self._root_scnd = self._create_second_interface()

        # Get users information and users name.
        self._users = self._get_users_by_name(self._data)
        self._users_name = self._get_users_name(self._data)

        self._fill_list_box(self._lb1, self._lb2)
        self._fill_list_box(self._lb1_scnd, None)
        self._pack_items(self._lb1, self._lb2, self._btn, self._txt)
        self._pack_items(self._lb1_scnd, None, self._btn_scnd, self._txt_scnd)
        self._root_scnd.mainloop()
        self._root.mainloop()

    #  This functions creates the graphic interface and add the items.
    def _create_first_interface(self):
        root = Tk()
        root.config(bg='black')
        root.title("Similarities between two actors.")
        root.geometry('500x500+100+100')
        lb1 = Listbox(root, bg='black', fg='white', exportselection=0)
        lb2 = Listbox(root, bg='black', fg='white', exportselection=0)
        btn = Button(root, text="SUBMIT", command=self._call_euclidean_distance)
        txt = Text(root, bg='black', fg='white')
        return lb1, lb2, btn, txt, root

    def _create_second_interface(self):
        scnd_root = Tk()
        scnd_root.title("Top similarities for a given actor.")
        scnd_root.config(bg='black')
        scnd_root.geometry('500x500+800+100')
        lb1 = Listbox(scnd_root, bg='black', fg='white', exportselection=0)
        btn = Button(scnd_root, text='SUBMIT', command=self._find_nearest_neighbors)
        txt = Text(scnd_root, bg='black', fg='white')
        return lb1, btn, txt, scnd_root

    def _fill_list_box(self, lb1, lb2):
        if lb2 is not None:
            for i in range(len(self._users_name)):
                lb1.insert(i+1, self._users_name[i])
                lb2.insert(i+1, self._users_name[i])
        else:
            for i in range(len(self._users_name)):
                lb1.insert(i+1, self._users_name[i])

    def _pack_items(self, lb1, lb2, btn, txt):
        if lb2 is not None:
            btn.pack(side=BOTTOM)
            lb1.pack(side=LEFT, fill=BOTH, expand=1)
            lb1.bind('<<ListboxSelect>>', self._onselect_lb1)
            lb2.pack(side=LEFT, fill=BOTH, expand=1)
            lb2.bind('<<ListboxSelect>>', self._onselect_lb2)
            txt.pack()
        else:
            btn.pack(side=BOTTOM)
            lb1.pack(side=BOTTOM, fill=BOTH, expand=1)
            lb1.bind('<<ListboxSelect>>', self._onselect_scnd_lb1)
            txt.pack()

    #  Functions called when an item is chosen
    def _onselect_lb1(self, evt):
        w = evt.widget
        index_list1 = int(w.curselection()[0])
        self._person1 = w.get(index_list1)

    def _onselect_lb2(self, evt):
        w = evt.widget
        index_list2 = int(w.curselection()[0])
        self._person2 = w.get(index_list2)

    def _onselect_scnd_lb1(self, evt):
        w = evt.widget
        index_list1 = int(w.curselection()[0])
        self._person1_scnd = w.get(index_list1)

    #  Function called when button is pressed. This function calculates
    #  the similarities between actors.
    def _euclidean_distance(self, name1, name2):
        u1 = self._users[name1]
        u2 = self._users[name2]
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
        similarity = 1 / (1 + distance)
        return similarity

    def _call_euclidean_distance(self):
        self._txt.delete(1.0, END)
        similarity = self._euclidean_distance(self._person1, self._person2)
        self._txt.insert(INSERT, "Similarity between {} and {} is: {}".format(self._person1,
                                                                              self._person2,
                                                                              similarity))

    def _find_nearest_neighbors(self):
        self._txt_scnd.delete(1.0, END)
        name = self._person1_scnd
        similarity_scores = {}
        for i in self._users_name:
            if i != name:
                similarity = self._euclidean_distance(name, i)
                similarity_scores[i] = similarity
            else:
                similarity_scores[i] = -1
        sorted_hash = sorted(similarity_scores.items(), key=operator.itemgetter(1))
        for i in range(5):
            desired_person = sorted_hash[len(sorted_hash)-i-1]
            self._txt_scnd.insert(INSERT, "{} : {}\n".format(desired_person[0], desired_person[1]))

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
