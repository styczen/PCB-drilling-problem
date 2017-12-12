import tabu_search
import obj_function
import numpy as np

OF = obj_function.ObjectiveFun('pcb.txt', 3)

permut = np.arange(0, 189)
permut[188] = 0
# print(permut)
# print(len(permut))
q = OF.obj_function(permut)
# print(q)

TS = tabu_search.TabuSearch('pcb.txt', permut, q, 100, 10, 10, 2)

TS.run()