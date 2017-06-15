import pygame
import cell
import sys
import random


class Gui:
    def __init__(self):
        self.__WIDTH = 750
        self.__HEIGHT = 750
        self.__R_WIDTH = self.__WIDTH/15
        self.__NUMBER_RECTS = 12
        self.__NUMBER_OF_MINES = 25
        self.__screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__caption = pygame.display.set_caption("MINESWEEPER")
        self.__cell = self.__create_cell()
        pygame.init()
        self.set_cells_attribute()
        self.__create_mines()
        self.__do_neighbor_count()

        # Grid is loaded only once
        self.__screen.fill((255, 255, 255))
        self.__draw_rectangles()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button_states = pygame.mouse.get_pressed()
                    if button_states[0] == 1:  # If left button is pressed on the mouse
                        self.__cell_pressed(event.pos[0], event.pos[1])

            pygame.display.update()

    def __draw_rectangles(self):
        if int(self.__NUMBER_RECTS*self.__R_WIDTH) > self.__WIDTH:
            self.__NUMBER_RECTS = int(self.__WIDTH/self.__R_WIDTH)+1

        for i in range(self.__NUMBER_RECTS):
            for j in range(self.__NUMBER_RECTS):
                rect = pygame.Rect((self.__R_WIDTH*i, self.__R_WIDTH*j,
                                    self.__R_WIDTH, self.__R_WIDTH))
                rect2 = pygame.Rect(self.__R_WIDTH*i, self.__R_WIDTH*j,
                                    self.__R_WIDTH-2, self.__R_WIDTH-1)
                pygame.draw.rect(self.__screen, (0, 0, 0), rect)
                pygame.draw.rect(self.__screen, (255, 255, 255), rect2)

    def __create_cell(self):
        cells = []
        for i in range(self.__NUMBER_RECTS):
            for j in range(self.__NUMBER_RECTS):
                cells.append(cell.Cell(i, j, self.__R_WIDTH, self.__NUMBER_RECTS))
        return cells

    def set_cells_attribute(self):
        for i in range(len(self.__cell)):
            self.__cell[i].cells = self.__cell

    def __cell_pressed(self, x, y):
        for i in range(len(self.__cell)):
            if self.__cell[i].x < x < self.__cell[i].x + self.__R_WIDTH \
                    and self.__cell[i].y < y < self.__cell[i].y + self.__R_WIDTH:
                self.__cell[i].show(self.__screen)

    def __find_cell(self, i_par, j_par):
        for i in self.__cell:
            if i.i == i_par and i.j == j_par:
                return i

    def __create_mines(self):
        options = []
        for i in range(self.__NUMBER_RECTS):
            for j in range(self.__NUMBER_RECTS):
                options.append((i, j))

        for n in range(self.__NUMBER_OF_MINES):
            index = int(random.uniform(0, len(options)))
            element = options[index]
            cell = self.__find_cell(element[0], element[1])
            cell.mine = True
            options.remove(element)

    def __do_neighbor_count(self):
        for cell in self.__cell:
            if cell.mine:
                cell.neighbor_count = -1
            else:
                number_of_mines = 0
                for i_offset in range(-1, 2):
                    for j_offset in range(-1, 2):
                        new_i = cell.i+i_offset
                        new_j = cell.j+j_offset
                        if -1 < new_i < cell.number_cells and -1 < new_j < cell.number_cells:
                            new_cell = self.__find_cell(new_i, new_j)
                            if new_cell is not None:
                                if new_cell.mine:
                                    number_of_mines += 1
                            else:
                                continue
            cell.neighbor_count = number_of_mines


gui = Gui()


