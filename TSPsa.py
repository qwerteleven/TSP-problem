import os
from IPython.display import FileLink
import networkx as nx
import csv
import math
import random
import numpy as np
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
    W = nx.Graph()

    for i in range(nodeCount):
        if T.degree[i] % 2 != 0:
            W.add_edges_from(T.edges(i))

    if len(W) > 0:
        M = dict(nx.all_pairs_shortest_path_length(W))
        if '1' in M:
            T.add_edges_from(M[1].items())

    return list(nx.dfs_preorder_nodes(T))


def incomplexGraf(nodeCount, points):
    G = nx.MultiGraph()

    for i in range(nodeCount - 1):
        for j in range(i + 1, i + 50):
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
    return -(theta/math.log(0.9))


def reverseOrder(order):
    a = random.randint(0, len(order) - 2)
    result = order.copy()
    aux = order[a + 1]
    result[a + 1] = order[a]
    result[a] = aux

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


    alpha = 0.9
    value = check_solution(nodeCount, solution, points)

    t = costSA(len(solution))
    print(value)

    mejoraCount = 0

    while(mejoraCount < 1000):
        newSolution = reverseOrder(solution)
        newValue = check_solution(nodeCount, newSolution, points)
        theta = newValue - value
        if theta > 0:
            u = np.random.uniform(0, 1)
            if u <= math.exp(-(theta/t)):
                solution = newSolution
                value = newValue
        else:
            solution = newSolution
            value = newValue

        mejoraCount = mejoraCount + 1
        t = alpha * t

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
