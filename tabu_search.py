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
    def __init__(self, file_name, init_solution, number_of_iterations, tabu_list_length, 
                 type_of_neighborhood, t_min, point_number, number_of_tools, seed):
        self.OF = obj_function.ObjectiveFun(file_name, t_min, point_number, number_of_tools)
        self.number_of_iterations = number_of_iterations
        self.tabu_list = np.array([], dtype=int)
        self.tabu_list_length = tabu_list_length
        self.objective_fun_value = self.OF.obj_function(init_solution)
        self.solution = init_solution
        self.solution_length = len(self.solution)
        self.type_of_neighborhood = type_of_neighborhood
        self.all_objective_fun_value_best = np.array([])
        self.all_objective_fun_value_tabu_candidate = np.array([])
        self.all_objective_fun_value_best_candidate = np.array([])
        self.time = 0
        self.seed = seed
        random.seed(seed)
        self.early_break = False
        # self.aspiration_criteria = False

    def get_tabu_candidate(self):
        """Permutes new neighborhood"""
        permutation = np.copy(self.solution)
        for _ in range(self.type_of_neighborhood):
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
        if self.tabu_list.shape[0] >= self.tabu_list_length:
            self.tabu_list = self.tabu_list.flatten()
            delete_vector_indices = [i for i in range(self.solution_length)]
            self.tabu_list = np.delete(self.tabu_list, delete_vector_indices)
        self.tabu_list = np.append(self.tabu_list, candidate)

    def run(self):
        """Main method which searches for optimal solution; ends when objective function value does not change for 10000 iterations"""
        local_min_indicator = 0
        repeat_obj_value = 0

        prev_value = self.objective_fun_value

        prev_solution = np.copy(self.solution)
        prev_objective_fun_value = self.objective_fun_value

        prev_prev_objective_fun_value = 0

        prev_prev_prev_objective_fun_value = 0

        start = timeit.default_timer()

        for i in range(self.number_of_iterations):
            self.all_objective_fun_value_best = np.append(self.all_objective_fun_value_best, self.objective_fun_value)
            best_candidate = self.get_neighbor()
            tabu_candidate = self.get_tabu_candidate()

            temporary_obj_best_candidate = self.OF.obj_function(best_candidate)
            self.all_objective_fun_value_best_candidate = np.append(self.all_objective_fun_value_best_candidate, temporary_obj_best_candidate)
            if temporary_obj_best_candidate < self.objective_fun_value:
                prev_prev_prev_objective_fun_value = prev_prev_objective_fun_value
                prev_prev_objective_fun_value = prev_objective_fun_value
                prev_objective_fun_value = self.objective_fun_value
                prev_solution = np.copy(self.solution)
                self.solution = np.copy(best_candidate)
                self.objective_fun_value = temporary_obj_best_candidate

            temporary_obj_tabu_candidate = self.OF.obj_function(tabu_candidate)
            self.all_objective_fun_value_tabu_candidate = np.append(self.all_objective_fun_value_tabu_candidate, temporary_obj_tabu_candidate)
            if temporary_obj_tabu_candidate < self.objective_fun_value:
                prev_prev_prev_objective_fun_value = prev_prev_objective_fun_value
                prev_prev_objective_fun_value = prev_objective_fun_value
                prev_objective_fun_value = self.objective_fun_value
                prev_solution = np.copy(self.solution)
                best_candidate = np.copy(tabu_candidate)
                self.solution = np.copy(tabu_candidate)
                self.objective_fun_value = temporary_obj_tabu_candidate

            self.update_memory(best_candidate)

            if self.objective_fun_value == prev_value:
                local_min_indicator = local_min_indicator + 1
            else:
                local_min_indicator = 0   

            if local_min_indicator >= 10000:
                local_min_indicator = 0
                self.solution = np.copy(prev_solution)
                self.objective_fun_value = prev_objective_fun_value

                print("Back to last valid solution completed")
                print("---"+str(i)+" "+str(int(self.objective_fun_value))+" "+str(int(prev_objective_fun_value)))

            if self.objective_fun_value == prev_prev_objective_fun_value and prev_objective_fun_value == prev_prev_prev_objective_fun_value:
                repeat_obj_value = repeat_obj_value + 1
            else:
                repeat_obj_value = 0

            if repeat_obj_value == 3:
                self.number_of_iterations = i
                break

            prev_value = self.objective_fun_value
            if i and not i % 1000:
                print("Iter: "+str(i)+" Value: "+str(int(self.objective_fun_value))+" Ind: "+str(local_min_indicator))

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
        plt.figure(figsize=(12, 9))
        plt.xlabel('Iteration')
        plt.ylabel('Value')

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        plt.plot(self.all_objective_fun_value_best)
        plt.title('Objective function value')
        plt.savefig("Fig/"+str(date)+"_"+str(int(self.time))+"_"\
                          +str(self.number_of_iterations)+"_"+str(self.seed)+"_"+str(int(self.objective_fun_value))+"_"\
                          +str(self.type_of_neighborhood)+"_"+str(self.tabu_list_length)+"_"\
                          +str(self.OF.tmin)+"_"+str(self.OF.data.number_of_tools)+".png")
        plt.clf()

        plt.plot(self.all_objective_fun_value_best_candidate,)
        plt.title('Best candidate objective function value')
        plt.savefig("Fig/"+str(date)+"_"+str(int(self.time))+"_"\
                          +str(self.number_of_iterations)+"_"+str(self.seed)+"_"+str(int(self.objective_fun_value))+"_"\
                          +str(self.type_of_neighborhood)+"_"+str(self.tabu_list_length)+"_"\
                          +str(self.OF.tmin)+"_"+str(self.OF.data.number_of_tools)+"_"+"best.png")
        plt.clf()
        
        plt.plot(self.all_objective_fun_value_tabu_candidate)
        plt.title('Tabu candidate objective function value')
        plt.savefig("Fig/"+str(date)+"_"+str(int(self.time))+"_"\
                          +str(self.number_of_iterations)+"_"+str(self.seed)+"_"+str(int(self.objective_fun_value))+"_"\
                          +str(self.type_of_neighborhood)+"_"+str(self.tabu_list_length)+"_"\
                          +str(self.OF.tmin)+"_"+str(self.OF.data.number_of_tools)+"_"+"tabu.png")

        plt.close()

        record = [date, int(self.time), \
        self.number_of_iterations, self.seed, self.objective_fun_value, self.type_of_neighborhood, \
        self.tabu_list_length, self.OF.tmin, self.OF.data.number_of_tools]

        with open('records.csv', 'a') as csv_file:
            write_record = csv.writer(csv_file, delimiter=",")
            write_record.writerow(record)