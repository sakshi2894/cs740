num_nodes = 6


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

    # in case there's no path between the 2 nodes
    #return "So sorry, but a connecting path doesn't exis


def generate_edges(src, dest):
    #print("src: %d, dest: %d" % (src, dest))
    path = bfs_shortest_path(nw_graph, src, dest)
    #print("path: ", path)
    return path


# Generate Gre
def generate_gre():
    for i in range(0, len(rls)):
        edges = []
        gre.append([])
        for j in range(0, len(rls[i])):
            for k in range(0, len(rls[i][j]) - 1):
                edges = edges + generate_edges(rls[i][j][k], rls[i][j][k + 1])

            print(edges)
            for j in range(0, len(edges) - 1):
                edge = str(edges[j]) + "-" + str(edges[j + 1])
                gre[len(gre) - 1].append({edge: 5})

            print(gre[len(gre) - 1])

def main():
    generate_rls()
    print(rls)
    generate_gre()
    #print(gre)



main()