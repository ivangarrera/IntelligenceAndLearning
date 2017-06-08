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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
rectangle = pygame.Rect(WIDTH/2, HEIGHT/2, 40, 40)
vehicle_figure = pygame.Rect(300, 300, 15, 15)
vehicle = Vehicle.Vehicle(10, 10)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Draw the rectangle in the mouse position
    rectangle.center = pygame.mouse.get_pos()
    x, y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, DARKGREEN, rectangle)

    # Calculate the new vehicle's position
    vehicle.seek([x, y])
    # vehicle.update_location()
    x_v, y_v = vehicle.position

    # Draw the vehicle in the new position
    vehicle_figure.x = x_v
    vehicle_figure.y = y_v
    vehicle_figure.move_ip(x_v-x, y_v-y)
    pygame.draw.rect(screen, WHITE, vehicle_figure)

    pygame.display.update()

    clock.tick(40)

