#!/usr/bin/env python
import obj_function
import numpy as np
import random
import matplotlib.pyplot as plt

class TabuSearch():
    """Class implements tabu search algorithm having cost funtion value"""
    def __init__(self, file_name, init_solution, init_objective_fun_value, stats_every_iteration,
                 number_of_iterations, tabu_list_length, type_of_neighborhood,
                 t_min, point_number, number_of_tools):
        self.OF = obj_function.ObjectiveFun(file_name, t_min, point_number, number_of_tools)
        self.number_of_iterations = number_of_iterations
        self.tabu_list = np.array([], dtype=int)
        self.tabu_list_length = tabu_list_length
        self.objective_fun_value = init_objective_fun_value
        self.solution = init_solution
        self.solution_length = len(self.solution)
        self.type_of_neighborhood = type_of_neighborhood
        self.all_objective_fun_value = np.array([])
        self.stats_every_iteration = stats_every_iteration
        # self.aspiration_criteria = False

    def get_tabu_candidate(self):
        """Permutes new neighborhood"""
        index_a_array = np.array([])
        index_b_array = np.array([])
        permutation = np.copy(self.solution)
        for iteration in range(self.type_of_neighborhood):
            index_a = random.randint(0, len(self.solution) - 1)
            index_b = random.randint(0, len(self.solution) - 1)
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
        self.tabu_list = self.tabu_list.reshape(len(self.tabu_list) // self.solution_length, self.solution_length)
        while not permutation_find_indicator:
            permutation = self.get_tabu_candidate()
            for i in range(self.tabu_list.shape[0]):
                if np.array_equal(permutation, self.tabu_list[i, :]):
                    continue
            permutation_find_indicator = True
        return permutation

    def update_memory(self, candidate):
        """Add new elements to the tabu list and removes those which are too long"""
        self.tabu_list = np.append(self.tabu_list, candidate)
        if self.tabu_list.reshape(len(self.tabu_list) // self.solution_length, self.solution_length).shape[0] >= self.tabu_list_length:
            delete_vector = [i for i in range(self.solution_length)]
            self.tabu_list = np.delete(self.tabu_list, delete_vector)

    def run(self):
        """Main method which searches for optimal solution"""
        for i in range(self.number_of_iterations):
            self.all_objective_fun_value = np.append(self.all_objective_fun_value, self.objective_fun_value)
            best_candidate = self.get_neighbor()
            tabu_candidate = self.get_tabu_candidate()
            # print("best generated: "+str(best_candidate))
            # print("tabu generated: "+str(tabu_candidate))

            if self.OF.obj_function(best_candidate) < self.objective_fun_value:
                self.solution = best_candidate
                self.objective_fun_value = self.OF.obj_function(best_candidate)
                print(best_candidate)
                print("best "+str(i))
            if self.OF.obj_function(tabu_candidate) < self.objective_fun_value:
                best_candidate = tabu_candidate
                self.solution = tabu_candidate
                self.objective_fun_value = self.OF.obj_function(tabu_candidate)
                print(tabu_candidate)
                print("tabu "+str(i))
            self.update_memory(best_candidate)
            if self.stats_every_iteration == True:
                print("Iteration number: " + str(i + 1))
                print("Solution: \n" + str(self.solution))
                print("Objective function value: " + str(self.objective_fun_value), end="\n\n")

    def show_objective_fun_value_plot(self):
        """Display plot of all objective_fun_valuees"""
        plt.plot(self.all_objective_fun_value)
        plt.xlabel('Number of iteration')
        plt.ylabel('Value')
        plt.title('Objective function value')
        plt.show()
