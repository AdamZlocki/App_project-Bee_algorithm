import numpy as np
from main import *
from tkinter import TclError
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("Algorytm pszczeli")
window.geometry("850x500")


def insert_data_manually():
    if wczytywanie.get() == 0:
        odleglosci.configure(state="normal")
        sciezka.configure(state="disabled")


def insert_data_file():
    if wczytywanie.get() == 1:
        odleglosci.configure(state="disabled")
        sciezka.configure(state="normal")
        file = ctk.filedialog.askopenfilename(initialdir="/", title="Open Text file",
                                              filetypes=(("Text Files", "*.txt"),))
        if sciezka.get() != '':
            sciezka.delete(0, "end")
        print(file)
        sciezka.insert("end", file)


wczytywanie = ctk.IntVar()
wczytywanie.set(0)
recznie = ctk.CTkRadioButton(window, text='Ręcznie', variable=wczytywanie, value=0, command=insert_data_manually)
recznie.place(x=5, y=5)
plik = ctk.CTkRadioButton(window, text='Z pliku', variable=wczytywanie, value=1, command=insert_data_file)
plik.place(x=90, y=5)

odleglosci = ctk.CTkTextbox(window, height=320, width=565)
odleglosci.place(x=5, y=69)
label_odleglosci = ctk.CTkLabel(window, text="""Podaj dane (zapotrzebowanie\noddziel ' # ', a odległości ','):""",
                                justify=ctk.LEFT).place(x=5, y=30)

label_sciezka = ctk.CTkLabel(window, text='Podaj ścieżkę do pliku .txt:').place(x=220, y=5)
sciezka = ctk.CTkEntry(window, width=350, state=ctk.DISABLED)
sciezka.place(x=220, y=27)

liczba_iteracji_box = ctk.CTkEntry(window, width=40, placeholder_text="10")
liczba_iteracji_box.place(x=780, y=27)
wielkosc_populacji_box = ctk.CTkEntry(window, width=40, placeholder_text="10")
wielkosc_populacji_box.place(x=780, y=67)
liczba_elitarnych_box = ctk.CTkEntry(window, width=40, placeholder_text="2")
liczba_elitarnych_box.place(x=780, y=107)
liczba_najlepszych_box = ctk.CTkEntry(window, width=40, placeholder_text="3")
liczba_najlepszych_box.place(x=780, y=147)
rozmiar_sasiedztwa_elit_box = ctk.CTkEntry(window, width=40, placeholder_text="10")
rozmiar_sasiedztwa_elit_box.place(x=780, y=187)
rozmiar_sasiedztwa_najlep_box = ctk.CTkEntry(window, width=40, placeholder_text="5")
rozmiar_sasiedztwa_najlep_box.place(x=780, y=227)
max_dlugosc_zycia_box = ctk.CTkEntry(window, width=40, placeholder_text="3")
max_dlugosc_zycia_box.place(x=780, y=267)

label_liczba_iteracji = ctk.CTkLabel(window, text='Liczba iteracji:', justify=ctk.RIGHT).place(x=687, y=27)
label_wielkosc_populacji = ctk.CTkLabel(window, text='Wielkość populacji:', justify=ctk.RIGHT).place(x=660, y=67)
label_liczba_elitarnych = ctk.CTkLabel(window, text='Liczba rozwiązań elitarnych:', justify=ctk.RIGHT).place(x=608,
                                                                                                             y=107)
label_liczba_najlepszych = ctk.CTkLabel(window, text='Liczba rozwiązań najlepszych:', justify=ctk.RIGHT).place(x=597,
                                                                                                               y=147)
label_rozmiar_sasiedztwa_elit = ctk.CTkLabel(window, text='Rozmiar sąsiedztwa\nrozwiązań elitarnych:',
                                             justify=ctk.RIGHT).place(x=649, y=187)
label_rozmiar_sasiedztwa_najlep = ctk.CTkLabel(window, text='Rozmiar sąsiedztwa\nrozwiązań najlepszych:',
                                               justify=ctk.RIGHT).place(x=639, y=227)
label_max_dlugosc_zycia = ctk.CTkLabel(window, text='Maksymalna długość\nżycia rozwiązania:', justify=ctk.RIGHT).place(
    x=648, y=267)


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

    if rozmiar_sasiedztwa_najlep_box.get() == '':
        rozmiar_sasiedztwa_najlep = 5
    else:
        rozmiar_sasiedztwa_najlep = int(rozmiar_sasiedztwa_najlep_box.get())

    if max_dlugosc_zycia_box.get() == '':
        max_dlugosc_zycia = 3
    else:
        max_dlugosc_zycia = int(max_dlugosc_zycia_box.get())

    return liczba_iteracji, wielkosc_populacji, liczba_elitarnych, liczba_najlepszych, rozmiar_sasiedztwa_elit, rozmiar_sasiedztwa_najlep, max_dlugosc_zycia


def openNewWindow():
    wykres.configure(state="disabled")
    newWindow = ctk.CTk()
    newWindow.title("Wykres zmian najlepszego rozwiązania")
    newWindow.geometry("800x500")

    fig = Figure(figsize=(12, 5), dpi=100)

    x = [item for item in range(1, 1 + len(list_of_bests.get()))]
    plot1 = fig.add_subplot(111)

    plot1.step(x, list_of_bests.get(), where='post')
    plot1.grid()
    plot1.set_xticks(np.arange(min(x), max(x) + 1, 2))
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
            wykres.configure(state="normal")
            break


def run_algorithm():
    # odczyt paramterów
    liczba_iteracji, wielkosc_populacji, liczba_elitarnych, liczba_najlepszych, rozmiar_sasiedztwa_elit, \
    rozmiar_sasiedztwa_najlep, max_dlugosc_zycia = read_parameters()

    Restaurants = GraphMatrix()  # utworzenie grafu
    truck = Truck()
    v = 40  # prędkość ciężarówki
    matrix = []
    distance_matrix = []
    names = []
    requests = []
    if wczytywanie.get() == 0:  # jeśli wczytujemy z ręcznie wpisanych danych
        if odleglosci.get("1.0", ctk.END) == '\n':
            ErrorWindow = ctk.CTk()
            ErrorWindow.title("Brak danych!")
            ErrorWindow.geometry("250x100")
            label_brak_danych = ctk.CTkLabel(ErrorWindow, text=f"Podaj dane!", justify=ctk.LEFT, font=("normal", 40),
                                             fg_color="transparent")
            label_brak_danych.pack()
            while True:
                try:
                    ErrorWindow.update()
                    ErrorWindow.update_idletasks()
                except TclError:
                    break
        else:
            data = odleglosci.get("1.0", 'end-1c')
            names, requests, matrix = get_data(data)
            if is_matrix_square(matrix):
                distance_matrix = convert_matrix_elements_to_int(matrix)
            else:
                ErrorWindow = ctk.CTk()
                ErrorWindow.title("Błędne dane!")
                ErrorWindow.geometry("450x120")
                label_zle_dane = ctk.CTkLabel(ErrorWindow, text=f"Podana macierz\nnie jest kwadratowa!",
                                              justify=ctk.LEFT,
                                              font=("normal", 40),
                                              fg_color="transparent")
                label_zle_dane.pack()
                while True:
                    try:
                        ErrorWindow.update()
                        ErrorWindow.update_idletasks()
                    except TclError:
                        break
                return

    elif wczytywanie.get() == 1:  # jeśli wczytujemy z pliku
        file = sciezka.get()
        names, requests, matrix = save_data_from_txt_to_matrix(file)
        if is_matrix_square(matrix):
            distance_matrix = convert_matrix_elements_to_int(matrix)
        else:
            ErrorWindow = ctk.CTk()
            ErrorWindow.title("Błędne dane!")
            ErrorWindow.geometry("450x120")
            label_zle_dane_plik = ctk.CTkLabel(window, text=f"Macierz z pliku\nnie jest kwadratowa!", justify=ctk.LEFT,
                                               font=("normal", 40),
                                               fg_color="transparent")
            label_zle_dane_plik.pack()
            while True:
                try:
                    ErrorWindow.update()
                    ErrorWindow.update_idletasks()
                except TclError:
                    break
            return
    else:
        return
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
                                        size_of_neighbourhood_elite=rozmiar_sasiedztwa_elit, max_LT=max_dlugosc_zycia)
        list_of_bests.set(bests)
        trasa.delete("1.0", ctk.END)
        trasa.insert(ctk.END, solution.route)
        wynik.delete("1.0", ctk.END)
        wynik.insert(ctk.END, solution.cost)
        wykres.configure(state="normal")


trasa = ctk.CTkTextbox(window, height=1, width=250)
trasa.place(x=20, y=450)
wynik = ctk.CTkTextbox(window, height=1, width=70)
wynik.place(x=300, y=450)

uruchom = ctk.CTkButton(window, height=40, fg_color="green", text='Uruchom', command=run_algorithm)
uruchom.place(x=680, y=440)
wykres = ctk.CTkButton(window, height=40, text='Wykres', command=openNewWindow)
wykres.place(x=680, y=370)
wykres.configure(state="disabled")

label_trasa = ctk.CTkLabel(window, text='Najlepsza znaleziona przez algorytm trasa:').place(x=20, y=420)
label_wynik = ctk.CTkLabel(window, text='Najmniejszy znaleziony koszt:').place(x=300, y=420)

list_of_bests = ctk.Variable()

window.mainloop()
