#!/usr/bin/env python
from obj_function import ObjectiveFun
import numpy as np
import random

class TabuSearch():
    """Class implements tabu search algorithm having cost funtion value"""
    def __init__(self, file_name, initial_solution, initial_fitness,
                 number_of_iterations=100, tabu_list_length=10, 
                 expiration_time=10, type_of_neighborhood=2):
        self.OF = ObjectiveFun(file_name, 3)
        self.number_of_iterations = number_of_iterations
        self.tabu_list = np.zeros(shape=(tabu_list_length, len(initial_solution)), dtype=int)
        self.tabu_list_indicator = 0
        self.tabu_list_time = np.zeros(shape=tabu_list_length, dtype=int)
        self.tabu_list_time_indicator = 0
        self.fitness = initial_fitness
        self.solution = initial_solution
        self.expiration_time = expiration_time
        self.type_of_neighborhood = int(type_of_neighborhood / 2)
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
            index_a_array = np.append(index_a_array, index_a)
            index_b_array = np.append(index_b_array, index_b)
            permutation[index_a], permutation[index_b] = permutation[index_b], permutation[index_a]
        return permutation

    def get_neighbor(self):
        """Permutes new neighborhood excluding ones from tabu list"""
        permutation_find_indicator = False
        while not permutation_find_indicator:
            permutation = self.get_tabu_candidate()
            for i in range(self.tabu_list.shape[0]):
                if np.array_equal(permutation, self.tabu_list[i, :]):
                    continue
            permutation_find_indicator = True
        return permutation

    def update_memory(self, candidate):
        """Add new elements to the list and removes those which are too long"""
        self.tabu_list_time = self.tabu_list_time + 1
        self.tabu_list_time = np.append(self.tabu_list_time, 1)
        # if len(self.tabu_list) == 
        self.tabu_list = np.append(self.tabu_list, candidate)
        for index in range(len(self.tabu_list_time)):
            if self.tabu_list_time[index] >= self.expiration_time:
                self.tabu_list = np.delete(self.tabu_list, index, axis=0)
                self.tabu_list_time = np.delete(self.tabu_list_time, index)

    def run(self):
        """Main method which searches for optimal solution"""
        for i in range(self.number_of_iterations):
            print(i)
            best_candidate = self.get_neighbor()
            # print(best_candidate)
            tabu_candidate = self.get_tabu_candidate()
            # print(tabu_candidate)
            if self.OF.obj_function(best_candidate) < self.fitness:
                self.solution = best_candidate
                self.fitness = self.OF.obj_function(best_candidate)
            if self.OF.obj_function(tabu_candidate) < self.fitness:
                best_candidate = tabu_candidate
                self.solution = tabu_candidate
                self.fitness = self.OF.obj_function(tabu_candidate)
            print(best_candidate)
            self.update_memory(best_candidate)
