import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np

x = []  #wsp x pkt
y = []  #wsp y pkt

with open('pcb_test.txt','r') as csvfile:    # pcb.txt to plik ze wspolrzednymi
    plots = csv.reader(csvfile, delimiter=' ')
    for row in plots:
        x.append(int(row[0])/100)   # dodajemy do listy wczytywane współrzędne
        y.append(int(row[1])/100)   # dzielimy przez 100 aby wspolrzzedne byly w mm


# ustawienia wykresu płytki
plt.plot(x,y,'.')
plt.xlabel(u'Współrzedne X')
plt.ylabel(u'Współrzedne Y')
plt.title('Przykładowa płytka PCB')


D = [[0 for i in range(len(x))] for j in range(len(x))]   # tworzy tablicę na odległości wypełnianą zerami

for i in range(len(x)):
    for j in range(len(x)):
        D[i][j] = math.sqrt((x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2)    # liczy odległości między pkt w
                                                                        # układzie kartezjańskim

plt.show()  # wyświetla wygląd płytki


T = np.random.randint(9, size=(len(D), len(D)))  # Tworzenie losowyej tablicy przezbrojeń
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        if i == 0 or j == 0: #Brak przezbrojenia względem punktu początkowego "0"
            T[i][j] = 0
        elif i == j:
            T[i][j] = 0
        elif i > j:
            T[i][j] = T[j][i] #Macierz symetryczna

solution_vector = np.array([0]) #Tworzenie przykładowego wektora roazwiązania
for i in range(1, len(D)):
    solution_vector = np.append(solution_vector, i)
solution_vector = np.append(solution_vector, 0)



def obj_function(permutation, distance_array, times_array, tmin):
    sum1 = 0
    sum2 = 0
    real_permutation = permutation
    for i in range((permutation.shape[0] - 1)):
        sum1 += distance_array[permutation[i]][permutation[i+1]]
    for i in range((permutation.shape[0] - 1)):
        if times_array[permutation[i]][permutation[i+1]] == 0:
            if distance_array[permutation[i]][permutation[i+1]] < tmin:
                sum2 += tmin - distance_array[permutation[i]][permutation[i+1]]
        else:
            if (distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i+1]] + times_array[permutation[i]][permutation[i+1]]) >= tmin:
                sum2 += distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i+1]] + times_array[permutation[i]][permutation[i+1]] - distance_array[permutation[i]][permutation[i+1]]
            else:
                sum2 += tmin - (distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i+1]] + times_array[permutation[i]][permutation[i+1]]) - distance_array[permutation[i]][permutation[i+1]]
    i = 0
    while True:
        if i == real_permutation.shape[0] - 1:
            break
        if times_array[real_permutation[i]][real_permutation[i + 1]] > 0:
            if (real_permutation[i] != 0) and (real_permutation[i + 1] != 0):
                real_permutation = np.insert(real_permutation, i + 1, [0])
        i += 1
    sum = sum1 + sum2
    return (sum, real_permutation)


t = 3
D = np.array(D)
np.set_printoptions(precision=2)
print("D = \n", D)
print("T =\n", T)
print("solution_vector =\n", solution_vector)
val = obj_function(solution_vector, D, T, t)
print("value of objective function is:\n ", val[0])
print("real permutation is:\n", val[1])
