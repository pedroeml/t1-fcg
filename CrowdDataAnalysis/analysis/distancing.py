import numpy as np
from collections import deque
from analysis.distance_event import DistanceEvent


def calc_distances_for_everyon_in_frame(everyone_in_frame, people_graph, too_far_distance, minimum_distance_change):
    """
    
    :param everyone_in_frame: [PersonPath]
    :type everyone_in_frame: list
    :param people_graph: 
    :type people_graph: Graph
    :param too_far_distance:
    :param minimum_distance_change:
    :return: 
    :rtype: Graph
    """
    points = [[person_path.world_frame_coordinates_list.current_frame_coord().x, person_path.world_frame_coordinates_list.current_frame_coord().y] for person_path in everyone_in_frame]  # all points of everyone in this frame
    points = np.array(points)
    ids = [person_path.id_number for person_path in everyone_in_frame]

    for index, person_path in enumerate(everyone_in_frame):
        x, y = person_path.world_frame_coordinates_list.current_frame_coord_xy()
        point = np.array([x, y])

        all_euclidean_distances = np.linalg.norm(points - point, axis=1)  # calculate all euclidean distances

        closer = deque()
        further = deque()

        for i in range(len(ids)):
            id_number = ids[i]

            if id_number == person_path.id_number:  # if it's the same id as the person_path's id
                continue

            distance = all_euclidean_distances[i]
            people_graph.add_edge(person_path.id_number, id_number, distance)

            if distance < too_far_distance:  # if it's not too far
                event = distance_event(person_path.id_number, id_number, people_graph, minimum_distance_change)

                if event == DistanceEvent.CLOSER:
                    closer.append(id_number)
                elif event == DistanceEvent.FURTHER:
                    further.append(id_number)

        if closer:
            print('%3d is getting  CLOSER  to' % person_path.id_number, list(closer))
        if further:
            print('%3d is getting FURTHER from' % person_path.id_number, list(further))

    return people_graph


def distance_event(id_number_a, id_number_b, people_graph, minimum_distance_change):
    """
    
    :param id_number_a: 
    :param id_number_b: 
    :param people_graph: 
    :type people_graph: Graph
    :param minimum_distance_change:
    :return: 
    """
    node_a = people_graph.find_node(id_number_a)
    node_b = people_graph.find_node(id_number_b)
    edge = node_a.find_edge(node_b)

    try:
        previous_weight = edge.weight_history[-2]
        before_previous_weight = edge.weight_history[-3]
        before_than_before_previous_weight = edge.weight_history[-4]
    except IndexError:
        return None
    else:
        if abs(edge.weight - before_than_before_previous_weight) > minimum_distance_change:    # ignoring little distance changes
            if edge.weight < previous_weight:   # if it's getting closer
                if previous_weight < before_previous_weight and before_previous_weight < before_than_before_previous_weight:  # if it keeps getting closer
                    return DistanceEvent.CLOSER
            elif edge.weight > previous_weight:     # if it's getting further
                if previous_weight > before_previous_weight and before_previous_weight > before_than_before_previous_weight:  # if it keeps getting further
                    return DistanceEvent.FURTHER
    return None