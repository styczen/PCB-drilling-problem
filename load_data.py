import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy
import numpy as np


class Pcb():

    def __init__(self,file_name, point_number=20, number_of_tools=2):
        self.D = np.zeros((2,2))
        self.T = np.zeros((2,2))
        self.file_name = file_name
        self.x = [0]
        self.y = [0]
        self.tools_number = [0]
        self.number_of_tools = number_of_tools
        self.point_number = point_number
        self.read_data(point_number, number_of_tools)

    def read_data(self, point_number, number_of_tools):
        '''Tworzenie wektora rodzaju narzędzia oraz wczytanie danych z pliku'''
        if number_of_tools > 6 or number_of_tools < 1 or point_number > 188:
            print('Podano złą wartośś liczby pkt lub narzędzi')
        point_per_tool = int(point_number/number_of_tools)
        for i in range(1, number_of_tools+1):
            for a in range(i, i+point_per_tool):
                self.tools_number.append(i)
            if i == number_of_tools:
                for b in range(0,point_number-len(self.tools_number)+1):
                    self.tools_number.append(i)

        with open(self.file_name,'r') as csvfile:
            points = csv.reader(csvfile, delimiter=' ')
            for i, point in enumerate(points):
                if i == point_number:
                    break
                self.x.append(int(point[0]) / 100)  # dodajemy do listy wczytywane współrzędne
                self.y.append(int(point[1]) / 100)  # dzielimy przez 100 aby wspolrzzedne byly w mm

    def distance_matrix(self):
        '''Liczenie macierzy odległości między pkt'''
        D = np.zeros((len(self.x),len(self.x)))
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                D[i][j] = math.sqrt((self.x[j] - self.x[i]) ** 2 + (self.y[j] - self.y[i]) ** 2)
        self.D = D
        return D

    def times_matrix(self):
        '''Liczenie czasów przezbrojenia między pkt'''
        t=np.array([[4,9,4,5,4,5,5],[6,5,2,4,1,5,9],[2,5,5,1,6,7,3],[9,2,9,5,4,1,7],[1,9,7,7,2,2,3],
                    [6,4,9,6,3,6,3],[8,2,9,9,3,7,2]])
        t=t*20
        #t = np.random.randint(low=1, high=10, size=(self.tools_number[-1], self.tools_number[-1]))
        T = np.zeros((len(self.D),len(self.D)))
        for i in range(len(T)):
            for j in range(len(T)):
                if i != j:
                    if self.tools_number[i] != self.tools_number[j]:
                        T[i][j] = t[self.tools_number[i]-1][self.tools_number[j]-1]

        T[0] = np.zeros(T.shape[0])     #zerowanie pierwszej kolumny i wiersza
        T[:,0] = np.zeros(T.shape[1])   #aby uwzględnić, że pkt 0,0 nie ma typu narzędzia
        self.T = T
        return T

    def show(self):
        plt.scatter(self.x, self.y, s=5, c=self.tools_number)
        plt.xlabel(u'Współrzedne X')
        plt.ylabel(u'Współrzedne Y')
        plt.title('Widok PCB')
        plt.show()


if __name__ == "__main__":
    pkta=39
    pktb=130
    dd=Pcb("pcb.txt",180,6)
    dd.distance_matrix()
    T=dd.times_matrix()
    print("Wielkość tablicy: {}".format(dd.distance_matrix().shape))
    print("odległość: {}".format(dd.D[pkta][pktb]))
    print("Czas przezbrojenia: {}".format(dd.T[pkta][pktb]))
    print("PKT A to narzędzie {} a pkt B to {}".format(dd.tools_number[pkta],dd.tools_number[pktb]))
    print(T)
    dd.show()