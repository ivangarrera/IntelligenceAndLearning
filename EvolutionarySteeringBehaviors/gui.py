import pygame, sys
import random
from pygame.locals import *
import Vehicle

pygame.mixer.init()
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR   = BLACK

pygame.init()

WIDTH = 500
HEIGHT = 400
NUM_FOOD = 30
food = []

screen = pygame.display.set_mode((WIDTH, HEIGHT))
vehicle_figure = pygame.Rect(0, 0, 15, 15)
vehicle = Vehicle.Vehicle(100, 100)

figures = []

for i in range(NUM_FOOD):
    x = random.uniform(0, WIDTH)
    y = random.uniform(0, HEIGHT)
    food.append([x, y])


def draw_eat():
    for j in range(len(food)):
        figures.append(pygame.Rect(food[j][0], food[j][1], 7, 7))
        pygame.draw.rect(screen, DARKGREEN, figures[j])

clock = pygame.time.Clock()
draw_eat()
pygame.display.update()
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    screen.fill(BLACK)
    pygame.draw.rect(screen, BGCOLOR, vehicle_figure)

    # Calculate the new vehicle's position
    index = vehicle.eat(food)
    vehicle.seek(food[index])
    x_v, y_v = vehicle.position

    # Print the food
    for i in range(NUM_FOOD):
        rec = figures[i]
        pygame.draw.rect(screen, DARKGREEN, rec)

    # Draw the vehicle in the new position
    vehicle_figure.x = x_v
    vehicle_figure.y = y_v
    vehicle_figure.move_ip(x_v - food[index][0], y_v - food[index][1])
    pygame.draw.rect(screen, WHITE, vehicle_figure)

    pygame.display.update()

    clock.tick(60)

