from random import seed
from random import randint
from  random import uniform
from Network import flows, mbox_types, nw_graph, top_mbox, ce, pm

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
    rls = []
    for i in range(0, len(flows)):
        rl = []
        generate_rls_flow(i, rl, 0, [])
        rls.append(rl)
    return rls


def bfs_shortest_path(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        return None

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
def generate_gre(rls, fl_e):
    gre = []
    for i in range(0, len(rls)):
        energy = fl_e[i]
        for j in range(0, len(rls[i])):
            edges = []
            for k in range(0, len(rls[i][j]) - 1):
                gen_edges = generate_edges(rls[i][j][k], rls[i][j][k + 1])
                if gen_edges == None:
                    continue

                if k != 0:
                    edges = edges + gen_edges[1:]
                else:
                    edges = edges + gen_edges

            # print(edges)
            edge_weights = {}
            for l in range(0, len(edges) - 1):
                edge = get_key(edges[l], edges[l + 1])
                if edge not in edge_weights:
                    edge_weights[edge] = 0
                edge_weights[edge] = edge_weights[edge] + energy

            gre.append(edge_weights)

    return gre


def generate_ce():
    ce = {}
    for key in nw_graph:
        for val in nw_graph[key]:
            strkey = str(val) + "-" + str(key)
            if strkey in ce:
                ce[str(key) + "-" + str(val)] = ce[str(val) + "-" + str(key)]
            else:
                ce[str(key) + "-" + str(val)] = randint(20, 50)
    return ce


def generate_fl():
    fl = []
    for i in flows:
        fl.append(1)
    return fl


def generate_fl_edges():
    fl_e = []
    for i in flows:
        fl_e.append(uniform(1,5))
    return fl_e


def generate_fl_pm():
    fl_pm = []
    for i in flows:
        fl_pm.append(randint(1, 4))
    return fl_pm


def generate_pm():
    pm = {}
    for key in top_mbox:
        pm[key] = randint(25, 30)
    return pm


def generate_qrm(rls, fl_pm):
    qrm = []
    for i in range(0, len(rls)):
        energy = fl_pm[i]
        for j in range(0, len(rls[i])):
            mbox_in_r = {}
            for k in range(0, len(rls[i][j])):
                if rls[i][j][k] in top_mbox:
                    if (rls[i][j][k] not in mbox_in_r):
                        mbox_in_r[rls[i][j][k]] = 0
                    mbox_in_r[rls[i][j][k]] += energy
            qrm.append(mbox_in_r)
    return qrm

def get_key(a, b):
    min_number = min(a,b)
    max_number = max(a,b)
    return str(min_number)+'-'+str(max_number)

def generate_data():
    seed(1)
    rls = generate_rls()
    fl = generate_fl()
    fl_e = generate_fl_edges()
    print("FLow Cost: "+str(fl_e))
    fl_pm = generate_fl_pm()
    #pm = generate_pm()
    gre = generate_gre(rls, fl_e)
    qrm = generate_qrm(rls, fl_pm)
    return rls, gre, ce, fl, pm, qrm, fl_e,fl_pm


def get_network_values():
    return flows, mbox_types, nw_graph,top_mbox

