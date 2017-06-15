from json import *
from tkinter import *
import math
import operator


class Gui:
    def __init__(self):
        # Load data
        self.__data = loads(open("movies.json").read())
        self.__person1 = ""
        self.__person2 = ""
        self.__person1_scnd = ""

        self.__titles = self.__get__titles(self.__data)

        # Create the interfaces
        self.__lb1, self.__lb2, self.__btn, self.__txt, self.__root = self.__create_first_interface()
        self.__lb1_scnd, self.__btn_scnd, self.__txt_scnd, self.__root_scnd = self.__create_second_interface()
        self._drop_downs, self._labels, self.__txt_third, self.__root_third = self.__create_third_interface()

        # Get users information and users name.
        # users = { 'Name' : { 'info' : value }, ... }
        self.__users = self.__get__users_by_name(self.__data)
        self.__users_name = self.__get__users_name(self.__data)  # Vector with all the user names

        self.__fill_list_box(self.__lb1, self.__lb2)
        self.__fill_list_box(self.__lb1_scnd, None)
        self.__pack_items(self.__lb1, self.__lb2, self.__btn, self.__txt)
        self.__pack_items(self.__lb1_scnd, None, self.__btn_scnd, self.__txt_scnd)
        self.__root_scnd.mainloop()
        self.__root.mainloop()

    #  This functions creates the graphic interface and add the items.
    def __create_first_interface(self):
        root = Tk()
        root.config(bg='black')
        root.title("Similarities between two actors.")
        root.geometry('500x500+100+100')
        lb1 = Listbox(root, bg='black', fg='white', exportselection=0)
        lb2 = Listbox(root, bg='black', fg='white', exportselection=0)
        btn = Button(root, text="SUBMIT", command=self.__call__euclidean_distance)
        txt = Text(root, bg='black', fg='white')
        return lb1, lb2, btn, txt, root

    def __create_second_interface(self):
        scnd__root = Tk()
        scnd__root.title("Top similarities for a given actor.")
        scnd__root.config(bg='black')
        scnd__root.geometry('500x500+800+100')
        lb1 = Listbox(scnd__root, bg='black', fg='white', exportselection=0)
        btn = Button(scnd__root, text='SUBMIT', command=self.__find_nearest_neighbors)
        txt = Text(scnd__root, bg='black', fg='white')
        return lb1, btn, txt, scnd__root

    def __create_third_interface(self):
        third__root = Tk()
        third__root.title("Movie recommendation")
        third__root.config(bg='black')
        third__root.geometry('500x500+1500+100')
        options = []
        string_var = []
        drop_down = []
        labels = []
        options.append('Not seen')
        # Assign a rate from 1 to 5
        for i in range(5):
            options.append(i+1)

        for i in range(len(self.__titles)):
            labels.append(Label(third__root, bg='black', fg='white', justify=LEFT, anchor=W, text=self.__titles[i]))
            labels[i].grid(row=i, column=0)
            string_var.append(StringVar(third__root))
            string_var[i].set('Not seen')  # Default value
            drop_down.append(OptionMenu(third__root, string_var[i], *options))
            drop_down[i].grid(row=i, column=1)
        btn = Button(third__root, text='SUBMIT', command=self.__predict_ratings)
        btn.grid(row=(len(self.__titles)+2), column=3)
        txt = Text(third__root, bg='black', fg='white')
        txt.grid(row=(len(self.__titles)+3), column=3)
        return string_var, labels, txt, third__root

    def __fill_list_box(self, lb1, lb2):
        if lb2 is not None:
            for i in range(len(self.__users_name)):
                lb1.insert(i+1, self.__users_name[i])
                lb2.insert(i+1, self.__users_name[i])
        else:
            for i in range(len(self.__users_name)):
                lb1.insert(i+1, self.__users_name[i])

    def __pack_items(self, lb1, lb2, btn, txt):
        if lb2 is not None:
            btn.pack(side=BOTTOM)
            lb1.pack(side=LEFT, fill=BOTH, expand=1)
            lb1.bind('<<ListboxSelect>>', self.__onselect__lb1)
            lb2.pack(side=LEFT, fill=BOTH, expand=1)
            lb2.bind('<<ListboxSelect>>', self.__onselect__lb2)
            txt.pack()
        else:
            btn.pack(side=BOTTOM)
            lb1.pack(side=BOTTOM, fill=BOTH, expand=1)
            lb1.bind('<<ListboxSelect>>', self.__onselect_scnd__lb1)
            txt.pack()

    #  Functions called when an item is chosen
    def __onselect__lb1(self, evt):
        w = evt.widget
        index_list1 = int(w.curselection()[0])
        self.__person1 = w.get(index_list1)

    def __onselect__lb2(self, evt):
        w = evt.widget
        index_list2 = int(w.curselection()[0])
        self.__person2 = w.get(index_list2)

    def __onselect_scnd__lb1(self, evt):
        w = evt.widget
        index_list1 = int(w.curselection()[0])
        self.__person1_scnd = w.get(index_list1)

    #  Function called when button is pressed. This function calculates
    #  the similarities between actors.
    def __euclidean_distance(self, u1, u2):
        self.__clean_name_and_timestamp(u1)
        self.__clean_name_and_timestamp(u2)
        sum = 0
        difference = 0
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

    def __call__euclidean_distance(self):
        self.__txt.delete(1.0, END)
        similarity = self.__euclidean_distance(self.__users[self.__person1],
                                               self.__users[self.__person2])
        self.__txt.insert(INSERT, "Similarity between {} and {} is: {}".format(self.__person1,
                                                                               self.__person2,
                                                                               similarity))

    def __find_nearest_neighbors(self):
        self.__txt_scnd.delete(1.0, END)
        name = self.__person1_scnd
        # similarity_scores = {'name':similarity, ...}
        similarity_scores = {}
        for i in self.__users_name:
            if i != name:
                similarity = self.__euclidean_distance(self.__users[name], self.__users[i])
                similarity_scores[i] = similarity
            else:
                similarity_scores[i] = -1
        sorted_hash = sorted(similarity_scores.items(), key=operator.itemgetter(1))
        for i in range(5):
            desired_person = sorted_hash[len(sorted_hash)-i-1]
            self.__txt_scnd.insert(INSERT, "{} : {}\n".format(desired_person[0], desired_person[1]))

    def __find_nearest_neighbors2(self, new_user):
        self.__txt_third.delete(1.0, END)
        # similarity_scores = {'name':similarity, ...}
        similarity_scores = {}
        for i in self.__users_name:
            d = self.__users[i]
            similarity = self.__euclidean_distance(new_user, d)
            similarity_scores[i] = similarity
        # sorted_hash have all people ordered by similarity with new_user.
        # sorted_hash = [('name', similarity), ...]
        sorted_hash = sorted(similarity_scores.items(), key=operator.itemgetter(1))
        for i in range(len(self.__titles)):
            title = self.__titles[i]
            if new_user[title] == 0:
                weighted_sum = 0
                similarity_sum = 0
                for j in range(5):
                    sim = sorted_hash[len(sorted_hash)-j-1][1]  # 5 most similar people
                    all_ratings = self.__users[self.__users_name[j]]
                    rating = all_ratings[title]
                    if rating is not None:
                        weighted_sum += rating*sim
                        similarity_sum += sim
                stars = weighted_sum / similarity_sum
                self.__txt_third.insert(INSERT, "{} : {}\n".format(title, stars))

    def __predict_ratings(self):
        new_user = {}
        for i in range(len(self._drop_downs)):
            title = self.__titles[i]
            rating = self._drop_downs[i].get()
            if rating.lower() == 'not seen':
                rating = 0
            new_user[title] = int(rating)
        # new_user = {'title' = rating, ...}
        self.__find_nearest_neighbors2(new_user)

    #  Functions to manage JSON data
    @staticmethod
    def __get__users_by_name(data):
        users = {}
        for i in range(len(data['users'])):
            users[data['users'][i]['name']] = data['users'][i]
        return users

    @staticmethod
    def __get__users_name(data):
        list = []
        for i in range(len(data['users'])):
            list.append(data['users'][i]['name'])
        return list

    @staticmethod
    def __clean_name_and_timestamp(dict):
        dict.pop('name', None)
        dict.pop('timestamp', None)

    @staticmethod
    def __get__titles(data):
        titles = []
        for i in range(len(data['titles'])):
            titles.append(data['titles'][i])
        return titles

gui = Gui()
