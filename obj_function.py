# import math                         # pozwala na operacje matematyczne typu sqrt
# import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
# import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np
import load_data


def distance_function(permutation, distance_array, times_array):
    u"""Zwraca  czas potrzebny na pokonanie trasy pomiędzy otworami na płytce
    wg danego wektora rozwiązania oraz czas potzrzebny na przezbrojenie wg
    macierzy zmiany wierteł oraz czasu powrotu do punktu bazowego
    """
    sum = 0
    for i in range((permutation.shape[0] - 1)):
        if times_array[permutation[i]][permutation[i + 1]] == 0:
            sum += distance_array[permutation[i]][permutation[i + 1]]
        else:
            sum += distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i + 1]] \
                   + times_array[permutation[i]][permutation[i + 1]]
    return sum


def loss_function(permutation, distance_array, times_array, tmin):
    u"""Funkcja kary - zwraca czas oczekiwania na ostygnięcie płytki
    na podstawie czasu stygnięcia, czasu przejścia pomiędzy otworami oraz ewentualnego przezbrojenia
    """
    sum = 0
    for i in range((permutation.shape[0] - 1)):
        if times_array[permutation[i]][permutation[i + 1]] == 0:
            if distance_array[permutation[i]][permutation[i + 1]] < tmin:
                sum += tmin - distance_array[permutation[i]][permutation[i + 1]]
        else:
            if (distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i + 1]] \
                + times_array[permutation[i]][permutation[i + 1]]) < tmin:
                sum += tmin - (distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][
                    permutation[i + 1]] + times_array[permutation[i]][permutation[i + 1]])
    return sum


class ObjectiveFun():
    u"""Udostępnia metody obliczania wartości funkcji celu oraz generowania
    rzeczywistego wektora rozwiązania z uwzględnieniem powrotów do punktu bazowego
    """
    def __init__(self, file_name, t_min, point_number, number_of_tools):
        self.data = load_data.Pcb(file_name, point_number, number_of_tools)
        self.data.distance_matrix()
        self.data.times_matrix()
        self.tmin = t_min

    def obj_function(self, permutation):
        u"""Zwraca całkowity czas potrzebny na pokonanie trasy pomiędzy otworami na płytce
        wg danego wektora rozwiązania, w tym czas potzrzebny na przezbrojenie
        oraz czas oczekiwania na ostygnięcie płytki
        """
        permutation = np.insert(permutation, 0, [0])
        permutation = np.insert(permutation, permutation.shape[0], [0])
        return distance_function(permutation, self.data.D, self.data.T) + loss_function(permutation, self.data.D, self.data.T, self.tmin)

    def real_permutation(self, permutation):
        u"""Zwraca permutację na podstawie wektora rozwiązań, która
        uwzględnia ewentualny powrót do punktu bazowego w celu przezbrojenia
        """
        real_permutation = permutation
        real_permutation = np.insert(real_permutation, 0, [0])
        real_permutation = np.insert(real_permutation, real_permutation.shape[0], [0])
        i = 0
        while True:
            if i == real_permutation.shape[0] - 1:
                break
            if self.data.T[real_permutation[i]][real_permutation[i + 1]] > 0:
                if (real_permutation[i] != 0) and (real_permutation[i + 1] != 0):
                    real_permutation = np.insert(real_permutation, i + 1, [0])
            i += 1
        return real_permutation

