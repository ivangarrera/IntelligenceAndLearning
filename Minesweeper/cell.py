import pygame
import os


class Cell:
    def __init__(self, i, j, width, number_cells):
        self.__revealed = False
        self.i = i
        self.j = j
        self.x = int(i*width)
        self.y = int(j*width)
        self.cells = []
        self.__width = width
        self.number_cells = number_cells
        self.neighbor_count = 0
        self.mine = False
        self.mine_image = pygame.image.load(os.path.join("mine_v3.png"))

    def show(self, screen):
        if self.__revealed is not True:  # Don't load the image more than once on each cell
            self.__revealed = True
            if self.mine:
                rect = pygame.Rect((self.x, self.y, self.__width - 1, self.__width - 1))
                pygame.draw.rect(screen, (211, 211, 211), rect)
                self.mine_image.convert()
                screen.blit(self.mine_image, (self.x+int(self.__width/4), self.y+int(self.__width/4)))
                self.__game_over(screen)
            else:
                rect = pygame.Rect((self.x, self.y, self.__width-1, self.__width-1))
                pygame.draw.rect(screen, (192, 192, 192), rect)
                mines = self.neighbor_count
                if mines > 0:
                    font = pygame.font.Font(None, 40)
                    msg = font.render(str(mines), 1, (0, 0, 0))
                    screen.blit(msg, (self.x+int(self.__width/4), self.y+int(self.__width/4)))
                else:
                    self.flood_fill(screen)

    def flood_fill(self, screen):
        for i_offset in range(-1, 2):
            for j_offset in range(-1, 2):
                new_i = self.i+i_offset
                new_j = self.j+j_offset
                if -1 < new_i < self.number_cells and -1 < new_j < self.number_cells:
                    neighbor = self.__find_cell(new_i, new_j)
                    if not neighbor.mine:
                        neighbor.show(screen)

    def __find_cell(self, i_par, j_par):
        for i in self.cells:
            if i.i == i_par and i.j == j_par:
                return i

    def __game_over(self, screen):
        for i in self.cells:
            i.show(screen)