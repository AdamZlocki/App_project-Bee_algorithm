class Vertex:  # wierzchołek - restauracja; reprezentuje id, nazwa(łatwość wprowadzania danych przez użytkownika) i
    # informuje o swoim zapotrzebowaniu
    def __init__(self, id, name, request):
        self.id = id
        self.name = name
        self.visited = 0
        self.request = request

    def __eq__(self, other):
        if self.name == other.name or self.id == self.id:
            return True
        else:
            return False


class Edge:  # połączenie między restauracjami; reprezentuje czas przejazdu i odległość
    def __init__(self, start, end, time=0, distance=0):
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
    def __init__(self, capacity=1000):
        self.capacity = capacity


class Solution:  # postać rozwiązania; route to trasa w postaci listy id restauracji w kolejności odwiedzania,
    # cost to wyliczona wartość funkcji celu
    def __init__(self, route, cost):
        self.route = route
        self.cost = cost

    def __eq__(self, other):
        if self.route == other.route:
            return True
        else:
            return False


def Target_funtion(route):  #funkcja obliczająca funkcję celu
    cost = 0

    return cost


if __name__ == '__main__':
    print(0)
