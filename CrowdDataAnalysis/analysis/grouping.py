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


def find_group_that_it_belongs(node, groups):
    for group in groups:
        if node in group:
            return group

    return None


def does_belong_to_any_group(node, groups):
    return True if find_group_that_it_belongs(node, groups) is not None else False


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


def differences_between_groups(group_a, group_b):
    people_not_in_group_b = deque()
    people_not_in_group_a = deque()

    for node in group_a:
        if not (node in group_b):
            people_not_in_group_b.append(node)

    for node in group_b:
        if not (node in group_a):
            people_not_in_group_a.append(node)

    return people_not_in_group_b, people_not_in_group_a


def are_groups_the_same(group_a, group_b):
    if len(group_a) != len(group_b):
        return False

    people_not_in_group_b, people_not_in_group_a = differences_between_groups(group_a, group_b)

    if people_not_in_group_b or people_not_in_group_a:  # if at least one of these lists is not empty
        return False

    return True


def compare_groups(previous_groups, current_groups):
    for current_group in current_groups:    # for each group in the current groups list
        for node in current_group:  # for each person in this group
            foo(node, previous_groups, current_group)
            break


def foo(node, previous_groups, current_group):
    previous_group_where_it_belongs = find_group_that_it_belongs(node, previous_groups)  # find the group where this person belongs in the previous groups list

    if previous_group_where_it_belongs is None:  # if this person never was in a group before
        if len(current_group) == 1:
            print('Group created: ', [n.item for n in current_group])
        else:
            print('Group updated: ', [n.item for n in current_group])   # when someone who wasn't in a group before and now joined a group
    else:  # if this person was in a group before
        people_not_in_group_b, people_not_in_group_a = differences_between_groups(previous_group_where_it_belongs, current_group)

        # if there is anything bifferent between these groups where this person belongs
        if people_not_in_group_b:
            print([person.item for person in people_not_in_group_b], "left %d's group:" % node.item, [n.item for n in current_group])
        if people_not_in_group_a:
            print([person.item for person in people_not_in_group_a], "joined %d's group:" % node.item, [n.item for n in current_group])

        return True

    return False
