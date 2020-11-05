import os
from IPython.display import FileLink
import networkx as nx
import csv
import math
import random
from collections import namedtuple


for dirname, _, filenames in os.walk('./data'):
    for filename in filenames:
        os.path.join(dirname, filename)


def submission_generation(filename, str_output):
    os.chdir(r'./result')
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in str_output:
            writer.writerow(item)
    return FileLink(filename)


def check_solution(node_count, solution, points):
    solutionCheck = sorted(solution, key=lambda x: x)

    for i in range(node_count):
        if solutionCheck[i] != i:
            print("solución inválida, no se recorren todas la ciudades")
            return 0

    return tourLength(points, solution, node_count)


def tourLength(points, solution, nodeCount):

    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    return obj


def edgesFromZero(orden):
    orden = sorted(orden, key=lambda p: -length(p, Point(0, 0)))
    return orden


def edgesFromCentroid(orden):
    x = 0
    y = 0

    for point in orden:
        x += point[0]
        y += point[1]

    meanPoint = Point(x/len(orden), y / len(orden))
    orden = sorted(orden, key=lambda p: -length(p, meanPoint))
    return orden


def edgesFromOutlayer(orden):
    x = 0
    y = 0

    for point in orden:
        x += point[0]
        y += point[1]

    Outlayer = Point(x, y)
    orden = sorted(orden, key=lambda p: -length(p, Outlayer))
    return orden


def christofides(nodeCount, G):
    T = nx.MultiGraph()
    minumumTree = nx.minimum_spanning_tree(G).edges
    T.add_edges_from(minumumTree)

    return list(nx.dfs_preorder_nodes(T))


def incomplexGraf(G, nodeCount, points):
    G = nx.MultiGraph()

    for i in range(nodeCount - 1):
        for j in range(i + 1, i + 200):
            if j < nodeCount:
                G.add_edge(i, j, weight=length(points[i], points[j]))
    return G


def twoOpt(orden, points):
    longA = tourLength(points, orden, len(orden))
    for i in range(len(orden) - 2):

        ordenb = orden.copy()
        aux = ordenb[i + 1]
        ordenb[i + 1] = ordenb[i + 2]
        ordenb[i + 2] = aux
        longB = tourLength(points, ordenb, len(ordenb))

        if longA > longB:
            orden = ordenb
            longA = longB

    return orden

def costSA(theta):
    return -(theta/math.log(0.99))


def reverseOrder(order):
    a = random.randint(0, len(order) - 1)
    b = random.randint(0, len(order) - 1)
    result = order.copy()

    for i in range(b - a):
        result[a + i] = order[b - i]

    return result


Point = namedtuple("Point", ['x', 'y'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def solve_it(input_data):

    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    solution = []
    points = []

    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
        solution.append(i-1)

    G = nx.MultiGraph()

    if nodeCount < 1000:

        for i in range(nodeCount):
            for j in range(i + 1, nodeCount):
                G.add_edge(i, j, weight=length(points[i], points[j]))

        solution = christofides(nodeCount, G)

    else:
        G = incomplexGraf(G, nodeCount, points)
        solution = christofides(nodeCount, G)








    value = check_solution(nodeCount, solution, points)

    print(value)

    # prepare the solution in the specified output format
    output_data = '%.2f' % value + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data, value


str_output = [["Filename","Value"]]

valueT = 0

for dirname, _, filenames in os.walk('./data'):
    for filename in filenames:
        full_name = dirname+'/'+filename
        with open(full_name, 'r') as input_data_file:
            input_data = input_data_file.read()
            output, value = solve_it(input_data)
            str_output.append([filename, str(value)])
            valueT += value
            print("11111111111111111111111111111111111111111111")


print(valueT)

submission_generation('sample_submission_non_sorted.csv', str_output)

reader = csv.reader(open("sample_submission_non_sorted.csv"))

sortedlist = sorted(reader, key=lambda row: row[0], reverse=False)

submission_generation('sample_submission.csv', sortedlist)
