import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np


class Pcb():

    def __init__(self,file_name):
        self.D = np.zeros((2,2))
        self.T = np.zeros((2,2))
        self.file_name = file_name
        self.x = []
        self.y = []
        self.tools_number = []

    def read_data(self):
        number_of_tools = 1
        with open(self.file_name,'r') as csvfile:  # pcb.txt to plik ze wspolrzednymi
            points = csv.reader(csvfile, delimiter=' ')
            for i, point in enumerate(points):
                if point != []:
                    self.x.append(int(point[0]) / 100)  # dodajemy do listy wczytywane współrzędne
                    self.y.append(int(point[1]) / 100)  # dzielimy przez 100 aby wspolrzzedne byly w mm
                    self.tools_number.append(number_of_tools)
                else:
                    number_of_tools += 1

    def distance_matrix(self):
        self.read_data()
        D = np.zeros((len(self.x),len(self.x)))
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                D[i][j] = math.sqrt((self.x[j] - self.x[i]) ** 2 + (self.y[j] - self.y[i]) ** 2)
        self.D = D
        return D

    def times_matrix(self):
        t=np.array([[4,9,4,5,4,5,5],[6,5,2,4,1,5,9],[2,5,5,1,6,7,3],[9,2,9,5,4,1,7],[1,9,7,7,2,2,3],[6,4,9,6,3,6,3],[8,2,9,9,3,7,2]])
        #t = np.random.randint(low=1, high=10, size=(self.tools_number[-1], self.tools_number[-1]))
        T = np.zeros((len(self.D),len(self.D)))
        for i in range(len(T)):
            for j in range(len(T)):
                if i != j:
                    if self.tools_number[i] != self.tools_number[j]:
                        T[i][j] = t[self.tools_number[i]-1][self.tools_number[j]-1]
        self.T = T
        return T

    def show(self):
        plt.plot(self.x, self.y, '.')
        plt.xlabel(u'Współrzedne X')
        plt.ylabel(u'Współrzedne Y')
        plt.title('Widok PCB')
        plt.show()


""" Testowanie
pkta=1
pktb=150
dd=Pcb("pcb.txt")
dd.distance_matrix()
dd.times_matrix()
print("odległość: {}".format(dd.D[pkta][pktb]))
print("Czas przezbrojenia: {}".format(dd.T[pkta][pktb]))
print("PKT A to narzędzie {} a pkt B to {}".format(dd.tools_number[pkta],dd.tools_number[pktb]))
"""