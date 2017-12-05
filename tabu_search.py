#!/usr/bin/env python
import test
import numpy as np
import random

class TabuSearch():
    """Class implements tabu search algorithm having cost funtion value"""
    def __init__(self, length_of_solution, initial_solution, initial_fitness,
                 number_of_iterations=10000, tabu_list_length=10, expiration_time=10, type_of_neighborhood=2)
        self.number_of_iterations = number_of_iterations
        self.tabu_list = np.array([], shape=(tabu_list_length, length_of_solution))
        self.tabu_list_time = np.array([], shape=tabu_list_length)
        self.fitness = initial_fitness
        self.solution = initial_solution
        self.expiration_time = expiration_time
        self.type_of_neighborhood = type_of_neighborhood
        # self.aspiration_criteria = False

    def get_tabu_candidate(self):
        """Permutes new neighborhood"""
        index_a_array = np.array([])
        index_b_array = np.array([])
        permutation = self.solution
        for iteration in range(self.type_of_neighborhood):
            index_a = random.randint(0, len(self.solution))
            index_b = random.randint(0, len(self.solution))
            if index_a in index_a_array or index_b in index_b_array:
                iteration = iteration - 1
                continue
            index_a_array.append(index_a)
            index_b_array.append(index_b)
            permutation[index_a], permutation[index_b] = permutation[index_b], permutation[index_a]
        return permutation

    def get_neighbor(self):
        """Permutes new neighborhood excluding ones from tabu list"""
        permutation_find_indicator = False
        while not permutation_find_indicator:
            permutation = get_tabu_candidate()
            for i in range(self.tabu_list.shape[0]):
                if permutation == self.tabu_list[i, :]:
                    continue
            permutation_find_indicator = True
        return permutation

    def update_memory(self, candidate):
        """Add new elements to the list and removes those which are too long"""
        self.tabu_list_time = self.tabu_list_time + 1
        self.tabu_list_time.append(1)
        self.tabu_list.append(candidate)
        for index in len(self.tabu_list_time):
            if self.tabu_list_time[index] >= self.expiration_time:
                self.tabu_list = np.delete(self.tabu_list, index, axis=0)
                self.tabu_list_time = np.delete(self.tabu_list_time, index)

    def run(self):
        """Main method which searches for optimal solution"""
        for _ in range(self.number_of_iterations):
            best_candidate = self.get_neighbor()
            tabu_candidate = self.get_tabu_candidate()
            if test.obj_function(best_candidate, distance_array, times_array, tmin) < self.fitness:
                self.solution = best_candidate
                self.fitness = test.obj_function(best_candidate, distance_array, times_array, tmin)
            if test.obj_function(tabu_candidate, distance_array, times_array, tmin) < self.fitness:
                best_candidate = tabu_candidate
                self.solution = tabu_candidate
                self.fitness = test.obj_function(tabu_candidate, distance_array, times_array, tmin)
            self.update_memory(best_candidate)