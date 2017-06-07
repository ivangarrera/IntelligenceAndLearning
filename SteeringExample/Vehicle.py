import math


class Vehicle:
    def __init__(self, x, y):
        self.acceleration = [0, 0]
        self.velocity = [0, -2]
        self.position = [x, y]
        self.max_speed = 1
        self.max_force = 0.05

    def update_location(self):
        # Update velocity
        self.add_two_vector(self.velocity, self.acceleration)
        # Limit speed
        self.limit(self.velocity, self.max_speed)
        self.add_two_vector(self.position, self.velocity)
        # Reset acceleration
        self.acceleration = [0, 0]

    def apply_force(self, force):
        self.add_two_vector(self.acceleration, force)

    # This method calculates the steering force where:
    # steer = desired - velocity
    def seek(self, target):
        # Substract the target position to the vehicle position
        desired = self.substract_two_vector(target, self.position)
        # Scale to maximum speed
        desired = self.set_magnitude(desired, self.max_speed)
        steer = self.substract_two_vector(desired, self.velocity)
        #self.limit(steer, self.max_force)
        self.apply_force(steer)

    def limit(self, vect, value):
        for i in range(len(vect)):
            if vect[i] > value:
                vect[i] = value


    def add_value_to_vector(self, vect, value):
        for i in range(len(vect)):
            vect[i] += value

    def add_two_vector(self, vect1, vect2):
        assert len(vect1) == len(vect2)
        for i in range(len(vect1)):
            vect1[i] += vect2[i]


    def substract_two_vector(self, vect1, vect2):
        assert len(vect1) == len(vect2)
        for i in range(len(vect1)):
            vect1[i] -= vect2[i]
        return vect1

    def set_magnitude(self, vector, magn):
        if vector[0] != 0 and vector[1] != 0:
            magnitude = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
            new_vx = vector[0] * magn / magnitude
            new_vy = vector[1] * magn / magnitude
            new_vector = [new_vx, new_vy]
            return new_vector
        else:
            return [0, 0]
