# import main
from tkinter import *

window = Tk()
window.geometry("450x300")


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

odleglosci = Text(window, height=5, width=20)
odleglosci.place(x=5, y=52)
label_odleglosci = Label(window, text='Podaj dane:').place(x=5, y=30)

label_sciezka = Label(window, text='Podaj ścieżkę do pliku:').place(x=5, y=140)
sciezka = Entry(window, width=30, state=DISABLED)
sciezka.place(x=5, y=160)

liczba_iteracji_box = Entry(window)
liczba_iteracji_box.place(x=320, y=5)
wielkosc_populacji_box = Entry(window)
wielkosc_populacji_box.place(x=320, y=45)
liczba_elitarnych_box = Entry(window)
liczba_elitarnych_box.place(x=320, y=85)
liczba_najlepszych_box = Entry(window)
liczba_najlepszych_box.place(x=320, y=125)
rozmiar_sasiedztwa_elit_box = Entry(window)
rozmiar_sasiedztwa_elit_box.place(x=320, y=165)
max_dlugosc_zycia_box = Entry(window)
max_dlugosc_zycia_box.place(x=320, y=205)

label_liczba_iteracji = Label(window, text='Liczba iteracji:', justify=RIGHT).place(x=200, y=5)
label_wielkosc_populacji = Label(window, text='Wielkość populacji:', justify=RIGHT).place(x=200, y=45)
label_liczba_elitarnych = Label(window, text='Liczba rozwiązań\nelitarnych:', justify=RIGHT).place(x=200, y=75)
label_liczba_najlepszych = Label(window, text='Liczba rozwiązań\nnajlepszych:', justify=RIGHT).place(x=200, y=115)
label_rozmiar_sasiedztwa_elit = Label(window, text='Rozmiar sąsiedztwa\nelitarnego:', justify=RIGHT).place(x=200, y=155)
label_max_dlugosc_zycia = Label(window, text='Maksymalna długość\nżycia rozwiązania:', justify=RIGHT).place(x=200,
                                                                                                            y=195)


def run_algorithm():
    if liczba_iteracji_box.get() != '' and wielkosc_populacji_box.get() != '' and liczba_elitarnych_box.get() != '' \
            and liczba_najlepszych_box.get() != '' and rozmiar_sasiedztwa_elit_box.get() != '' and \
            max_dlugosc_zycia_box.get() != '':
        liczba_iteracji = int(liczba_iteracji_box.get())
        wielkosc_populacji = int(wielkosc_populacji_box.get())
        liczba_elitarnych = int(liczba_elitarnych_box.get())
        liczba_najlepszych = int(liczba_najlepszych_box.get())
        rozmiar_sasiedztwa_elit = int(rozmiar_sasiedztwa_elit_box.get())
        max_dlugosc_zycia = int(max_dlugosc_zycia_box.get())


uruchom = Button(window, text='Uruchom', command=run_algorithm)
uruchom.place(x=350, y=260)

window.mainloop()
