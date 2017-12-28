import tabu_search
import obj_function
import load_data
import numpy as np

# file_name = 'PCB_test.txt'
# point_number = 100
# number_of_tools = 1

file_name = 'pcb.txt'
point_number = 25
number_of_tools = 3

t_min = 3
number_of_iterations = 10000
tabu_list_length = 5
type_of_neighborhood = 25
stats_every_iteration = False
OF = obj_function.ObjectiveFun(file_name, t_min, point_number, number_of_tools)

init_solution = np.arange(1, point_number + 1)
np.random.shuffle(init_solution)
init_objective_fun_value = OF.obj_function(init_solution)

print("Initial solution: " + str(init_solution))
print("Initial objective function value: " + str(init_objective_fun_value))
print("Solution's length: " + str(len(init_solution)))

# OF.data.show()

TS = tabu_search.TabuSearch(file_name, init_solution, init_objective_fun_value, stats_every_iteration,
                 number_of_iterations, tabu_list_length, type_of_neighborhood,
                 t_min, point_number, number_of_tools)

TS.run()

print("--------------------------------------")
print("Best solution: " + str(TS.solution))
print("Best real solution: " + str(OF.real_permutation(TS.solution)))
print("Best objective function value: " + str(TS.objective_fun_value))

TS.show_objective_fun_value_plot()

