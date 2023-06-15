from genepro.node import Node
from genepro.node_impl import Feature, Constant, Times
from copy import deepcopy

from genepro.node import Node
from genepro.node_impl import Feature, Constant, Times

def traverse_and_invert_iter(tree: Node, feature_ids: list[int]):
    new_tree = deepcopy(tree)
    stack = [new_tree]

    while stack:
        n = stack.pop()

        if n.arity == 0:
            if isinstance(n, Feature) and n.id in feature_ids:
                new_node = deepcopy(Times())
                child_node = deepcopy(Feature(n.id))
                inverse_node = deepcopy(Constant())
                inverse_node.set_value(float(-1))
                new_node.insert_child(child_node)
                new_node.insert_child(inverse_node)

                p = n.parent
                if p:
                    i = p.detach_child(n)
                    p.insert_child(new_node, i)
                else:
                    new_tree = new_node

        else:
            stack.extend(n._children)

    return new_tree



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
