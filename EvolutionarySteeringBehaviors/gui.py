import pygame, sys
import random
import Vehicle
from colour import Color

# CONSTANTS

#             R    G    B
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKGREEN = (  0, 155,   0)
BGCOLOR   = BLACK

WIDTH           = 700
HEIGHT          = 700
NUM_FOOD        = 500
NUM_POISON      = 30
NUM_VEHICLES    = 1000
food            = []
poison          = []
figures         = []
poison_figures  = []
vehicles        = []
vehicles_figures = []

screen = pygame.display.set_mode((WIDTH, HEIGHT))

green = Color("LightBlue")
colors = list(green.range_to(Color("BlueViolet"), 10))


class Text:
    def __init__(self, FontName=None, FontSize=25):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        text = text
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size


class Gui:
    def __init__(self, food, poison, figures, poison_figures, screen, vehicles, vehicles_figures):
        pygame.mixer.init()
        pygame.init()
        text = Text()

        # Create food rectangle objects
        self.create_rectangles(food, NUM_FOOD)

        # Create poison rectangle objects
        self.create_rectangles(poison, NUM_POISON)

        # Create vehicle rectangle objects
        for i in range(NUM_VEHICLES):
            x = random.uniform(0, WIDTH)
            y = random.uniform(0, HEIGHT)
            vehicles.append(Vehicle.Vehicle(x, y, None))

        clock = pygame.time.Clock()
        self.draw_vehicles()

        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            screen.fill(BLACK)

            # Renovate food, approximately each 25% of time
            if random.uniform(0, 1) > 0.75:
                x = random.uniform(0, WIDTH)
                y = random.uniform(0, HEIGHT)
                food.append([x, y])

            # Renovate poison, approximately each 5% of time
            if random.uniform(0, 1) > 0.95:
                x = random.uniform(0, WIDTH)
                y = random.uniform(0, HEIGHT)
                poison.append([x, y])

            # Perform the action for all vehicles
            if len(vehicles) > 0:
                for i in range(len(vehicles)):
                    if vehicles[i].health > 0:
                        # Decrease health periodically
                        vehicles[i].decrease_health(0.005)

                        # Calculate the nearest target (food or poison). We have on count the perceptions
                        # (how far can the vehicle perceive the food or poison)
                        best_food_distance, index = vehicles[i].which_is_closest(food, vehicles[i].dna[2])
                        best_poison_distance, ind = vehicles[i].which_is_closest(poison, vehicles[i].dna[3])

                        if best_food_distance < best_poison_distance:
                            vehicles[i].boundaries(WIDTH, HEIGHT)
                            food, element = vehicles[i].eat(food, index, best_food_distance, 0.1, 0)
                        else:
                            poison, element = vehicles[i].eat(poison, ind, best_poison_distance, -0.3, 1)

                        # Calculate the new vehicle's position
                        vehicles[i].seek(element, -1)
                        x_v, y_v = vehicles[i].position

                        # Draw the vehicle in the new position
                        vehicles_figures[i].x = x_v
                        vehicles_figures[i].y = y_v
                        vehicles_figures[i].move_ip(x_v - element[0], y_v - element[1])

                        # Append a child vehicle?
                        child_vehicle = vehicles[i].clone()
                        if child_vehicle is not None:
                            vehicles.append(child_vehicle)

                    else:  # Not health enough. Vehicle broken.
                        vehicles.remove(vehicles[i])
                        break
            else:
                print("All vehicles are broken")
                exit(0)

            # Clear list, because can causes overwrites.
            figures.clear()
            vehicles_figures.clear()
            poison_figures.clear()

            # Draw the eat
            self.draw_eat()

            # Draw the poison
            self.draw_poison()

            self.draw_vehicles()

            # Display the text
            number_of_food = 0
            number_of_poison = 0
            for i in range(len(vehicles)):
                number_of_food += vehicles[i].number_of_food_eated
                number_of_poison += vehicles[i].number_of_poison_eated

            text.render(screen, "Food eated --> {}".format(number_of_food), (255, 255, 255), (0, 0))
            text.render(screen, "Poison eated --> {}".format(number_of_poison), (255, 255, 255), (0, 20))

            pygame.display.update()

            clock.tick(100)

    # Methods

    def draw_eat(self):
        for j in range(len(food)):
            figures.append(pygame.Rect(food[j][0], food[j][1], 7, 7))
            pygame.draw.rect(screen, DARKGREEN, figures[j])

    def draw_poison(self):
        for i in range(len(poison)):
            poison_figures.append(pygame.Rect(poison[i][0], poison[i][1], 7, 7))
            pygame.draw.rect(screen, RED, poison_figures[i])

    def draw_vehicles(self):
        for i in range(len(vehicles)):
            vehicles_figures.append(pygame.Rect(vehicles[i].position[0], vehicles[i].position[1], 15, 15))
            color = colors[int(vehicles[i].health * 10 - 1)]
            _red = 255 - color.get_rgb()[0]*255
            _green = 255 - color.get_rgb()[1]*255
            _blue = color.get_rgb()[2]*255
            color = (_red, _green, _blue)
            pygame.draw.rect(screen, color, vehicles_figures[i])

    def create_rectangles(self, list, num_elments):
        for i in range(num_elments):
            x = random.uniform(0, WIDTH)
            y = random.uniform(0, HEIGHT)
            list.append([x, y])

gui = Gui(food, poison, figures, poison_figures, screen, vehicles, vehicles_figures)
