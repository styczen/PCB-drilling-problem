#!/usr/bin/env python
import obj_function
import numpy as np
import random
import matplotlib.pyplot as plt
import datetime
import csv
import timeit

class TabuSearch():
    """Class implements tabu search algorithm having cost funtion value"""
    def __init__(self, file_name, init_solution, init_objective_fun_value, stats_every_iteration,
                 number_of_iterations, tabu_list_length, type_of_neighborhood,
                 t_min, point_number, number_of_tools, seed, fig_number):
        self.OF = obj_function.ObjectiveFun(file_name, t_min, point_number, number_of_tools)
        self.number_of_iterations = number_of_iterations
        self.early_break = False
        self.true_iter = 0
        self.tabu_list = np.array([], dtype=int)
        self.tabu_list_length = tabu_list_length
        self.objective_fun_value = init_objective_fun_value
        self.solution = init_solution
        self.solution_length = len(self.solution)
        self.type_of_neighborhood = type_of_neighborhood
        self.all_objective_fun_value_best = np.array([])
        self.all_objective_fun_value_tabu_candidate = np.array([])
        self.all_objective_fun_value_best_candidate = np.array([])
        self.stats_every_iteration = stats_every_iteration
        self.time = 0
        self.seed = seed
        self.fig_number = fig_number
        random.seed(seed)
        # self.aspiration_criteria = False

    def get_tabu_candidate(self):
        """Permutes new neighborhood"""
        permutation = np.copy(self.solution)
        for iteration in range(self.type_of_neighborhood):
            index_a = random.randint(0, len(self.solution) - 1)
            index_b = random.randint(0, len(self.solution) - 1)
            permutation[index_a], permutation[index_b] = permutation[index_b], permutation[index_a]
        return permutation

    def get_neighbor(self):
        """Permutes new neighborhood excluding ones from tabu list"""
        self.tabu_list = self.tabu_list.reshape(len(self.tabu_list) // self.solution_length, self.solution_length)
        permutation_find_indicator = False
        while not permutation_find_indicator:
            permutation = self.get_tabu_candidate()
            for i in range(self.tabu_list.shape[0]):
                if np.array_equal(permutation, self.tabu_list[i, :]):
                    break
            else:
                permutation_find_indicator = True
        return permutation

    def update_memory(self, candidate):
        """Add new elements to the tabu list and removes those which are too long"""
        self.tabu_list = np.append(self.tabu_list, candidate)
        if len(self.tabu_list) // self.solution_length > self.tabu_list_length:
            delete_vector_indices = [i for i in range(self.solution_length)]
            self.tabu_list = np.delete(self.tabu_list, delete_vector_indices)

    def run(self):
        """Main method which searches for optimal solution; ends when objective function value does not change for 10000 iterations"""
        end_indicator = 0
        prev_value = self.objective_fun_value
        start = timeit.default_timer()
        for i in range(self.number_of_iterations):
            self.all_objective_fun_value_best = np.append(self.all_objective_fun_value_best, self.objective_fun_value)
            best_candidate = self.get_neighbor()
            tabu_candidate = self.get_tabu_candidate()

            temp_obj_best_candidate = self.OF.obj_function(best_candidate)
            self.all_objective_fun_value_best_candidate = np.append(self.all_objective_fun_value_best_candidate, temp_obj_best_candidate)
            if temp_obj_best_candidate < self.objective_fun_value:
                self.solution = best_candidate
                self.objective_fun_value = temp_obj_best_candidate

            temp_obj_tabu_candidate = self.OF.obj_function(tabu_candidate)
            self.all_objective_fun_value_tabu_candidate = np.append(self.all_objective_fun_value_tabu_candidate, temp_obj_tabu_candidate)
            if temp_obj_tabu_candidate < self.objective_fun_value:
                best_candidate = tabu_candidate
                self.solution = tabu_candidate
                self.objective_fun_value = temp_obj_tabu_candidate

            self.update_memory(best_candidate)

            if self.stats_every_iteration == True:
                print("Iteration number: " + str(i + 1))
                print("Solution: \n" + str(self.solution))
                print("Objective function value: " + str(self.objective_fun_value), end="\n\n")

            if (self.objective_fun_value == prev_value):
                end_indicator = end_indicator + 1
            else:
                end_indicator = 0

            if (end_indicator == 10000):
                self.true_iter = i
                self.early_break = True
                break
            prev_value = self.objective_fun_value
        stop = timeit.default_timer()
        self.time = stop - start

    def show_objective_fun_value_plots(self):
        """Display plot of all objective_fun_valuees"""
        font = {'family' : 'monospace',
                'size'   : '10'}

        plt.rc('font', **font)  # pass in the font dict as kwargs
        plt.figure(figsize=(12, 9))               
        
        plot1 = plt.subplot(311, ylabel='Value', title='Objective function value')             
        plot1.plot(self.all_objective_fun_value_best)
        
        plot2 = plt.subplot(312, sharex=plot1, ylabel='Value', title='Best candidate')            
        plot2.plot(self.all_objective_fun_value_best_candidate)

        plot3 = plt.subplot(313, sharex=plot2, xlabel='Iteration', ylabel='Value', title='Tabu candidate')
        plot3.plot(self.all_objective_fun_value_tabu_candidate)
        
        plt.show()

    def save_objective_fun_value_plots(self):
        """Saves plot of all objective function values to .png"""
        plt.figure()
        plt.xlabel('Iteration')
        plt.ylabel('Value')

        plt.plot(self.all_objective_fun_value_best)
        plt.title('Objective function value')
        plt.savefig("Fig/"+str(self.fig_number)+"_"+str(1)+".png")
        plt.clf()

        plt.plot(self.all_objective_fun_value_best_candidate,)
        plt.title('Best candidate objective function value')
        plt.savefig("Fig/"+str(self.fig_number)+"_"+str(2)+".png")
        plt.clf()
        
        plt.plot(self.all_objective_fun_value_tabu_candidate)
        plt.title('Tabu candidate objective function value')
        plt.savefig("Fig/"+str(self.fig_number)+"_"+str(3)+".png")

        plt.close()

        if self.early_break:
            record = [self.fig_number, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.time, \
            self.true_iter+1, self.seed, self.objective_fun_value, self.type_of_neighborhood, \
            self.tabu_list_length, self.OF.tmin, self.OF.data.number_of_tools]
        else:
            record = [self.fig_number, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.time, \
            self.number_of_iterations+1, self.seed, self.objective_fun_value, self.type_of_neighborhood, \
            self.tabu_list_length, self.OF.tmin, self.OF.data.number_of_tools]

        with open('records.csv', 'a', newline='') as csvfile:
            write_record = csv.writer(csvfile, delimiter=',')
            write_record.writerow(record)
