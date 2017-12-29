import tabu_search
import obj_function
import load_data
import numpy as np
import timeit

if __name__ == "__main__":
    # BEGIN - Parameters for algorithm 
    file_name = 'pcb.txt'
    point_number = 188
    number_of_tools = 6
    t_min = 3
    number_of_iterations = 300
    tabu_list_length = 20
    type_of_neighborhood = 1
    stats_every_iteration = 0
    seed = 0
    # END - Parameters for algorithm  

    OF = obj_function.ObjectiveFun(file_name, t_min, point_number, number_of_tools)

    init_solution = np.arange(1, point_number + 1)
    # np.random.shuffle(init_solution)
    init_objective_fun_value = OF.obj_function(init_solution)

    # OF.data.show()

    for i in range(1, 6):
        seed = 3**i
        TS = tabu_search.TabuSearch(file_name, init_solution, init_objective_fun_value, stats_every_iteration,
                        number_of_iterations, tabu_list_length, type_of_neighborhood,
                        t_min, point_number, number_of_tools, seed)

        start = timeit.default_timer()
        TS.run()
        stop = timeit.default_timer()

        print("*************************************************************************")
        # print("Initial solution: \n" + str(init_solution))
        print("Initial objective function value: " + "{0:.2f}".format(init_objective_fun_value))
        print("-------------------------------------------------------------------------")
        # print("Best solution: \n" + str(TS.solution) + "\n")
        # print("Best real solution: \n" + str(OF.real_permutation(TS.solution)) + "\n")
        print("Best objective function value: " + "{0:.2f}".format(TS.objective_fun_value))
        print("Time of execution: " + "{0:.2f}".format(stop - start) + " seconds")
        print("*************************************************************************\n")

        # TS.show_objective_fun_value_plot()
        TS.save_objective_fun_value_plot()


