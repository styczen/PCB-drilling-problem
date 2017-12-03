import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np


def obj_function(permutation, distance_array, times_array, tmin):
    u"""Zwraca całkowity czas potrzebny na pokonanie trasy pomiędzy otworami na płytce
    wg danego wektora rozwiązania, w tym czas potzrzebny na przezbrojenie
    oraz czas oczekiwania na ostygnięcie płytki
    """
    return distance_function(permutation, distance_array, times_array) + loss_function(permutation, distance_array, times_array, tmin)

def distance_function(permutation, distance_array, times_array):
    u"""Zwraca  czas potrzebny na pokonanie trasy pomiędzy otworami na płytce
    wg danego wektora rozwiązania oraz czas potzrzebny na przezbrojenie wg
    macierzy zmiany wierteł oraz czasu powrotu do punktu bazowego
    """
    sum=0
    for i in range((permutation.shape[0] - 1)):
        if times_array[permutation[i]][permutation[i + 1]] == 0:
            sum += distance_array[permutation[i]][permutation[i+1]]
        else:
            sum += distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i+1]] + times_array[permutation[i]][permutation[i+1]]
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
            if (distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i + 1]] + times_array[permutation[i]][permutation[i + 1]]) < tmin:
                sum += tmin - (distance_array[permutation[i]][permutation[0]] + distance_array[permutation[0]][permutation[i + 1]] + times_array[permutation[i]][permutation[i + 1]])
    return sum

def real_permutation(permutation, times_array):
    u"""Zwraca permutację na podstawie wektora rozwiązań, która
    uwzględnia ewentualny powrót do punktu bazowego w celu przezbrojenia
    """
    real_permutation = permutation
    i = 0
    while True:
        if i == real_permutation.shape[0] - 1:
            break
        if times_array[real_permutation[i]][real_permutation[i + 1]] > 0:
            if (real_permutation[i] != 0) and (real_permutation[i + 1] != 0):
                real_permutation = np.insert(real_permutation, i + 1, [0])
        i += 1
    return real_permutation

#################################################################################################################
#### Tworzenie danych wejściowych:

#Macierz czasów przejścia między otworami v=1mm/s - początkowe współrzędne w pliku to współrzędne punktu bazoewgo
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

#Macierz czasów zmiany wierteł
T = np.random.randint(9, size=(len(D), len(D)))  # Tworzenie losowyej tablicy przezbrojeń
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        if i == 0 or j == 0: #Brak przezbrojenia względem punktu początkowego "0"
            T[i][j] = 0
        elif i == j:
            T[i][j] = 0
        elif i > j:
            T[i][j] = T[j][i] #Macierz symetryczna

#Przykładowy wektor rozwiązania
solution_vector = np.array([0])
for i in range(1, len(D)):
    solution_vector = np.append(solution_vector, i)
solution_vector = np.append(solution_vector, 0)

#Czas stygnięcia płytki
t = 3

#### Test:
D = np.array(D)  #Zamiana na typ numppy nie jest konieczna
np.set_printoptions(precision=2) #Wyświetlanie elementów tablic z dokładnością do 2 miejsc po przecinku
print("Time of transition between points array D = \n", D)
print("Time of change drills T =\n", T)
print("Minimal cooling time t =\n", t)
print("Solution vector =\n", solution_vector)
print("Value of objective function is:\n ", obj_function(solution_vector, D, T, t))
print("Real permutation is:\n", real_permutation(solution_vector, T))
