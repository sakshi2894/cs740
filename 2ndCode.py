from random import seed
from random import randint
import math
import heapq
import numpy
from DataGenerator import generate_data,get_network_values

seed(1)

# G = {
#     1 : [2, 10],
#     2 : [3, 8, 1],
#     3 : [2, 4, 6],
#     4 : [3, 5],
#     5 : [4, 6, 7],
#     6 : [3, 5, 7, 8],
#     7 : [5, 6, 9],
#     8 : [2, 6, 9],
#     9 : [7, 8, 10],
#     10: [1, 9]
# }



# M = {
#     "a" : [10, 2, 8],
#     "b" : [10, 2, 7],
#     "c" : [8, 3, 6, 7],
#     "d" : [8, 6, 7]
# }

# V_fn = [2, 3, 6, 7, 8, 9, 10]
# V_sw = [1, 4, 5]
#
#
#
# flows = [
#     [1, "a", "b", 3],
#     [1, "a", "b", "c", "d", 5],
#     [1, "a", 2],
#     [2, "b", 6],
#     [1, "b", "a", 5],
#     [4, "b", 5],
#     [1, "b" , "c", "d", 6],
#     [3, "d", "a", 7],
#     [7, "c" ,"d", 10],
#     [4, "b", "d", 8]
# ]


def get_key(a, b):
    min_number = min(a,b)
    max_number = max(a,b)
    return str(min_number)+'-'+str(max_number)


## Is the graph bi-directional?
def generate_Cbw():
    for node in G:
        for edge in G[node]:
            key = str(node) + '-' + str(edge)
            C_bw[key] = randint(100, 150)

def generate_Ccpu():
    for node in G:
        C_cpu[node] = randint(100, 150)

def generate_fbw():
    for i in flows:
        fbw.append(randint(15, 30))

def generate_fcpu():
    for i in flows:
        fcpu.append(randint(15, 30))

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

def bfs_shortest_path(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        return [start,goal]

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

def dijkstra(graph,src,dest,v_bw,K):
    heap = []
    heapq.heapify(heap)
    final_paths = []
    paths = {}
    counts = {}
    for key in graph:
        counts[key] = 0;
    paths[src] = [src]
    heapq.heappush(heap,(0,src,paths[src]))
    while(len(heap)>0 & counts[dest]<K):
        cost,curr_node,path = heapq.heappop(heap)
        counts[curr_node] = counts[curr_node]+1
        if curr_node==dest:
            final_paths.append(path)
        if(counts[curr_node]<=K):
            for neighbour in graph[curr_node]:
                key = str(curr_node) + '-' + str(neighbour)
                new_distance = cost + v_bw[key]
                path_neibhour = path + [neighbour]
                heapq.heappush(heap,(new_distance,neighbour,path_neibhour))
    return final_paths
    # if src == dest:
    #     path = []
    #     pred = dest
    #     while pred != None:
    #         path.append(pred)
    #         pred = predecessors.get(pred, None)
    #     #print(path)
    #     return path
    # else:
    #     if not visited:
    #         distances[src] = 0
    #
    #     for neighbour in graph[src]:
    #         if neighbour not in visited:
    #             key = str(src) + '-' + str(neighbour)
    #             new_distance = distances[src] + v_bw[key]
    #             if new_distance < distances.get(neighbour,float('inf')):
    #                 distances[neighbour] = new_distance
    #                 predecessors[neighbour] = src
    #
    #     visited[src]=True
    #     unvisited={}
    #     for k in graph:
    #         if k not in visited:
    #             unvisited[k] = distances.get(k, float('inf'))
    #     x = sorted(unvisited, key=unvisited.get)
    #     if unvisited:
    #         return dijkstra(graph, x[0], dest, v_bw, visited, distances, predecessors)


def construct_LFG(graph, v_bw, v_cpu, index):
    G_cap = {}
    #print('eta')
    eta = [[flows[index][0]]]
    for j in range(1, len(flows[index])-1):
        m_type = flows[index][j]
        eta.append(M[m_type])
    eta.append([flows[index][len(flows[index])-1]])
    #print(eta)

    v_cap_cost = {}
    last_column=0
    for j in range(0, len(eta)-1):
        last_column=j+1
        shortest_path = None
        found_one_path = False
        for u_cap in eta[j]:
            for v_cap in eta[j+1]:
                if u_cap in graph and v_cap in graph and u_cap != v_cap:
                    #shortest_path = dijkstra(graph, u_cap, v_cap, v_bw)
                    shortest_path = bfs_shortest_path(graph, u_cap, v_cap)
                elif u_cap in graph and v_cap in graph and u_cap == v_cap:
                    shortest_path = [u_cap, v_cap]
                #print('src,dest', u_cap, ' ', v_cap)
                #print('s', shortest_path)

                if shortest_path != None:
                    found_one_path = True
                    v_sum_bw = 0
                    v_sum_cpu = 0
                    for i in range(len(shortest_path)-1):
                        if shortest_path[i] != shortest_path[i+1]:
                            key = get_key(shortest_path[i],shortest_path[i+1])
                            v_sum_bw = v_sum_bw + v_bw[key]

                    if(u_cap in V_fn):
                        v_sum_cpu = v_cpu[u_cap]
                    if(v_cap in V_fn):
                        v_sum_cpu = v_sum_cpu + v_cpu[v_cap]
                    node1 = str(u_cap)+"_"+str(j)
                    node2 = str(v_cap)+"_"+str(j+1)
                    key = node1 + '-' + node2

                    v_cap_cost[key] = v_sum_bw + v_sum_cpu
                    if node1 not in G_cap:
                        G_cap[node1] = [node2]
                    else:
                        G_cap[node1].append(node2)

                    if node2 not in G_cap:
                        G_cap[node2] = []
        if(not found_one_path):
            return None,None,None
    return G_cap, v_cap_cost,last_column







def RA_RA(index, flow, K):

    required_bw = fbw[index]
    required_cpu = fcpu[index]
    G_new = {}
    for node in G:
        if node in V_sw or C_cpu[node] >= required_cpu:
            for edge in G[node]:
                key = get_key(node,edge);
                if C_bw[key]*r_bw[key] >= required_bw:
                    if node not in G_new:
                        G_new[node] = [edge]
                    else:
                        G_new[node].append(edge)
                        if(edge not in G_new):
                            G_new[edge] = []


    max_cpu = get_max_cpu()
    max_bw = get_max_bw()
    v_bw = {}
    v_cpu = {}

    for edge in C_bw:
        if fbw[index] > threshold_bw:
            deno = (r_bw[edge]*C_bw[edge] - fbw[index])
            if(deno!=0):
               v_bw[edge] = max_bw[1]/(r_bw[edge]*C_bw[edge] - fbw[index])
            else:
               v_bw[edge] =  10000000
        else:
            v_bw[edge] = 0

    for node in C_cpu:
        if fcpu[index] > threshold_cpu:
            deno = (r_cpu[node]*C_cpu[node] - fcpu[index])
            if(deno!=0):
                v_cpu[node] = max_cpu[1]/(r_cpu[node]*C_cpu[node] - fcpu[index])
            else:
                v_cpu[node] = 10000000
        else:
            v_cpu[node] = 0

    output_LFG, LFG_cost,last_column = construct_LFG(G_new, v_bw, v_cpu, index)
    if (output_LFG is None):
        return "Routing Failed", False
    print("output_LFG: ")
    print(output_LFG)
    src = str(flows[index][0])+"_"+"0"
    dst = str(flows[index][len(flows[index])-1])+"_"+str(last_column)
    output_bars = dijkstra(output_LFG, src, dst,LFG_cost,K)
    k = -1
    K = min(K,len(output_bars))
    while(k<K-1):
        k = k + 1
        print("Bar Path")
        print(output_bars[k])
        remembering_paths = {}
        if(output_bars[k] is not None):
            routing_path = []
            no_path_found = False
            for i in range(0,len(output_bars[k])-1):
                start = output_bars[k][i].split("_")[0]
                end = output_bars[k][i+1].split("_")[0]
                path = bfs_shortest_path(G_new,int(start),int(end))
                key = str(start)+"-"+str(end)
                remembering_paths[key] = path
                if path is None:
                    no_path_found = True
                    break;
                if not routing_path:
                   routing_path.extend(path)
                else:
                   routing_path.extend(path[1:])

            if(no_path_found):
                continue;

            constraints=True
            ## Check Equation 9:
            for edge in C_bw:
                start_edge_node = edge.split("-")[0]
                end_edge_node = edge.split("-")[1]
                sum = 0
                for i in range(0, len(output_bars[k]) - 1):
                    start = output_bars[k][i].split("_")[0]
                    end = output_bars[k][i + 1].split("_")[0]
                    key = str(start) + "-" + str(end)
                    possible_path = remembering_paths[key]
                    count = check_if_in_path(possible_path,int(start_edge_node),int(end_edge_node))
                    sum = sum+fbw[index]*count

                if(sum>r_bw[edge]*C_bw[edge]):
                    constraints=False
                    break;

            if(constraints==False):
                continue

            ##check Equation 10:
            #Follow Table not checking for the time being


            ##check Equation 11:
            for node in V_fn:
                sum = 0
                for i in range(0,len(output_bars[k])):
                    start_edge_node = output_bars[k][i].split("_")[0]
                    if(node==start_edge_node):
                        sum = sum + fcpu[node]

                if(sum>C_cpu[node]*r_cpu[node]):
                    constraints=False


            if (constraints == False):
                continue

            ## Equation 12:
            # it is about delay which we are not comparing

            ## Equation 13-17:
            # As the equation puts contraints on z variables, we are not using them hence not requried.

            for i in range(0,len(routing_path)-1):
                start = routing_path[i]
                end = routing_path[i+1]
                if(start==end):
                    continue
                key = get_key(start,end)
                remaing = C_bw[key]*r_bw[key]-fbw[index]
                r_bw[key] = remaing/C_bw[key]
                if(r_bw[key]<0):
                    print("Alert")

            for i in range(0,len(routing_path)):
                node = routing_path[i]
                if(node in V_fn):
                    remaing = C_cpu[node]*r_cpu[node]-fcpu[index]
                    r_cpu[node] = remaing/C_cpu[node]

            return routing_path,True
        else:
            return "Routing Failed",False

    return "Routing Failed",False

    #     print('phi')
    #     print(output)
    #     k = k + 1



def check_if_in_path(possible_path,start_edge,end_edge):
    count = 0
    for i in range(0,len(possible_path)-1):
        if( (possible_path[i]==start_edge and possible_path[i+1]==end_edge) or (possible_path[i]==end_edge and possible_path[i+1]==start_edge) ):
            count = count+1
    return count



if __name__ == '__main__':
    flows, mbox_types, nw_graph,top_mbox = get_network_values()
    rls, gre, ce, fl, pm, qrm, fl_e,fl_pm = generate_data()
    r_bw = {}
    r_cpu = {}
    G = nw_graph
    M = mbox_types
    V_fn = top_mbox
    V_sw = [x for x in list(nw_graph) if x not in V_fn]
    fbw = fl_e
    #generate_fbw()
    fcpu = fl_pm
    #generate_fcpu()
    C_bw= ce
    #generate_Cbw()
    C_cpu = pm
    #generate_Ccpu()

    initialize_rbw()
    initialize_rcpu()
    K = 100
    throughput = 0

    threshold_bw = 2
    threshold_cpu = 2

    for i in range(len(flows)):
        print("For Index i: "+str(i+1))
        result,passed = RA_RA(i, flows[i], K)
        if(passed):
            throughput = throughput+fbw[i]
        print(result)
        print(r_bw)
        print(r_cpu)
        print("\n\n")

    sum = 0
    for i in range(len(fl_e)):
        sum = sum +fl_e[i]
    print("Total_throughtput Possible: "+ str(sum))
    print("Total_throughput: "+ str(throughput))

