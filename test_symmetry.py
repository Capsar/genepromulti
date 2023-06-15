from genepro.thruster_symmetry import traverse_and_invert, traverse_and_invert_iter
from genepro.node import Node
from genepro.node_impl import *
from genepro.variation import generate_random_tree
from genepro.ascii_tree import generate_vertical_ascii_tree
from copy import deepcopy

import sys
sys.setrecursionlimit(1500)



def test_traverse_and_invert():
    num_features = 8
    internal_nodes=[Plus(),Minus(),Times(),Div(), Square(), Cube(), Sqrt()]
    features = [Feature(i) for i in range(num_features)]

    base_tree = generate_random_tree(
            internal_nodes=internal_nodes,
            leaf_nodes = features + [Constant()],
            max_depth=5) 


    # Create a copy of the base tree
    copied_tree = deepcopy(base_tree)
    
    # Invert the tree
    inverted_tree = traverse_and_invert_iter(copied_tree, [0,2,4,5,6,7])



    return base_tree, inverted_tree


if __name__ == '__main__':
    base_tree, inverted_tree = test_traverse_and_invert()
    print('Base tree:')
    print(base_tree)
    print(generate_vertical_ascii_tree(base_tree))

    print('Inverted tree:')
    print(inverted_tree)
    print(generate_vertical_ascii_tree(inverted_tree))
    
    


