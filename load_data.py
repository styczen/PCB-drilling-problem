import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np


class Pcb():

    def __init__(self,file_name):
        self.D = np.zeros((2,2))
        self.file = open(file_name,"a+")
        self.x = []  # wsp x pkt
        self.y = []  # wsp y pkt

    def __del__(self):
        self.file.close()

    def read_data(self):
        with open('pcb.txt','r') as csvfile:  # pcb.txt to plik ze wspolrzednymi
            points = csv.reader(csvfile, delimiter=' ')
            for point in points:
                self.x.append(int(point[0]) / 100)  # dodajemy do listy wczytywane współrzędne
                self.y.append(int(point[1]) / 100)  # dzielimy przez 100 aby wspolrzzedne byly w mm

    def distance_matrix(self):
        self.read_data()
        D = np.zeros((len(self.x),len(self.x)))
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                D[i][j] = math.sqrt((self.x[j] - self.x[i]) ** 2 + (self.y[j] - self.y[i]) ** 2)
        self.D = D
        return D

    def show(self):
        plt.plot(self.x, self.y, '.')
        plt.xlabel(u'Współrzedne X')
        plt.ylabel(u'Współrzedne Y')
        plt.title('Przykładowa płytka PCB')
        plt.show()


dd=Pcb("pcb.txt")
matrix = dd.distance_matrix()
print(matrix[0][2])