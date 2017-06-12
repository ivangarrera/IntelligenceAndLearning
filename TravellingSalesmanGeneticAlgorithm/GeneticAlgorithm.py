import math
from random import uniform


class GeneticAlgorithm:
    def __init__(self, cities, fitness, population):
        self.cities = cities
        self.fitness = fitness
        self.population = population

    #  Calculates the distances in a given order (population[index])
    def calculateFitness(self, best_ever, record_distance, current_distance, current_best):
        rd = record_distance
        infinity = 10000000
        for i in range(len(self.population)):
            d = self.calc_distances(self.cities, self.population[i])
            if d < record_distance:
                record_distance = d
                best_ever = self.population[i]
            if d < infinity:
                current_distance = d
                current_best = self.population[i]
        if d < rd:
            self.fitness.clear()
            self.fitness.append(d)

        # Returns the best order and the current order
        return best_ever, record_distance, current_best, current_distance

    def normalize_fitness(self):
        sum = 0
        for i in range(len(self.fitness)):
            sum += self.fitness[i]
        for i in range(len(self.fitness)):
            self.fitness[i] = self.fitness[i] / sum

    #  Generates a new population
    def next_generation(self):
        new_population = []
        for i in range(len(self.population)):
            #  Pick one random order and swap its components
            order_a = self.pick_one(self.population, self.fitness)
            order_b = self.pick_one(self.population, self.fitness)
            order = self.crossover(order_a, order_b)
            self.mutate(order, 0.01)
            new_population.append(order.copy())
        self.population = new_population

    # This method merges two order vectors, to implement evolutionary behaviors
    def crossover(self, order_a, order_b):
        start = math.floor(uniform(0, len(order_a)))
        end = math.floor(uniform(start+1, len(order_a)))
        new_order = order_b[start:end]
        for i in range(len(order_b)):
            if order_b[i] not in new_order:
                new_order.append(order_b[i])
        return new_order

    #  Pick a random element from the list
    def pick_one(self, list, probability):
        index = 0
        r = uniform(0, 1)
        while r > 0:
            r -= probability[index]
            index += 1
        index -= 1
        return list[index]

    #  Calculates the total sum of the partial sums of distances between points
    def calc_distances(self, points, order):
        sum = 0
        for i in range(len(order) - 1):
            index_city_a = order[i]
            index_city_b = order[i + 1]
            city_a = points[index_city_a]
            city_b = points[index_city_b]
            distance = math.sqrt(math.pow((city_b[0] - city_a[0]), 2) +
                                 math.pow((city_b[1] - city_a[1]), 2))
            sum += distance
        return sum

    #  Swap a random number of times between 0 and the number of cities
    def mutate(self, order, mutation_rate):
        for i in range(len(self.cities)):
            if uniform(0, 1) < mutation_rate:
                indexA = math.floor(uniform(0, len(order)))
                indexB = math.floor(uniform(0, len(order)))
                aux = order[indexA]
                order[indexA] = order[indexB]
                order[indexB] = aux