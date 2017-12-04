import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np


class Pcb():

    def __init__(self,file_name):
        self.D = np.zeros((2,2))
        self.file_name = file_name
        self.x = []  # wsp x pkt
        self.y = []  # wsp y pkt
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

    def show(self):
        plt.plot(self.x, self.y, '.')
        plt.xlabel(u'Współrzedne X')
        plt.ylabel(u'Współrzedne Y')
        plt.title('Przykładowa płytka PCB')
        plt.show()


