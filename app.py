from main import *
from tkinter import *

window = Tk()
window.geometry("850x300")


def insert_data_manually():
    if wczytywanie.get() == 0:
        odleglosci['state'] = NORMAL
        sciezka['state'] = DISABLED


def insert_data_file():
    if wczytywanie.get() == 1:
        odleglosci['state'] = DISABLED
        sciezka['state'] = NORMAL


wczytywanie = IntVar()
wczytywanie.set(0)
recznie = Radiobutton(window, text='Ręcznie', variable=wczytywanie, value=0, command=insert_data_manually)
recznie.place(x=5, y=5)
plik = Radiobutton(window, text='Z pliku', variable=wczytywanie, value=1, command=insert_data_file)
plik.place(x=70, y=5)

odleglosci = Text(window, height=10, width=20)
odleglosci.place(x=5, y=52)
label_odleglosci = Label(window, text='Podaj dane:').place(x=5, y=30)

label_sciezka = Label(window, text='Podaj ścieżkę do pliku:').place(x=220, y=30)
sciezka = Entry(window, width=30, state=DISABLED)
sciezka.place(x=220, y=52)

liczba_iteracji_box = Entry(window, width=10)
liczba_iteracji_box.place(x=720, y=5)
wielkosc_populacji_box = Entry(window, width=10)
wielkosc_populacji_box.place(x=720, y=45)
liczba_elitarnych_box = Entry(window, width=10)
liczba_elitarnych_box.place(x=720, y=85)
liczba_najlepszych_box = Entry(window, width=10)
liczba_najlepszych_box.place(x=720, y=125)
rozmiar_sasiedztwa_elit_box = Entry(window, width=10)
rozmiar_sasiedztwa_elit_box.place(x=720, y=165)
max_dlugosc_zycia_box = Entry(window, width=10)
max_dlugosc_zycia_box.place(x=720, y=205)

label_liczba_iteracji = Label(window, text='Liczba iteracji (domyślnie 10):', justify=RIGHT).place(x=555, y=5)
label_wielkosc_populacji = Label(window, text='Wielkość populacji (domyślnie 10):', justify=RIGHT).place(x=528, y=45)
label_liczba_elitarnych = Label(window, text='Liczba rozwiązań\nelitarnych (domyślnie 2):', justify=RIGHT).place(x=580,
                                                                                                                 y=75)
label_liczba_najlepszych = Label(window, text='Liczba rozwiązań\nnajlepszych (domyślnie 3):', justify=RIGHT).place(
    x=572, y=115)
label_rozmiar_sasiedztwa_elit = Label(window, text='Rozmiar sąsiedztwa\nelitarnego (domyślnie 10):',
                                      justify=RIGHT).place(x=575, y=155)
label_max_dlugosc_zycia = Label(window, text='Maksymalna długość\nżycia rozwiązania (domyślnie 3):',
                                justify=RIGHT).place(x=544,
                                                     y=195)


def run_algorithm():
    if liczba_iteracji_box.get() == '':
        liczba_iteracji = 10
    else:
        liczba_iteracji = int(liczba_iteracji_box.get())

    if wielkosc_populacji_box.get() == '':
        wielkosc_populacji = 10
    else:
        wielkosc_populacji = int(wielkosc_populacji_box.get())

    if liczba_elitarnych_box.get() == '':
        liczba_elitarnych = 2
    else:
        liczba_elitarnych = int(liczba_elitarnych_box.get())

    if liczba_najlepszych_box.get() == '':
        liczba_najlepszych = 3
    else:
        liczba_najlepszych = int(liczba_najlepszych_box.get())

    if rozmiar_sasiedztwa_elit_box.get() == '':
        rozmiar_sasiedztwa_elit = 10
    else:
        rozmiar_sasiedztwa_elit = int(rozmiar_sasiedztwa_elit_box.get())

    if max_dlugosc_zycia_box.get() == '':
        max_dlugosc_zycia = 3
    else:
        max_dlugosc_zycia = int(max_dlugosc_zycia_box.get())

    Restaurants = GraphMatrix()
    truck = Truck()
    v = 40  # prędkość ciężarówki
    Restaurants.insertVertex(Vertex(is_base=True))
    # ---------------------------------------------------------------------
    names = {1: "Szewska",
             2: "Floriańska",
             3: "Grodzka",
             4: "Pawia",
             5: "Jasnogórska",
             6: "Wadowicka",
             7: "Aleja Generała Tadeusza Bora-K",
             8: "Stawowa",
             9: "Pilotów",
             10: "Mieczysława Medwieckiego",
             11: "Podgórska",
             12: "Wielicka",
             13: "Opolska",
             14: "Tadeusza Śliwiaka",
             15: "Aleja Pokoju",
             16: "Stanisława Stojałowskiego",
             17: "Henryka Kamińskiego"}

    for i in names.keys():  # utworzenie grafu dla testów
        vertex = Vertex(Id=i, name=names[i], is_base=False)
        if vertex not in Restaurants.list:
            Restaurants.insertVertex(vertex)

    for i in range(Restaurants.order()):
        for j in range(Restaurants.order()):
            if i != j and not Restaurants.matrix[i][j]:
                distance = round(uniform(0.3, 5), 2)  # odległość między dwoma restauracjami - od 300 metrów do 5
                # kilometrów
                time = round(distance / v, 2)  # obliczony czas przejazdu w godzinach dla średniej prędkości 50 km/h
                Restaurants.insertEdge(vertex1_idx=i, vertex2_idx=j, edge=Edge(i, j, time=time, distance=distance))
                Restaurants.insertEdge(vertex1_idx=j, vertex2_idx=i, edge=Edge(j, i, time=time, distance=distance))
    # ---------------------------------------------------------------------
    solution = bee_algorythm(Restaurants, truck=truck, num_of_iterations=liczba_iteracji,
                             size_of_iteration=wielkosc_populacji, num_of_elite=liczba_elitarnych,
                             num_of_bests=liczba_najlepszych, size_of_neighbourhood=rozmiar_sasiedztwa_elit,
                             max_LT=max_dlugosc_zycia)
    trasa.delete("1.0", END)
    trasa.insert(END, solution.route)
    wynik.delete("1.0", END)
    wynik.insert(END, solution.cost)


trasa = Text(window, height=1, width=55)
trasa.place(x=20, y=260)
wynik = Text(window, height=1, width=10)
wynik.place(x=500, y=260)

uruchom = Button(window, text='Uruchom', command=run_algorithm)
uruchom.place(x=750, y=260)
label_trasa = Label(window, text='Najlepsza znaleziona przez algorytm trasa:').place(x=20, y=235)
label_wynik = Label(window, text='Najmniejszy znaleziony koszt:').place(x=490, y=235)


window.mainloop()
