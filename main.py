from random import seed
from random import randint
import numpy as np
from scipy.optimize import linprog

seed(1)
# Topology
nw_graph = {
    1: [2, 3, 7],
    2: [1, 4, 5],
    3: [1, 5],
    4: [2, 6, 8],
    5: [2, 3, 6, 9],
    6: [4, 5],

    7: [1],
    8: [4],
    9: [5]
}

mbox_types = {
    "p": [7, 8],
    "f": [9]
}

top_mbox = {
    7: 1,
    8: 4,
    9: 5
}

# Flows
flows = [
    [1, "p", "f", 3],
    [1, "p", 2],
    [2, "f", 6],
    [1, "f", "p", 5],
    [4, "f", 4]
]


rls = []
gre = []
ce = {}
fl = []


# Generate Rls
def generate_rls_flow(ind, rl, node_index, arr):
    flow = flows[ind]
    if node_index == len(flow):
        rl.append(arr)
        return

    if node_index == 0 or node_index == (len(flow) - 1):
        arr.append(flow[node_index])
        generate_rls_flow(ind, rl, node_index + 1, arr.copy())
    else:
        for j in range(0, len(mbox_types.get(flow[node_index]))):
            arr.append(mbox_types.get(flow[node_index])[j])
            generate_rls_flow(ind, rl, node_index + 1, arr.copy())
            arr = arr[:-1]


def generate_rls():
    for i in range(0, len(flows)):
        rl = []
        generate_rls_flow(i, rl, 0, [])
        rls.append(rl)


def bfs_shortest_path(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        return "That was easy! Start = goal"

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)


def generate_edges(src, dest):
    path = bfs_shortest_path(nw_graph, src, dest)
    return path


# Generate Gre

# ASSUMPTIONS
# 1. Different weights for different directions.
# 2. Gre will be an array of dictionaries wrt rls not differentiating
#    wrt flows (assuming fl will take care)
def generate_gre():
    for i in range(0, len(rls)):
        for j in range(0, len(rls[i])):
            edges = []
            for k in range(0, len(rls[i][j]) - 1):
                gen_edges = generate_edges(rls[i][j][k], rls[i][j][k + 1])

                if k != 0:
                    edges = edges + gen_edges[1:]
                else:
                    edges = edges + gen_edges

           # print(edges)
            edge_weights = {}
            for l in range(0, len(edges) - 1):
                edge = str(edges[l]) + "-" + str(edges[l + 1])
                edge_weights[edge] = randint(1, 5)

            gre.append(edge_weights)


# TODO: Generate random weights
def generate_ce():
    for key in nw_graph:
        for val in nw_graph[key]:
            ce[str(key) + "-" + str(val)] = randint(20, 50)


def generate_fl():
    for i in flows:
        fl.append(randint(1, 5))


def generate_data():
    generate_rls()
    generate_gre()
    generate_ce()
    generate_fl()

    print(flows)
    print(rls)
    print(gre)
    print(ce)
    print(fl)


def simplex():
    c = []
    eq1 = []
    eq2 = []
    eq5 = []
    num_rls = 0
    rls_arr = []

    A = []
    b = []

    # Optimization function
    for i in range(len(rls)):
        f = fl[i]
        rl_count = 0
        for j in rls[i]:
            c.append(f * -1)
            num_rls = num_rls + 1
            rl_count = rl_count + 1
        rls_arr.append(rl_count)
    constants = np.array(c)


    # Equation 1
    cum_rls = 0
    for i in range(len(fl)):
        arr = [0] * num_rls
        for j in range(cum_rls, cum_rls + rls_arr[i]):
            arr[j] = 1
        cum_rls = cum_rls + rls_arr[i]
        A.append(arr)
        b.append(1)

    # Equation 5
    iterator = 0
    for i in range(len(rls)):
        for j in rls[i]:
            arr = [0] * num_rls
            arr[iterator] = -1
            iterator = iterator + 1
            A.append(arr)
            b.append(0)


    # Equation 2
    for key in ce:
        cum_rls = 0
        arr = [0] * num_rls
        for i in range(len(flows)):
            for j in range(cum_rls, cum_rls + rls_arr[i]):
                if key in gre[j]:
                    arr[j] = fl[i] * gre[j][key]
            cum_rls = cum_rls + rls_arr[i]
        A.append(arr)
        b.append(ce[key])

    res = linprog(constants, A_ub=np.array(A), b_ub=np.array(b), bounds=(0, None),  method='simplex')
    print('Optimal value:', res.fun, '\nX:', res.x)



    print(A)



def main():
    generate_data()
    simplex()

main()