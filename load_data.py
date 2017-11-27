import math                         # pozwala na operacje matematyczne typu sqrt
import matplotlib.pyplot as plt     # do wykresów(składnia jak plot w matlabie)
import csv                          # do wczytywania lini z pliku jako rekordy

x = []  #wsp x pkt
y = []  #wsp y pkt

with open('pcb.txt','r') as csvfile:    # pcb.txt to plik ze wspolrzednymi
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




