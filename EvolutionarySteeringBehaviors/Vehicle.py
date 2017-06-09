from math import sqrt
import random
import math

mutation_rate = 0.01


class Vehicle:
    def __init__(self, x, y, dna):
        self.velocity = [0, -2]
        self.position = [x, y]
        self.max_speed = 5.5
        self.max_force = 0.9
        self.number_of_food_eated = 0
        self.number_of_poison_eated = 0
        self.health = 1
        if dna is not None:
            self.dna = self.__create_dna(dna)
        else:
            self.dna = []
            self.dna = self.__create_dna(self.dna)

    def __apply_force(self, force, dna_ind):
        if dna_ind != -1:
            for i in range(len(force)):
                force[i] *= self.dna[dna_ind]
        steering_force = self.__truncate(force, self.max_force)
        self.velocity = self.__truncate(self.__add(self.velocity, steering_force), self.max_speed)
        self.position = self.__add(self.position, self.velocity)

    # This method calculates the steering force where:
    # steer = desired - velocity
    def seek(self, target, dna_ind):
        desired_velocity = self.__mult(self.__normalize(self.__sub(target, self.position)), self.max_speed)
        steering_force = self.__sub(desired_velocity, self.velocity)
        self.__apply_force(steering_force, dna_ind)

    def __magnitude(self, vector):
        return sqrt(sum(vector[i]*vector[i] for i in range(len(vector))))

    def __add(self, vect1, vect2):
        assert len(vect1) == len(vect2)
        return [vect1[i]+vect2[i] for i in range(len(vect1))]

    def __sub(self, vect1, vect2):
        assert len(vect1) == len(vect2)
        return [vect1[i]-vect2[i] for i in range(len(vect1))]

    def __mult(self, vect1, value):
        return [vect1[i]*value for i in range(len(vect1))]

    def __normalize(self, vector):
        vect_magnitude = self.__magnitude(vector)
        return [vector[i]/vect_magnitude for i in range(len(vector))]

    def __truncate(self, vector, value):
        magnitude = self.__absolute(vector)
        for i in range(len(magnitude)):
            if magnitude[i] > value:
                vector = self.__mult(self.__mult(vector, value), (1/magnitude[i]))
        return vector

    def __absolute(self, vector):
        return [abs(vector[i]) for i in range(len(vector))]

    def which_is_closest(self, vect, value):
        if len(vect) > 0:
            closest = 100000  # infinity
            closest_index = -1
            for i in range(len(vect)):
                x_food_location = vect[i][0]
                y_food_location = vect[i][1]
                distance = sqrt(math.pow(x_food_location-self.position[0], 2) +
                                math.pow(y_food_location-self.position[1], 2))

                if distance < closest and distance < value:
                    closest = distance
                    closest_index = i
        return closest, closest_index

    def eat(self, vector, index, distance, nutrition, dna_ind):
        element = vector[index]
        if distance < 5:
            if nutrition > 0:
                self.increase_health(nutrition)
                self.number_of_food_eated += 1
            else:
                self.decrease_health(nutrition*-1)
                self.number_of_poison_eated += 1
            vector.remove(element)

        elif dna_ind == 1:  # If what I track isn't food, try to track another thing.
            return vector, element
        elif index > -1:  # If what I track is food, continue tracking that.
            self.seek(vector[index], dna_ind)
        return vector, element

    def decrease_health(self, value):
        self.health -= value

    def increase_health(self, value):
        if self.health + value > 1:
            self.health = 1
        else:
            self.health += value

    def __create_dna(self, dna):
        if len(dna) == 0:
            dna.append(random.uniform(-2, 2))  # Food weight
            dna.append(random.uniform(-2, 2))  # Poison weight
            dna.append(random.uniform(40, 50))  # Food perception
            dna.append(random.uniform(0, 5))  # Poison perception
        else:
            if random.uniform(0, 1) < mutation_rate:
                for i in range(2):
                    dna[i] += random.uniform(-0.1, 0.1)
                dna[2] += random.uniform(-10, 10)
                dna[3] += random.uniform(-1, 1)
        return dna

    # To don't permit vehicle to 'leave' the area (the screen)
    def boundaries(self, width, height):
        dist = 5
        desired = None
        if self.position[0] < dist:
            desired = [self.max_speed, -self.velocity[1]]
        elif self.position[0] < width - dist:
            desired = [-self.max_speed, -self.velocity[1]]

        if self.position[1] < dist:
            desired = [-self.velocity[0], self.max_speed]
        elif self.position[1] > height - dist:
            desired = [-self.velocity[0], -self.max_speed]

        if desired is not None:
            desired = self.__normalize(desired)
            steer = self.__sub(desired, self.velocity)
            self.__apply_force(steer, -1)

    def clone(self):
        if random.uniform(0, 1) > 0.999:
            return Vehicle(self.position[0], self.position[1], self.dna)
        else:
            return None
