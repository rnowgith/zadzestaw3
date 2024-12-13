import numpy as np
import json
import heapq
from dataclasses import dataclass


def multiply(x, y):
    z = np.zeros([len(x), len(y[0])])
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(x[0])):
                z[i][j] += x[i][k] * y[k][j]

    return z


@dataclass
class DaneOsobowe:
    imie: str
    nazwisko: str
    adres: str
    kod_pocztowy: str
    pesel: str

#    def __init__(self, imie, nazwisko, adres, kod_pocztowy, pesel):
#        self.imie = imie
#        self.nazwisko = nazwisko
#        self.adres = adres
#        self.kod_pocztowy = kod_pocztowy
#        self.pesel = pesel

    def savetojson(self):
        with open('dump.json', 'w') as file_json:
            json.dump(self.__dict__, file_json)

    @staticmethod
    def loadfromjson():
        with open('dump.json', 'r') as file_json:
            dane = json.load(file_json)
        return DaneOsobowe(**dane)


class Graph:
    def __init__(self):
        self.graph = {}

    def addnode(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def addedge(self, node1, node2, weigth):
        self.addnode(node1)
        self.addnode(node2)
        self.graph[node1].append((node2, weigth))
        self.graph[node2].append((node1, weigth))

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            currentdistance, currentnode = heapq.heappop(queue)

            if currentdistance > distances[currentnode]:
                continue

            for neighbor, weight in self.graph[currentnode]:
                distance = currentdistance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        return distances


class TrieNode:
    def __init__(self):
        self.children = {}
        self.output = []
        self.fail = None


def buildautomaton(keywords):
    root = TrieNode()
    for keyword in keywords:
        node = root
        for char in keyword:
            node = node.children.setdefault(char, TrieNode())
        node.output.append(keyword)
    queue = []
    for node in root.children.values():
        queue.append(node)
        node.fail = root
    while queue:
        currentnode = queue.pop(0)
        for key, next_node in currentnode.children.items():
            queue.append(next_node)
            fail_node = currentnode.fail
            while fail_node and key not in fail_node.children:
                fail_node = fail_node.fail
            next_node.fail = fail_node.children[key] if fail_node else root
            next_node.output += next_node.fail.output
    return root


def searchtext(text, keywords):
    root = buildautomaton(keywords)
    result = {keyword: [] for keyword in keywords}

    currentnode = root
    for i, char in enumerate(text):
        while currentnode and char not in currentnode.children:
            currentnode = currentnode.fail
        if not currentnode:
            currentnode = root
            continue
        currentnode = currentnode.children[char]
        for keyword in currentnode.output:
            result[keyword].append(i - len(keyword) + 1)
    return result


class State:
    def __init__(self):
        self.outputs = []
        self.nextstates = []

    def output(self, input):
        return self.outputs[input]

    def nextstate(self, input):
        return self.nextstates[input]


class Moore:
    def __init__(self, state):
        self.currentstate = state

    def next(self, input):
        output = self.currentstate.output(input)
        self.currentstate = self.currentstate.nextstate(input)
        return output


def enlarge(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


@enlarge
def enl(text):
    return text


x = [[1]]
y = [[1, 2]]
print(multiply(x, y))

# d1 = DaneOsobowe('Jan', 'Kowalski', 'ul. Polna 12', '00-123', '12345678901')
d1 = DaneOsobowe(imie="Jan", nazwisko="Kowalski", adres="ul. Polna 12", kod_pocztowy="00-123", pesel="12345678901")
d1.savetojson()
d2 = DaneOsobowe.loadfromjson()
if d1.__dict__ == d2.__dict__:
    print("ok")

graph = Graph()
graph.addedge('A', 'B', 1)
graph.addedge('A', 'C', 4)
graph.addedge('B', 'C', 2)
graph.addedge('B', 'D', 5)
graph.addedge('C', 'D', 1)
print(graph.dijkstra('A'))

print(searchtext("she", ["she", "he"]))

state1 = State()
state2 = State()
state1.outputs = [0, 1]
state1.nextstates = [state1, state2]
state2.outputs = [1, 0]
state2.nextstates = [state1, state2]
moore = Moore(state1)
print(moore.next(1))
print(moore.next(1))

print(enl("aaa"))
