from collections import deque


def detect_group(people_graph, everyone_in_frame, grouping_max_distance):
    """

    :param people_graph:
    :type people_graph: Graph
    :param everyone_in_frame:   [PersonPath]
    :type everyone_in_frame: list
    :param grouping_max_distance:
    :return:
    """
    groups = deque()

    ids_in_frame = [person_path.id_number for person_path in everyone_in_frame]
    nodes_in_frame = [node for node in people_graph.get_nodes() if node.item in ids_in_frame]

    for node in nodes_in_frame:
        if not does_belong_to_any_group(node, groups):
            group = perform_group(node, grouping_max_distance)
            groups.append(group)

    return groups


def does_belong_to_any_group(node, groups):
    for group in groups:
        if node in group:
            return True

    return False


def perform_group(node, grouping_max_distance, group=None):
    g = deque([edge.target for edge in node.get_edges() if edge.weight <= grouping_max_distance])
    g.append(node)

    if group is None:   # the base case: if this is the first call of this function
        group = g
        for n in list(group):     # for every person nearby
            group = perform_group(n, grouping_max_distance, group)
    else:   # if there is already a group
        for n in g:  # for every person nearby
            if n not in group:   # if this person is not already in the group
                group.append(n)  # add this person

    return group
