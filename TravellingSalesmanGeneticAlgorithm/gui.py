import pygame
import sys
import GeneticAlgorithm
import random

BLACK = (0, 0, 0)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 700
HEIGHT = 700
cities = []
symmetric_cities = []
total_cities = 15
order = []
city_figures = []
symmetric_city_figures = []

population_length = 500
population = []
fitness = []

screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Gui:
    def __init__(self, screen):
        self.recordDistance = 1000000000
        self.bestEver = []
        self.currentDistance = 100000000
        self.currentBest = []

        pygame.init()

        self.create_cities_and_order()
        self.calculate_symmetric_points()
        self.create_random_population()

        ga = GeneticAlgorithm.GeneticAlgorithm(cities, fitness, population)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            self.create_city_figures()
            self.create_symmetrical_city_figures()

            # Calculate best path accord a population
            self.bestEver, self.recordDistance, self.currentBest, self.currentDistance = \
                ga.calculateFitness(self.bestEver, self.recordDistance, self.currentDistance, self.currentBest)
            ga.normalize_fitness()
            self.draw(cities, self.bestEver, city_figures)
            self.draw(symmetric_cities, self.currentBest, symmetric_city_figures)

            # Generate a distinct population
            ga.next_generation()
            pygame.display.update()

    def calculate_symmetric_points(self):
        for i in range(len(cities)):
            symmetrical_y = cities[i][1] + (HEIGHT/2)
            symmetric_cities.append([cities[i][0], symmetrical_y])

    def draw(self, vect, order, figures):
        for i in range(len(vect)):
            pygame.draw.rect(screen, RED, figures[i])
        for i in range(len(order)-1):
            pygame.draw.line(screen, WHITE, (vect[order[i]][0], vect[order[i]][1]),
                             (vect[order[i+1]][0], vect[order[i+1]][1]))

    def create_cities_and_order(self):
        for i in range(total_cities):
            x = random.uniform(0, WIDTH)
            y = random.uniform(0, HEIGHT/2)
            cities.append([x, y])
            order.append(i)

    def create_random_population(self):
        for i in range(population_length):
            population.append(random.sample(order, len(order)))  # Shuffle the elements

    def create_city_figures(self):
        for i in range(len(cities)):
            city_figures.append(pygame.Rect(cities[i][0], cities[i][1], 7, 7))

    def create_symmetrical_city_figures(self):
        for i in range(len(symmetric_cities)):
            symmetric_city_figures.append(pygame.Rect(symmetric_cities[i][0], symmetric_cities[i][1], 7, 7))

# Program execution
gui = Gui(screen)






