from math import sqrt
import random
import pygame
import math


class Vehicle:
    def __init__(self, x, y):
        self.velocity = [0, -2]
        self.position = [x, y]
        self.max_speed = 5.5
        self.max_force = 0.9
        self.health = 1
        self.dna = []
        self.dna = self.create_dna(self.dna)

    def apply_force(self, force, dna_ind):
        if dna_ind != -1:
            for i in range(len(force)):
                force[i] *= self.dna[dna_ind]
        steering_force = self.truncate(force, self.max_force)
        self.velocity = self.truncate(self.add(self.velocity, steering_force), self.max_speed)
        self.position = self.add(self.position, self.velocity)

    # This method calculates the steering force where:
    # steer = desired - velocity
    def seek(self, target, dna_ind):
        desired_velocity = self.mult(self.normalize(self.sub(target, self.position)), self.max_speed)
        steering_force = self.sub(desired_velocity, self.velocity)
        self.apply_force(steering_force, dna_ind)

    def magnitude(self, vector):
        return sqrt(sum(vector[i]*vector[i] for i in range(len(vector))))

    def add(self, vect1, vect2):
        assert len(vect1) == len(vect2)
        return [vect1[i]+vect2[i] for i in range(len(vect1))]

    def sub(self, vect1, vect2):
        assert len(vect1) == len(vect2)
        return [vect1[i]-vect2[i] for i in range(len(vect1))]

    def mult(self, vect1, value):
        return [vect1[i]*value for i in range(len(vect1))]

    def normalize(self, vector):
        vect_magnitude = self.magnitude(vector)
        return [vector[i]/vect_magnitude for i in range(len(vector))]

    def truncate(self, vector, value):
        magnitude = self.absolute(vector)
        for i in range(len(magnitude)):
            if magnitude[i] > value:
                vector = self.mult(self.mult(vector, value), (1/magnitude[i]))
        return vector

    def absolute(self, vector):
        return [abs(vector[i]) for i in range(len(vector))]

    def which_is_closest(self, vect):
        if len(vect) > 0:
            closest = 100000  # infinity
            closest_index = -1
            for i in range(len(vect)):
                x_food_location = vect[i][0]
                y_food_location = vect[i][1]
                distance = sqrt(math.pow(x_food_location-self.position[0], 2) +
                                math.pow(y_food_location-self.position[1], 2))

                if distance < closest:
                    closest = distance
                    closest_index = i
        return closest, closest_index

    def eat(self, vector, index, distance, nutrition, dna_ind):
        element = vector[index]
        if distance < 5:
            if nutrition > 0:
                self.increase_health(nutrition)
            else:
                self.decrease_health(nutrition*-1)
            vector.remove(element)

        elif index > -1:
            self.seek(vector[index], dna_ind)
        return vector, element

    def draw_vehicle(self, screen, color, rect):
        pygame.draw.rect(screen, color, rect)

    def decrease_health(self, value):
        self.health -= value

    def increase_health(self, value):
        if self.health + value > 1:
            self.health = 1
        else:
            self.health += value

    def create_dna(self, dna):
        dna.append(random.uniform(-2, 2))  # Food weight
        dna.append(random.uniform(-2, 2))  # Poison weight
        dna.append(random.uniform(10, 100))  # Food perception
        dna.append(random.uniform(10, 100))  # Poison perception
        return dna

    # To don't permit vehicle to 'leave' the area (the screen)
    def boundaries(self, width, height):
        dist = 10
        desired = None
        if self.position[0] < dist:
            desired = [self.max_speed, self.velocity[1]]
        elif self.position[0] < width - dist:
            desired = [-self.max_speed, self.velocity[1]]

        if self.position[1] < dist:
            desired = [self.velocity[0], self.max_speed]
        elif self.position[1] > height - dist:
            desired = [self.velocity[0], -self.max_speed]

        if desired is not None:
            desired = self.normalize(desired)
            steer = self.sub(desired, self.velocity)
            steer = self.truncate(steer, self.max_force)
            self.apply_force(steer, -1)

    """def behaviors(self, good, bad):
        steer_force_good = self.eat(vector, index, distance, nutrition)"""