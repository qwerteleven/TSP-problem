import os
from IPython.display import FileLink
import csv
import math
import random
import heapq
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


def poblationInicializator(genotipes, nodeCount):
    poblation = []

    for i in range(genotipes):
        a = np.arange(0, nodeCount - 1)
        np.random.shuffle(a)
        poblation.append(a)

    return poblation


def mutation(arr):
    a = random.randint(0, len(arr))
    b = random.randint(0, len(arr))
    c = arr[a]
    arr[a] = arr[b]
    arr[b] = c

    return arr


def solve_it(input_data):

    lines = input_data.split('\n')

    nodeCount = int(lines[0])
    genotipes = 20

    poblation = poblationInicializator(genotipes, nodeCount)

    print(poblation)

    """
    points = []
    solution = []
    adaptation = {}
    padre = []


    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
        padre.append(i-1)



    for i in range(100):
        adaptation.clear()

        adaptation["padre"] = check_solution(nodeCount, solutions[0], points)
        adaptation["madre"] = check_solution(nodeCount, solutions[1], points)

        for i in range(2, int(nodeCount/10) - 2, 2):

            solutions[i] = indexGen(solutions[0], solutions[1])
            adaptation["bastard"] = check_solution(nodeCount, solutions[i], points)

            solutions[i + 1] = legit(solutions[0], solutions[1], nodeCount)
            adaptation["legit"] = check_solution(nodeCount, solutions[i + 1], points)


        bestAdaptation(adaptation)

        solutions[0] = solutions[adaptation["newpadre"]]
        solutions[1] = solutions[adaptation["newmadre"]]

        if adaptation["padre"] < value:
            value = adaptation["padre"]
            solution = solutions[0].copy()

        if random.uniform(0, 1) < 0.001:
            mutationSolution(solutions[0])
            mutationSolution(solutions[1])

    value = check_solution(nodeCount, solution, points)

    print(value)
    # prepare the solution in the specified output format
    output_data = '%.2f' % value + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data, value
"""

str_output = [["Filename", "Value"]]

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
