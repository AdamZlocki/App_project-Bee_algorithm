from random import randint, uniform, choice
from statistics import mean


class Vertex:  # wierzchołek - restauracja; reprezentuje id, nazwa(łatwość wprowadzania danych przez użytkownika) i
    # informuje o swoim zapotrzebowaniu
    def __init__(self, Id=None, name=None, is_base=False):
        if not is_base:
            self.Id = Id
            self.name = name
            self.visited = 0
            self.request = randint(100, 999)
        else:
            self.Id = 0
            self.name = "Base"
            self.visited = 1

    def __eq__(self, other):
        if self.name == other.name or self.Id == other.Id:
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
        self.neighbourhood_mean_cost = 0

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
        if self.neighbourhood_mean_cost > other.neighbourhood_mean_cost:
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
    penalty = 10 * (route.count(0) - 1)
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


def bee_algorythm(graph: GraphMatrix, truck: Truck, num_of_iterations: int = 10, size_of_iteration: int = 5, num_of_bests: int = 2, size_of_neighbourhood: int = 10):
    solutions = []
    counter_of_iterations = 0
    while counter_of_iterations < num_of_iterations:  # dopóki nie wykonano oczekiwanej liczby iteracji powtarzamy
        while len(solutions) < size_of_iteration:  # utworzenie zadanej ilości początkowych rozwiązań
            sol = find_solution(graph=graph, truck=truck)
            if sol not in solutions:
                solutions.append(sol)

        for solution in solutions:  # utworzenie sąsiedztwa każdego rozwiązania i obliczenie średniego kosztu w
            # sąsiedztwie
            solution.neighbourhood = neighbourhood(graph=graph, solution=solution, size=size_of_neighbourhood)
            neighbourhood_cost_list = []
            for neighbour in solution.neighbourhood:
                neighbourhood_cost_list.append(neighbour.cost)
            solution.neighbourhood_mean_cost = mean(neighbourhood_cost_list)

        best_solutions = []  # znalezienie oczekiwanej liczby najlepszych rozwiązań
        while len(best_solutions) < num_of_bests:
            best_solutions.append(solutions.pop(solutions.index(min(solutions))))
        solutions = best_solutions
        counter_of_iterations += 1

    return solutions[0]







def main():
    v = 40  # prędkość ciężarówki
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

    Restaurants = GraphMatrix()
    truck = Truck()
    Restaurants.insertVertex(Vertex(is_base=True))
    for i in names.keys():
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

    # test_solution = find_solution(Restaurants, truck)
    # print(test_solution, '\n')
    # test_neighbours = neighbourhood(graph=Restaurants, solution=test_solution)
    # for i in range(len(test_neighbours)):
    #     print(test_neighbours[i])

    test_solution = bee_algorythm(graph=Restaurants, truck=truck)
    print(test_solution)


if __name__ == '__main__':
    main()
