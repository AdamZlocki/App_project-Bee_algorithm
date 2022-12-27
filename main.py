from random import randint, choice


class Vertex:  # wierzchołek - restauracja; reprezentuje id, nazwa (łatwość wprowadzania danych przez użytkownika) i
    # informuje o swoim zapotrzebowaniu
    def __init__(self, Id=None, name=' ', request=randint(100, 999), is_base=False):
        if not is_base:
            self.Id = Id
            self.name = name
            self.visited = 0
            self.request = request
        else:
            self.Id = 0
            self.name = "Base"
            self.visited = 1

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __repr__(self):
        if self.Id != 0:
            return f"{self.Id}, {self.request}"
        else:
            return f"{self.Id}"

    def __hash__(self):
        return hash(self.Id)


class Edge:  # połączenie między restauracjami; reprezentuje czas przejazdu i odległość
    def __init__(self, start, end, time: float = 0, distance: float = 0):
        self.start = start
        self.end = end
        self.time = time
        self.distance = distance

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        else:
            return False

    def __repr__(self):
        return f"({self.distance}, {self.time})"


class Truck:  # ciężarówka; zadana pojemność
    def __init__(self, capacity=3000):
        self.capacity = capacity


class Solution:  # postać rozwiązania; route to trasa w postaci listy id restauracji w kolejności odwiedzania,
    # cost to wyliczona wartość funkcji celu
    def __init__(self, route, edges, cost):
        self.route = route
        self.edges = edges
        self.cost = cost
        self.neighbourhood = []
        self.LT = 0

    def __eq__(self, other):
        if self.route == other.route:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.route}, {self.cost}"

    def __str__(self):
        return f"{self.route}, {self.cost}"

    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        else:
            return False


class GraphMatrix:
    def __init__(self):
        self.list = []
        self.dict = {}
        self.matrix = [[]]

    def insertVertex(self, vertex):
        self.list.append(vertex)
        self.dict[vertex] = self.order() - 1
        if self.order() != 1:
            for i in range(len(self.matrix)):
                self.matrix[i].append(0)
            self.matrix.append([0] * len(self.matrix[0]))
        else:
            self.matrix[0].append(0)

    def insertEdge(self, vertex1_idx, vertex2_idx, edge):
        if vertex1_idx is not None and vertex2_idx is not None:
            self.matrix[vertex1_idx][vertex2_idx] = edge

    def deleteVertex(self, vertex):
        vertex_idx = self.getVertexIdx(vertex)
        for i in range(self.order()):
            if i != vertex_idx:
                self.matrix[i].pop(vertex_idx)
        self.matrix.pop(vertex_idx)
        self.list.pop(vertex_idx)
        self.dict.pop(vertex)
        for i in range(vertex_idx, self.order()):
            actual = self.list[i]
            self.dict[actual] -= 1

    def deleteEdge(self, vertex1, vertex2):
        vertex1_idx = self.getVertexIdx(vertex1)
        vertex2_idx = self.getVertexIdx(vertex2)
        for i in range(len(self.matrix[vertex1_idx])):
            if self.matrix[vertex1_idx][vertex2_idx] != 0:
                self.matrix[vertex1_idx][vertex2_idx] = 0

    def getVertexIdx(self, vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx):
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx):
        result = []
        for i in range(len(self.matrix[vertex_idx])):
            if self.matrix[vertex_idx][i]:
                result.append(i)
        return result

    def order(self):
        return len(self.list)

    def size(self):
        result = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    result += 1
        return result

    def edges(self):
        result = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j]:
                    result.append(self.matrix[i][j])
        return result


def Target_funtion(route, edges, w=2.68, p=20):  # funkcja obliczająca funkcję celu; w = koszt paliwa za przejechanie
    # jednego kilometra, p = godzionwe wynagordzenie kierowcy, penalty = kara
    cost = 0
    penalty = 10 * (route.count(0) - 2)
    for edge in edges:
        cost += edge.distance * w + edge.time * p
    cost += penalty
    return round(cost, 2)


def all_visited(graph: GraphMatrix):
    result = True
    for vertex in graph.list:
        if vertex.visited == 0:
            result = False
            break
    return result


def find_solution(graph: GraphMatrix, truck: Truck):
    route = [0]
    edges = []
    actual = 0
    while not all_visited(graph):
        neighbours = graph.neighbours(actual)  # wyszukanie sąsiadów i usunięcie Bazy
        if 0 in neighbours:
            neighbours.remove(0)

        neighbours_to_delete = []  # wyszukanie już odwiedzonych sąsiadów lub sąsiadów ze zbyt wysokim zapotrzebowaniem
        for neigh in neighbours:
            if graph.getVertex(neigh).visited == 1 or graph.getVertex(neigh).request > truck.capacity:
                neighbours_to_delete.append(neigh)

        for neigh in neighbours_to_delete:  # usunięcie niedozwolonych sąsiadów
            neighbours.remove(neigh)

        if len(neighbours):  # jeśli zostali jeszcze jacyś sąsiedzi wylosowanie nastepnego wierzchołka
            neighbour = choice(neighbours)
            graph.getVertex(neighbour).visited = 1
            truck.capacity -= graph.getVertex(neighbour).request
        else:  # jeśli nie wybranie 0
            neighbour = 0
            truck.capacity = 3000

        edges.append(graph.matrix[actual][neighbour])
        route.append(neighbour)

        actual = neighbour

    cost = Target_funtion(route=route, edges=edges)

    solution = Solution(route=route, edges=edges, cost=cost)

    for vertex in graph.list[1:]:  # reset grafu i ciężarówki
        vertex.visited = 0
    truck.capacity = 3000

    return solution


def neighbourhood(graph: GraphMatrix, solution: Solution, size: int = 5):
    n = len(solution.route)
    neighbours = []
    while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
        a, b = 0, 0
        is_0_between = True
        while is_0_between:  # podpętla wykonuje się dopóki między wylosowanymi do podmiany punktami występuje zero
            is_0_between = False
            a, b = randint(1, n - 1), randint(1, n - 1)  # wylosowanie punktów do podmiany
            if a == b:  # jeśli wylosowane punkty są identyczne nie ma sensu kontynuować podpętli
                is_0_between = True
            else:
                if a > b:  # ustalenie kolejności punktów: a - mniejszy, b - większy
                    a, b = b, a
                for i in range(a, b + 1):  # sprawdzenie czy między wylosowanymi punktami lub któryś z nich jest zero
                    if solution.route[i] == 0:
                        is_0_between = True
                        break

        neighbour_route = solution.route.copy()  # podmiana wybranych wierzchołków
        neighbour_route[a], neighbour_route[b] = neighbour_route[b], neighbour_route[a]

        neighbour_edges = []  # utworzenie nowej listy krawędzi
        for i in range(1, len(neighbour_route)):
            neighbour_edges.append(graph.matrix[neighbour_route[i - 1]][neighbour_route[i]])

        neighbour_cost = Target_funtion(neighbour_route, neighbour_edges)  # obliczenie nowego kosztu

        neighbour = Solution(route=neighbour_route, edges=neighbour_edges, cost=neighbour_cost)
        if neighbour not in neighbours:  # wstawienie nowego sąsiada jeśli nie ma go w sąsiedztwie
            neighbours.append(neighbour)

    return neighbours


def bee_algorythm(graph: GraphMatrix, truck: Truck, num_of_iterations: int = 10, size_of_iteration: int = 10,
                  num_of_elite: int = 2, num_of_bests: int = 3, size_of_neighbourhood: int = 10, max_LT: int = 3):
    solutions = []
    counter_of_iterations = 0
    best = 0
    while counter_of_iterations < num_of_iterations:  # dopóki nie wykonano oczekiwanej liczby iteracji powtarzamy
        if solutions:  # w przypadku gdy coś znajduje się w liście rozwiązań - usunięcie rozwiązń, które przekroczyły
            # maksymalną długość życia
            for solution in solutions:
                if solution.LT > max_LT:
                    solutions.remove(solution)

        while len(solutions) < size_of_iteration:  # utworzenie zadanej ilości początkowych rozwiązań
            sol = find_solution(graph=graph, truck=truck)
            if sol not in solutions:
                solutions.append(sol)

        # if counter_of_iterations == 0:
        #     print('Populacja początkowa:')
        #     for i in range(size_of_iteration):
        #         print(solutions[i])

        solutions_sorted = []  # posortowanie rozwiązań i zapamiętanie najlepszgo
        while len(solutions_sorted) < size_of_iteration:
            solutions_sorted.append(solutions.pop(solutions.index(min(solutions))))
        solutions = solutions_sorted.copy()
        best = solutions[0]

        elite_solutions = []  # utworzenie listy rozwiązań elitarnych
        while len(elite_solutions) < num_of_elite:
            elite_solutions.append(solutions.pop(solutions.index(min(solutions))))

        best_solutions = []  # utworzenie listy rozwiązań najlepszych (gorsze od elitarych)
        while len(best_solutions) < num_of_bests:
            best_solutions.append(solutions.pop(solutions.index(min(solutions))))

        for solution in elite_solutions:  # utworzenie sąsiedztwa rozwiązań elitarnych i ewentualne zastąpienie ich ich
            # najlepszymi sąsiadami
            solution.neighbourhood = []
            solution.neighbourhood = neighbourhood(graph=graph, solution=solution, size=size_of_neighbourhood)
            best_neighbour = solution.neighbourhood[solution.neighbourhood.index(min(solution.neighbourhood))]
            if best_neighbour < solution:
                elite_solutions[elite_solutions.index(solution)] = best_neighbour

        for solution in best_solutions:  # utworzenie sąsiedztwa rozwiązań najlepszych i ewentualne zastąpienie ich ich
            # najlepszymi sąsiadami
            solution.neighbourhood = []
            solution.neighbourhood = neighbourhood(graph=graph, solution=solution, size=round(size_of_neighbourhood/2))
            best_neighbour = solution.neighbourhood[solution.neighbourhood.index(min(solution.neighbourhood))]
            if best_neighbour < solution:
                best_solutions[best_solutions.index(solution)] = best_neighbour

        solutions = elite_solutions + best_solutions

        solutions_sorted = []  # posortowanie rozwiązań i zapamiętanie najlepszgo
        while len(solutions_sorted) < num_of_bests + num_of_elite:
            solutions_sorted.append(solutions.pop(solutions.index(min(solutions))))
        solutions = solutions_sorted.copy()
        if solutions[0] < best:
            best = solutions[0]

        for solution in solutions:
            solution.LT += 1

        counter_of_iterations += 1

    return best


def save_data_from_txt_to_matrix(file_name):
    f = open(file_name, 'r')
    splitted = [line.strip().split(' # ', 2) for line in f]
    names = []
    requests = []
    distance_matrix = []
    for line in splitted:
        names.append(line[0])
        requests.append(line[1])
        distance_matrix.append(line[2].strip().split(','))
    # names = [line.strip().split(' # ', 2)[0] for line in f]
    # request = [line.strip().split(' # ', 2)[1] for line in f]
    # distance_matrix = [line.strip().split(' # ', 2)[2].strip().split(',') for line in f]

    return names, requests, distance_matrix


def is_matrix_square(matrix):
    N = len(matrix)
    for row in range(N):
        if len(matrix[row]) != N:
            return False
    return True


def convert_matrix_elements_to_int(matrix):
    return [list(map(int, row)) for row in matrix]


def get_data(matrix):
    names = []
    requests = []
    distance_matrix = []
    matrix = matrix.splitlines()
    for line in matrix:
        names.append(line.split(' # ', 2)[0])
        requests.append(line.split(' # ', 2)[1].strip())
        distance_matrix.append(line.split(' # ', 2)[2].strip().split(','))

    return names, requests, distance_matrix


def main():
    # v = 40  # prędkość ciężarówki
    # names = {1: "Szewska",
    #          2: "Floriańska",
    #          3: "Grodzka",
    #          4: "Pawia",
    #          5: "Jasnogórska",
    #          6: "Wadowicka",
    #          7: "Aleja Generała Tadeusza Bora-K",
    #          8: "Stawowa",
    #          9: "Pilotów",
    #          10: "Mieczysława Medwieckiego",
    #          11: "Podgórska",
    #          12: "Wielicka",
    #          13: "Opolska",
    #          14: "Tadeusza Śliwiaka",
    #          15: "Aleja Pokoju",
    #          16: "Stanisława Stojałowskiego",
    #          17: "Henryka Kamińskiego"}
    #
    # Restaurants = GraphMatrix()
    # truck = Truck()
    # Restaurants.insertVertex(Vertex(is_base=True))
    # for i in names.keys():
    #     vertex = Vertex(Id=i, name=names[i], is_base=False)
    #     if vertex not in Restaurants.list:
    #         Restaurants.insertVertex(vertex)
    #
    # for i in range(Restaurants.order()):
    #     for j in range(Restaurants.order()):
    #         if i != j and not Restaurants.matrix[i][j]:
    #             distance = round(uniform(0.3, 5), 2)  # odległość między dwoma restauracjami - od 300 metrów do 5
    #             # kilometrów
    #             time = round(distance / v, 2)  # obliczony czas przejazdu w godzinach dla średniej prędkości 50 km/h
    #             Restaurants.insertEdge(vertex1_idx=i, vertex2_idx=j, edge=Edge(i, j, time=time, distance=distance))
    #             Restaurants.insertEdge(vertex1_idx=j, vertex2_idx=i, edge=Edge(j, i, time=time, distance=distance))
    #
    # # test_solution = find_solution(Restaurants, truck)
    # # print(test_solution, '\n')
    # # test_neighbours = neighbourhood(graph=Restaurants, solution=test_solution)
    # # for i in range(len(test_neighbours)):
    # #     print(test_neighbours[i])
    #
    # test_solution = bee_algorythm(graph=Restaurants, truck=truck)
    # print('Najlepsze znalezione rozwiązanie:\n', test_solution)

    file_1 = 'Dane_1.txt'
    file_2 = r'C:\Users\adamz\Downloads\Dane_2.txt'
    file_3 = r'C:\Users\adamz\Downloads\Dane_3.txt'

    actual_file = file_3
    matrix = save_data_from_txt_to_matrix(actual_file)

    if is_matrix_square(matrix):
        matrix = convert_matrix_elements_to_int(matrix)
    else:
        print(f"Macierz z pliku '{actual_file}' nie jest kwadratowa!")


if __name__ == '__main__':
    main()
