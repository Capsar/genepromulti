from genepro.node import Node
def generate_vertical_ascii_tree(node: Node, indent: str = '', is_left: bool = None) -> str:
    """
    Generates a vertical ASCII tree representation of the subtree rooted at the given node.

    Parameters
    ----------
    node : Node
        The root node of the subtree.
    indent : str, optional
        The indentation string for the current level of the tree (default is '').
    is_left : bool, optional
        Indicates if the current node is a left child (default is None).

    Returns
    -------
    str
        Vertical ASCII tree representation of the subtree.
    """
    tree = ''

    if indent:
        tree += indent[:-2]
        if is_left:
            tree += '├─'
        else:
            tree += '└─'

    tree += str(node.symb) + '\n'

    if node._children:
        if is_left is None:
            next_indent = indent + '  '
        elif is_left:
            next_indent = indent + '|  '
        else:
            next_indent = indent + '   '

        children_count = len(node._children)
        for i, child in enumerate(node._children):
            if i == children_count - 1:
                tree += generate_vertical_ascii_tree(child, next_indent, False)
            else:
                tree += generate_vertical_ascii_tree(child, next_indent, True)

    return tree

