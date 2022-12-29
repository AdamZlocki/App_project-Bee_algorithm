from tkinter import filedialog

import numpy as np

from main import *
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = Tk()
window.title("Algorytm pszczeli")
window.geometry("850x300")


def insert_data_manually():
    if wczytywanie.get() == 0:
        odleglosci['state'] = NORMAL
        sciezka['state'] = DISABLED


def insert_data_file():
    if wczytywanie.get() == 1:
        odleglosci['state'] = DISABLED
        sciezka['state'] = NORMAL
        file = filedialog.askopenfilename(initialdir="/", title="Open Text file", filetypes=(("Text Files", "*.txt"),))
        if sciezka.get() != '':
            sciezka.delete(0, END)
        sciezka.insert(END, file)


wczytywanie = IntVar()
wczytywanie.set(0)
recznie = Radiobutton(window, text='Ręcznie', variable=wczytywanie, value=0, command=insert_data_manually)
recznie.place(x=5, y=5)
plik = Radiobutton(window, text='Z pliku', variable=wczytywanie, value=1, command=insert_data_file)
plik.place(x=70, y=5)

odleglosci = Text(window, height=10, width=40)
odleglosci.place(x=5, y=69)
label_odleglosci = Label(window, text="""Podaj dane (zapotrzebowanie\noddziel ' # ', a odległości ','):""",
                         justify=LEFT).place(x=5, y=30)

label_sciezka = Label(window, text='Podaj ścieżkę do pliku .txt:').place(x=220, y=5)
sciezka = Entry(window, width=40, state=DISABLED)
sciezka.place(x=220, y=27)

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

label_zle_dane_plik = Label(window, text=f"Macierz z pliku nie jest kwadratowa!", justify=RIGHT)
label_zle_dane_plik.place(x=220, y=47)
label_zle_dane_plik.place_forget()

label_zle_dane = Label(window, text=f"Podana macierz\nnie jest kwadratowa!", justify=LEFT)
label_zle_dane.place(x=330, y=67)
label_zle_dane.place_forget()

label_brak_danych = Label(window, text=f"Podaj dane!", justify=LEFT)
label_brak_danych.place(x=330, y=67)
label_brak_danych.place_forget()


def read_parameters():
    if liczba_iteracji_box.get() == '':  # wczytanie paramterów
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

    return liczba_iteracji, wielkosc_populacji, liczba_elitarnych, liczba_najlepszych, rozmiar_sasiedztwa_elit, max_dlugosc_zycia


def openNewWindow():
    wykres['state'] = DISABLED
    newWindow = Tk()
    newWindow.title("Wykres zmian najlepszego rozwiązania")
    newWindow.geometry("500x500")

    fig = Figure(figsize=(5, 5), dpi=100)

    x = [item for item in range(1, 1 + len(list_of_bests.get()))]
    plot1 = fig.add_subplot(111)

    plot1.step(x, list_of_bests.get(), where='post')
    plot1.grid()
    plot1.set_xticks(np.arange(min(x), max(x)+1, 1))
    plot1.set_yticks(np.linspace(min(list_of_bests.get()), max(list_of_bests.get()), 10))
    plot1.set_xlabel("Liczba iteracji")
    plot1.set_ylabel("Koszt najlepszego znalezionego w danej iteracji rozwiązania")

    canvas = FigureCanvasTkAgg(fig, master=newWindow)
    canvas.draw()

    canvas.get_tk_widget().pack()
    while True:
        try:
            newWindow.update()
            newWindow.update_idletasks()
        except TclError:
            wykres['state'] = NORMAL
            break


def run_algorithm():
    # odczyt paramterów
    liczba_iteracji, wielkosc_populacji, liczba_elitarnych, liczba_najlepszych, rozmiar_sasiedztwa_elit, \
        max_dlugosc_zycia = read_parameters()

    Restaurants = GraphMatrix()  # utworzenie grafu
    truck = Truck()
    v = 40  # prędkość ciężarówki
    matrix = []
    distance_matrix = []
    names = []
    requests = []
    if wczytywanie.get() == 0:  # jeśli wczytujemy z ręcznie wpisanych danych
        if odleglosci.get("1.0", END) == '\n':
            label_brak_danych.place(x=330, y=67)
        else:
            label_brak_danych.place_forget()
            data = odleglosci.get("1.0", 'end-1c')
            names, requests, matrix = get_data(data)
            if is_matrix_square(matrix):
                label_zle_dane.place_forget()
                label_zle_dane_plik.place_forget()
                label_brak_danych.place_forget()
                distance_matrix = convert_matrix_elements_to_int(matrix)
            else:
                label_zle_dane.place(x=330, y=67)
                return 0

    elif wczytywanie.get() == 1:  # jeśli wczytujemy z pliku
        file = sciezka.get()
        names, requests, matrix = save_data_from_txt_to_matrix(file)
        if is_matrix_square(matrix):
            label_zle_dane_plik.place_forget()
            label_zle_dane.place_forget()
            label_brak_danych.place_forget()
            distance_matrix = convert_matrix_elements_to_int(matrix)
        else:
            label_zle_dane_plik.place(x=220, y=70)
            return 0
    else:
        return 0
    if distance_matrix:
        for i in range(len(matrix)):  # uzupełnienie listy wierzchołków
            if i == 0:
                Restaurants.insertVertex(Vertex(is_base=True))
            else:
                Restaurants.insertVertex(Vertex(Id=i, name=names[i], request=int(requests[i])))

        for i in range(Restaurants.order()):  # obliczenie czasu i dodanie wszystkich krawędzi
            for j in range(Restaurants.order()):
                distance = distance_matrix[i][j]
                time = round(distance / v, 2)
                Restaurants.insertEdge(vertex1_idx=i, vertex2_idx=j, edge=Edge(i, j, time=time, distance=distance))
                Restaurants.insertEdge(vertex1_idx=j, vertex2_idx=i, edge=Edge(j, i, time=time, distance=distance))

        solution, bests = bee_algorythm(Restaurants, truck=truck, num_of_iterations=liczba_iteracji,
                                        size_of_iteration=wielkosc_populacji, num_of_elite=liczba_elitarnych,
                                        num_of_bests=liczba_najlepszych,
                                        size_of_neighbourhood=rozmiar_sasiedztwa_elit,
                                        max_LT=max_dlugosc_zycia)
        list_of_bests.set(bests)
        trasa.delete("1.0", END)
        trasa.insert(END, solution.route)
        wynik.delete("1.0", END)
        wynik.insert(END, solution.cost)
        wykres['state'] = NORMAL


trasa = Text(window, height=1, width=55)
trasa.place(x=20, y=260)
wynik = Text(window, height=1, width=10)
wynik.place(x=500, y=260)

uruchom = Button(window, text='Uruchom', command=run_algorithm)
uruchom.place(x=750, y=260)
wykres = Button(window, text='Wykres', command=openNewWindow)
wykres.place(x=680, y=260)
wykres['state'] = DISABLED

label_trasa = Label(window, text='Najlepsza znaleziona przez algorytm trasa:').place(x=20, y=235)
label_wynik = Label(window, text='Najmniejszy znaleziony koszt:').place(x=490, y=235)

list_of_bests = Variable()

window.mainloop()
