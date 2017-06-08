from math import sqrt
import math


class Vehicle:
    def __init__(self, x, y):
        self.velocity = [0, -2]
        self.position = [x, y]
        self.max_speed = 5.5
        self.max_force = 0.9

    def apply_force(self, force):
        steering_force = self.truncate(force, self.max_force)
        self.velocity = self.truncate(self.add(self.velocity, steering_force), self.max_speed)
        self.position = self.add(self.position, self.velocity)

    # This method calculates the steering force where:
    # steer = desired - velocity
    def seek(self, target):
        desired_velocity = self.mult(self.normalize(self.sub(target, self.position)), self.max_speed)
        steering_force = self.sub(desired_velocity, self.velocity)
        self.apply_force(steering_force)

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

    def eat(self, food):
        closest = 100000  # infinity
        closest_index = -1
        for i in range(len(food)):
            x_food_location = food[i][0]
            y_food_location = food[i][1]
            distance = sqrt(math.pow(x_food_location-self.position[0], 2) +
                            math.pow(y_food_location-self.position[1], 2))
            if distance < closest:
                closest = distance
                closest_index = i

        return closest_index


