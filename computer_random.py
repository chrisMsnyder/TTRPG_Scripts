import numpy as np
import random
import argparse

def print_arch(arch):
    print()
    for i in range(arch.shape[0]):
        line = ''
        for j in range(arch.shape[1]):
            line += arch[i][j]
        print(' '.join(line))

    print()
    print("$ = Entry Point/Starting Node")
    print('O = Empty Node')
    print("F = Node with 'Firewall' Countermeasure")
    print("W = Node with 'Wipe' Countermeasure")
    print("A = Node with 'Alarm' Countermeasure")
    print("S = Node with 'Shock Grid' Countermeasure")
    print("L = Node with 'Lockout' Countermeasure")
    print("H = Node with 'Honeypot' Countermeasure")
    print("D = Data Access Node")
    print("C = Control Access Node")
    print("P = Ping Access Node")
    print()

def get_available_nodes(arch, node, filled_nodes):
    new_nodes = [(node[0]-1, node[1]),
                 (node[0], node[1]-1),
                 (node[0], node[1]+1),
                 (node[0]+1, node[1])]
    bad_coords = []
    for n in new_nodes:
        if n[0] < 0 or n[0] >= arch.shape[0] or n[1] < 0 or n[1] >= arch.shape[1]:
            bad_coords.append(n)
        elif n in filled_nodes:
            bad_coords.append(n)
    
    for coord in bad_coords:
        new_nodes.remove(coord)

    return new_nodes


def set_node(arch, n, val):
    arch[n[0]][n[1]] = val


def get_weights(complexity):
    node_weights = {
        'O': complexity, 
        'F': 1, 
        'L': 1, 
        'W': 1, 
        'A': 1, 
        'S': 1, 
        'H': 0.1 * complexity, 
        'P': 0.1 * complexity
    }
    node_odds = np.array(list(node_weights.values()))
    node_odds = np.array(node_odds / min(node_odds))
    node_odds = node_odds / sum(node_odds)
    return dict(zip(list(node_weights.keys()), node_odds))




def main(args):
    weighted_nodes = get_weights(args.complexity)
    arch = np.full((11,11), '-')
    nodes = []
    for n in range(int(args.complexity*args.tier)):
        node = random.choices(list(weighted_nodes.keys()), weights=list(weighted_nodes.values()), k=1)[0]
        nodes.append(node)
    access_nodes = ['D', 'C']
    filled_nodes = [(5, 5)]
    arch[5][5] = '$'
    avail = [(4, 5), (5, 4), (5, 6), (6, 5)]
    while len(nodes) > 0 and len(avail) > 0:
        type_index = random.randint(0, len(nodes)-1)
        chosen_type = nodes[type_index]
        avail_index = random.randint(0, len(avail)-1)
        chosen_avail = avail[avail_index]
        set_node(arch, chosen_avail, chosen_type)
        nodes.pop(type_index)
        avail.pop(avail_index)
        filled_nodes.append(chosen_avail)
        new_nodes = get_available_nodes(arch, chosen_avail, filled_nodes)
        avail = list(set(avail + new_nodes))
    
    start_adjacent = [(4, 5), (5, 4), (5, 6), (6, 5)]
    avail = [x for x in avail if x not in start_adjacent]
    
    for node in access_nodes:
        avail_index = random.randint(0, len(avail)-1)
        chosen_avail = avail[avail_index]
        set_node(arch, chosen_avail, node)
        avail.pop(avail_index)
        filled_nodes.append(chosen_avail)


    print_arch(arch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tier', default=1, type=int)
    parser.add_argument('--complexity', default=2, type=float)
    args = parser.parse_args()
    main(args)


