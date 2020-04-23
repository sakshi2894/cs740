from random import seed
from random import randint
import math

seed(1)

G = {
    1 : [2, 10],
    2 : [3, 8, 1],
    3 : [2, 4, 6],
    4 : [3, 5],
    5 : [4, 6, 7],
    6 : [3, 5, 7],
    7 : [5, 6, 9],
    8 : [2, 6, 9],
    9 : [7, 8, 10],
    10: [1, 9]
}

M = {
    "a" : [10, 2, 8],
    "b" : [10, 2, 7],
    "c" : [8, 3, 6, 7],
    "d" : [8, 6, 7]
}

V_fn = [2, 3, 6, 7, 8, 9, 10]
V_sw = [1, 4, 5]

threshold_bw = 7
threshold_cpu = 7

flows = [
    [1, "a", "b", "c", "d", 5],
    [1, "a", "b", 3],
    [1, "a", 2],
    [2, "b", 6],
    [1, "b", "a", 5],
    [4, "b", 5],
    [1, "b" , "c", "d", 6],
    [3, "d", "a", 7],
    [7, "c" ,"d", 10],
    [4, "b", "d", 8]
]

fbw = []
fcpu = []
C_bw = {}
C_cpu = {}
r_bw = {}
r_cpu = {}

def generate_Cbw():
    for node in G:
        for edge in G[node]:
            key = str(node) + '-' + str(edge)
            C_bw[key] = randint(20, 50)

def generate_Ccpu():
    for node in G:
        C_cpu[node] = randint(20, 50)

def generate_fbw():
    for i in flows:
        fbw.append(randint(1, 10))

def generate_fcpu():
    for i in flows:
        fcpu.append(randint(1, 10))

def initialize_rbw():
    for edge in C_bw:
        r_bw[edge] = 1

def initialize_rcpu():
    for node in C_cpu:
        r_cpu[node] = 1

def get_max_cpu():
    max_cpu = 0
    max_node = 0
    for node in C_cpu:
        if C_cpu[node] > max_cpu:
            max_cpu = C_cpu[node]
            max_node = node
    return [max_node, max_cpu]

def get_max_bw():
    max_bw = 0
    max_edge = ''
    for edge in C_bw:
        if C_bw[edge] > max_bw:
            max_bw = C_bw[edge]
            max_edge = edge
    return [max_edge, max_bw]

def dijkstra(src,dest,v_bw,visited=[],distances={},predecessors={}):
    #print(src, dest)
    if src == dest:
        path = []
        pred = dest
        while pred != None:
            path.append(pred)
            pred = predecessors.get(pred, None)
        #print(path)
        return path
    else:
        if not visited:
            distances[src] = 0

        for neighbour in G[src]:
            if neighbour not in visited:
                key = str(src) + '-' + str(neighbour)
                new_distance = distances[src] + v_bw[key]
                if new_distance < distances.get(neighbour,float('inf')):
                    distances[neighbour] = new_distance
                    predecessors[neighbour] = src

        visited.append(src)
        unvisited={}
        for k in G:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = sorted(unvisited, key=unvisited.get)
        if unvisited:
            return dijkstra(x[0], dest, v_bw, visited, distances, predecessors)


def construct_LFG(v_bw, v_cpu, index):
    G_cap = {}
    eta = [[flows[index][0]]]
    for j in range(1, len(flows[index])-1):
        m_type = flows[index][j]
        eta.append(M[m_type])
    eta.append([flows[index][len(flows[index])-1]])

    v_cap_cost = {}

    for j in range(0, len(eta)-1):
        for u_cap in eta[j]:
            for v_cap in eta[j+1]:
                shortest_path = dijkstra(u_cap, v_cap, v_bw)
                #print('src,dest', u_cap, ' ', v_cap)
                #print('s', shortest_path)

                if shortest_path != None:
                    v_sum_bw = 0
                    v_sum_cpu = 0
                    for i in range(len(shortest_path)-1):
                        key = str(shortest_path[i]) + '-' + str(shortest_path[i+1])
                        v_sum_bw = v_sum_bw + v_bw[key]
                        v_sum_cpu = v_sum_cpu + float((v_cpu[shortest_path[i]] + v_cpu[shortest_path[i+1]])/2)

                    key = str(u_cap) + '-' + str(v_cap)
                    v_cap_cost[key] = v_sum_bw + v_sum_cpu
                    if u_cap not in G_cap:
                        G_cap[u_cap] = [v_cap]
                    else:
                        G_cap[u_cap].append(v_cap)
    return G_cap, v_cap_cost







def RA_RA(index, flow, K):
    k = 1
    output_LFG =[]
    output = []
    required_bw = fbw[index]
    required_cpu = fcpu[index]
    G_new = {}
    for node in G:
        if C_cpu[node] >= required_cpu:
            for edge in G[node]:
                key = str(node) + '-' + str(edge)
                if C_cpu[edge] >= required_cpu and C_bw[key] >= required_bw:
                    if node not in G_new:
                        G_new = [edge]
                    else:
                        G_new.append(edge)

    max_cpu = get_max_cpu()
    max_bw = get_max_bw()
    v_bw = {}
    v_cpu = {}

    for edge in C_bw:
        if fbw[index] > threshold_bw:
            v_bw[edge] = max_bw[1]/(r_bw[edge]*C_bw[edge] - fbw[index])
        else:
            v_bw[edge] = 0

    for node in C_cpu:
        if fcpu[index] > threshold_cpu:
            v_cpu[node] = max_cpu[1]/(r_cpu[node]*C_cpu[node] - fcpu[index])
        else:
            v_cpu[node] = 0

    LFG, LFG_cost = construct_LFG(v_bw, v_cpu, index)
    print(LFG)



def main():
    generate_fbw()
    generate_fcpu()
    generate_Cbw()
    generate_Ccpu()
    initialize_rbw()
    initialize_rcpu()
    K = 5
    for i in range(len(flows)):
        RA_RA(i, flows[i], K)

if __name__ == '__main__':
    main()