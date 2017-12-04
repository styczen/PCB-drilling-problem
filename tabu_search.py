#!/usr/bin/env python
import numpy as np

class TabuSearch():
    """Class implements tabu search algorithm having cost funtion value"""
    def __init__(self, length_of_solution, initial_solution, initial_fitness,
                 number_of_iterations=10000, tabu_list_length=10, expiration_time=10):
        self.number_of_iterations = number_of_iterations
        self.tabu_list = np.array([], shape=(tabu_list_length, length_of_solution))
        self.tabu_list_time = np.array([], shape=tabu_list_length)
        self.fitness = initial_fitness
        self.solution = initial_solution
        self.expiration_time = expiration_time
        # self.aspiration_criteria = False

    def get_neighbor(self):
        """Permutes new neighborhood"""
        return np.array([], shape=(1, self.solution.shape[1]))

    def get_tabu_candidate(self):
        """Permutes new neighborhood"""
        return np.array([], shape=(1, self.solution.shape[1]))

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
            if Q(best_candidate) < self.fitness:
                self.solution = best_candidate
                self.fitness = Q(best_candidate)
            if Q(tabu_candidate) < self.fitness:
                best_candidate = tabu_candidate
                self.solution = tabu_candidate
                self.fitness = Q(tabu_candidate)
            self.update_memory(best_candidate)