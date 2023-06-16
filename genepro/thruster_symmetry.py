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
                new_node = Times()
                child_node = Feature(n.id)
                inverse_node = Constant()
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
