from random import randint, uniform


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
            self.visited = 0

    def __eq__(self, other):
        if self.name == other.name or self.Id == other.Id:
            return True
        else:
            return False

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


class Truck:  # ciężarówka; zadana pojemność
    def __init__(self, capacity=3000):
        self.capacity = capacity


class Solution:  # postać rozwiązania; route to trasa w postaci listy id restauracji w kolejności odwiedzania,
    # cost to wyliczona wartość funkcji celu
    def __init__(self, route, edges, cost):
        self.route = route
        self.edges = edges
        self.cost = cost

    def __eq__(self, other):
        if self.route == other.route:
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
            self.matrix[vertex1_idx][vertex2_idx] = (edge.distance, edge.time)

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
            if self.matrix[vertex_idx][i] == 1:
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
                    result.append((self.list[i].key, self.list[j].key))
        return result


def Target_funtion(edges, w=2.68, p=20):  # funkcja obliczająca funkcję celu; w = koszt paliwa za przejechanie
    # jednego kilometra, p = godzionwe wynagordzenie kierowcy
    cost = 0
    for edge in edges:
        cost += edge[0] * w + edge[1] * p
    return cost


def main():
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
    Restaurants.insertVertex(Vertex(is_base=True))
    for i in names.keys():
        vertex = Vertex(Id=i, name=names[i], is_base=False)
        if not vertex in Restaurants.list:
            Restaurants.insertVertex(Vertex(Id=i, name=names[i]))

    for i in range(Restaurants.order()):
        for j in range(Restaurants.order()):
            if i != j:
                distance = uniform(0.3, 5)  # odległość między dwoma restauracjami - od 300 metrów do 5 kilometrów
                time = distance/50  # obliczony czas przejazdu w godzinach dla średniej prędkości 50 km/h
                Restaurants.insertEdge(vertex1_idx=i, vertex2_idx=j, edge=Edge(i, j, time=time, distance=distance))

if __name__ == '__main__':
    main()
