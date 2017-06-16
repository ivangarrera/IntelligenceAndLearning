import pygame
import sys
import math


class Gui:
    def __init__(self):
        self.__WIDTH = 700
        self.__HEIGHT = 700
        self.__data = []
        self.__slope = 1
        self.__intersection_with_Y_axis = 0
        self.__screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__caption = pygame.display.set_caption("Linear Regression Rect Calculation")

        pygame.init()

        while True:
            self.__screen.fill((192, 192, 192))  # Re-fill screen to eliminate old lines
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button_states = pygame.mouse.get_pressed()  # Left mouse button
                    if button_states[0] == 1:
                        point = (event.pos[0], event.pos[1])
                        self.__data.append(point)

            # Calculate and draw linear regression rect
            if len(self.__data) > 1:
                self.__slope, self.__intersection_with_Y_axis = self.__linear_regression()
                self.__draw_regression_rect()

            self.__print_data()
            pygame.display.update()

    def __draw_regression_rect(self):
        x1 = self.__WIDTH
        x2 = 0
        y1 = self.__slope * x1 + self.__intersection_with_Y_axis
        y2 = self.__slope * x2 + self.__intersection_with_Y_axis
        pygame.draw.line(self.__screen, (0, 0, 255), (x1, y1), (x2, y2))

    def __linear_regression(self):
        #  Calculate the average
        xsum = 0
        ysum = 0
        for i in self.__data:
            xsum += i[0]
            ysum += i[1]
        mean_x = xsum/len(self.__data)
        mean_y = ysum/len(self.__data)
        #  Calculate the slope of the rect
        numerator = 0
        denominator = 0
        for i in self.__data:
            numerator += (i[0] - mean_x)*(i[1] - mean_y)
            denominator += math.pow(i[0]-mean_x, 2)
        m = numerator/denominator if denominator != 0 else -1
        b = mean_y - (mean_x * m)
        return m, b

    def __print_data(self):
        for i in self.__data:
            rect = pygame.Rect(i[0], i[1], 7, 7)
            pygame.draw.rect(self.__screen, (255, 0, 0), rect)

gui = Gui()
