from genepro.node import Node
from genepro.node_impl import Feature, Constant, Times

import sys
sys.setrecursionlimit(3000)

from genepro.node import Node
from genepro.node_impl import Feature, Constant, Times

def traverse_and_invert_iter(node: Node, feature_ids: list[int]):
    stack = [node]

    while stack:
        current_node = stack.pop()

        if current_node.arity == 0:
            if isinstance(current_node, Feature) and current_node.id in feature_ids:
                new_node = Times()
                child_node = Feature(current_node.id)
                inverse_node = Constant(-1)
                new_node.insert_child(child_node)
                new_node.insert_child(inverse_node)

                parent_node = current_node.parent
                parent_node.detach_child(current_node)
                parent_node.insert_child(new_node)
        else:
            stack.extend(current_node._children)


def traverse_and_invert(node: Node, feature_ids: list[int]):
    """
    Traverse the tree rooted at 'node' and replace feature leaf nodes with the target feature_id with their inverse.

    Parameters
    ----------
    node : Node
        The root node of the tree to traverse.
    feature_id : list[int]
        The features to replace.
    """
    if node.arity == 0:
        # see if the node is a feature
        if isinstance(node, Feature) and node.id in feature_ids:
            # Replace the leaf node with the inverse
            new_node = Times()

            child_node = Feature(node.id)

            inverse_node = Constant(-1)
            
            new_node.insert_child(child_node)
            new_node.insert_child(inverse_node)

            parent_node = node.parent
            parent_node.detach_child(node)
            parent_node.insert_child(new_node)
    else:
        for child in node._children:
            traverse_and_invert(child, feature_ids)
