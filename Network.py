
from random import seed
from random import randint
import pandas as pd

def get_key(a, b):
    min_number = min(a,b)
    max_number = max(a,b)
    return str(min_number)+'-'+str(max_number)

seed(1)
# nw_graph = {
#     1: [2, 3, 7],
#     2: [1, 4, 5],
#     3: [1, 5],
#     4: [2, 6, 8],
#     5: [2, 3, 6, 9],
#     6: [4, 5],
#
#     7: [1],
#     8: [4],
#     9: [5]
# }
#
# mbox_types = {
#     "p": [7, 8],
#     "f": [9]
# }
#
# top_mbox = [7, 8, 9]
#
# # Flows
# flows = [
#     [1, "p", "f", "p", "f", "p", "f", "p", 3],
#     # [1, "p", 2],
#     # [2, "f", 6],
#     # [1, "f", "p", 5],
#     # [4, "f", 4]
# ]



def get_opp_key(key):
    keys = key.split("-")
    new_key = keys[1]+"-"+keys[0]
    return new_key


def generate_flows(num_flows, node_start, node_end, mbox_types,how_many_to_keep):
    flows = []
    for i in range(0, num_flows):
        len_flow = randint(1, how_many_to_keep)
        flow = []
        flow.append(randint(node_start, node_end))
        for j in range(0, len_flow):
            flow.append(list(mbox_types)[randint(0, len(mbox_types)-1)])
        flow.append(randint(node_start, node_end))
        flows.append(flow)
    return flows

def fat_tree_generator():
    k = 8

    nw_graph = {}
    # Generate core switches
    core_switches = int(k / 2) ** 2
    aggregation_switches = int((k ** 2) / 2)
    edge_switches = int((k ** 2) / 2)
    servers = int((k ** 3) / 4)
    ce = {}
    pm = {}

    num_mbox = 24
    num_mbox_types = 8  # With num_box/mbox_types instances of each mbox type
    mbox_types = {}
    top_mbox = []

    aggregation_stop_index = core_switches + aggregation_switches
    edge_stop_index = core_switches + aggregation_switches + edge_switches
    server_stop_index = core_switches + aggregation_switches + edge_switches + servers
    mbox_stop_index = server_stop_index + num_mbox

    # First layer
    for i in range(1, core_switches + 1):
        nw_graph[i] = []

    num_pods = k

    # Second layer
    for i in range(core_switches + 1, aggregation_stop_index + 1):
        nw_graph[i] = []

    # Third layer
    for i in range(aggregation_stop_index + 1, edge_stop_index + 1):
        nw_graph[i] = []

    # fourth Layer
    for i in range(edge_stop_index + 1, server_stop_index + 1):
        nw_graph[i] = []

    # Connecting first two layers
    for i in range(1, core_switches + 1):
        aggregation_start = core_switches + int((i - 1) / int(k / 2)) + 1
        for j in range(0, num_pods):
            key = int(aggregation_start + (k / 2) * j)
            nw_graph[i].append(key)
            nw_graph[key].append(i)
            ce[get_key(i, key)] = first_second_layer_bw

    # Connecting Aggregation and Edge switches
    agg_start = core_switches + 1
    edge_start = aggregation_stop_index + 1

    pod_size = int(k / 2)

    ## Joining second and third layer
    for current_pod in range(0, num_pods):
        curr_agg_start = agg_start + pod_size * current_pod
        curr_edge_start = edge_start + pod_size * current_pod
        for i in range(curr_agg_start, curr_agg_start + pod_size):
            for j in range(curr_edge_start, curr_edge_start + pod_size):
                nw_graph[i].append(j)
                nw_graph[j].append(i)
                ce[get_key(i, j)] = second_third_layer_bw


    ### Joining third and fourth layers
    curr_server = edge_stop_index
    for i in range(aggregation_stop_index + 1, edge_stop_index + 1):
        for j in range(0, int(k / 2)):
            curr_server = curr_server + 1
            nw_graph[i].append(curr_server)
            nw_graph[curr_server].append(i)
            ce[get_key(i, curr_server)] = third_fourth_layer_bw



    ## Joining Middle Boxes
    for i in range(server_stop_index + 1, mbox_stop_index + 1):
        nw_graph[i] = []
        connected_host = randint(1, edge_stop_index)
        nw_graph[i].append(connected_host)
        nw_graph[connected_host].append(i)
        top_mbox.append(i)
        pm[i] = 300
        ce[get_key(i, connected_host)] = m_boxes_bw



    # Generating middle boxes
    mbox_curr = server_stop_index
    start_char_Mbox = ord('a')
    for m in range(0, num_mbox_types):
        jump = int(num_mbox / num_mbox_types)
        for t in range(0, jump):
            mbox_curr = mbox_curr + 1
            if (chr(start_char_Mbox) not in mbox_types):
                mbox_types[chr(start_char_Mbox)] = []
            mbox_types[chr(start_char_Mbox)].append(mbox_curr)
        start_char_Mbox = start_char_Mbox + 1

    flows = generate_flows(200, 81, 208, mbox_types,6)

    #print(flows)

    # flows = [
    #     [90, "a", "b", 189],
    #     [81, "c", 173],
    #     [207, "d", 150],
    #     [100, "e", "f", 120],
    #     [102, "g", 113]
    # ]

    print("Generating fat tree\n")
    print(mbox_types)
    print(nw_graph)
    print(top_mbox)

    print("\nGenerated fat tree\n")
    print("Flows: "+str(flows))

    return nw_graph, mbox_types, top_mbox, flows, ce, pm


def coronet_gen():
    cities = {}
    conus_frame = pd.read_csv('conus.csv', header=None)
    count = 1
    for index, row in conus_frame.iterrows():
        cityname1 = row[0]
        cityname2 = row[1]
        if(cityname1 not in cities):
            cities[cityname1]  = count
            count = count+1
        if(cityname2 not in cities):
            cities[cityname2] = count
            count = count+1

    nw_graph = {}
    ce = {}
    for city in cities:
        nw_graph[cities[city]] = []

    for index, row in conus_frame.iterrows():
        cityname1 = row[0]
        cityname2 = row[1]
        node1 = cities[cityname1]
        node2 = cities[cityname2]
        nw_graph[node1].append(node2)
        nw_graph[node2].append(node1)
        key = get_key(node1,node2)
        ce[key] = bandwidth_power_coronet


    num_mbox_types = 20  # With num_box/mbox_types instances of each mbox type
    mbox_types = {}
    start_char_Mbox = ord('a')

    for m in range(0, num_mbox_types):
        mbox_types[chr(start_char_Mbox)] = []
        start_char_Mbox = start_char_Mbox + 1
    print(mbox_types)
    num_mbox = 18
    number_of_vf_deployed = 8
    sorted_graph = sorted(nw_graph.items(), key=lambda s: len(s[1]), reverse=True)
    print(sorted_graph)
    start_char_Mbox = ord('a')

    top_mbox = []
    pm = {}
    for i in range(0,num_mbox):
        node = sorted_graph[i][0]
        top_mbox.append(node)
        pm[node] = 1000
        checking = {}
        for j in range(0,number_of_vf_deployed):
            while True:
                type = randint(0,num_mbox_types-1)
                if type in checking:
                    continue
                mbox_types[chr(start_char_Mbox+type)].append(node)
                checking[type] = 0
                break
    print(mbox_types)
    flows = generate_flows(1000,1,len(nw_graph), mbox_types,3)

    return nw_graph, mbox_types, top_mbox, flows, ce, pm


# first_second_layer_bw = 200
# second_third_layer_bw = 100
# third_fourth_layer_bw = 100
# m_boxes_bw = 200
# nw_graph, mbox_types, top_mbox, flows, ce, pm = fat_tree_generator()

bandwidth_power_coronet = 1000
nw_graph, mbox_types, top_mbox, flows, ce, pm = coronet_gen()



