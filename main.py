import tabu_search
import obj_function
import load_data
import numpy as np

# file_name = 'PCB_test.txt'
# point_number = 100
# number_of_tools = 1

file_name = 'pcb.txt'
point_number = 188
number_of_tools = 1

t_min = 3
number_of_iterations = 10000
tabu_list_length = 10
type_of_neighborhood = 2
stats_every_iteration = 0

OF = obj_function.ObjectiveFun(file_name, t_min, point_number, number_of_tools)

init_solution = np.arange(1, point_number + 1)
# # init_solution = np.flip(init_solution, 0)
# # init_solution = np.array([8,  5, 10,  6,  9,  3,  4,  2,  1,  7])
# np.random.shuffle(init_solution)

init_objective_fun_value = OF.obj_function(init_solution)

# print("Initial solution: " + str(init_solution))
# print("Initial objective function value: " + str(init_objective_fun_value))
# print("Solution's length: " + str(len(init_solution)))

# OF.data.show()

TS = tabu_search.TabuSearch(file_name, init_solution, init_objective_fun_value, stats_every_iteration,
                 number_of_iterations, tabu_list_length, type_of_neighborhood,
                 t_min, point_number, number_of_tools)

TS.run()

print("---------------------------------------------------------------")
print("Best solution: \n" + str(TS.solution))
print("Best real solution: \n" + str(OF.real_permutation(TS.solution)))
print("Best objective function value: " + str(TS.objective_fun_value))
print("---------------------------------------------------------------")

TS.show_objective_fun_value_plot()

# for _ in range(10):
#     # best_candidate = TS.get_neighbor()
#     tabu_candidate = TS.get_tabu_candidate()
#     print("s: " + str(TS.solution))
#     # print("b: " + str(best_candidate) + str(OF.obj_function(best_candidate)))
#     # print("t: " + str(tabu_candidate) + str(OF.obj_function(tabu_candidate)))
#     # print("b1: " + str(best_candidate) + str(TS.OF.obj_function(best_candidate)))
#     # print("t1: " + str(tabu_candidate) + str(TS.OF.obj_function(tabu_candidate)) + '\n')