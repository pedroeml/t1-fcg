from collections import deque
import numpy as np
from analysis.frame_coord import FrameCoord
from analysis.frame_coord_list import FrameCoordList
from analysis.people_paths import PeoplePaths
from analysis.person_path import PersonPath
from graph.graph import Graph
from analysis.distance_event import DistanceEvent


def create_people_paths(image_coords_paths, world_coords_paths):
    """

    :param image_coords_paths: [[int]]
    :type image_coords_paths: list
    :param world_coords_paths: [[int]]
    :type world_coords_paths: list
    :return:
    :rtype: PeoplePaths
    """
    if len(image_coords_paths) != len(world_coords_paths):
        raise Exception('len(image_coords_paths) != len(world_coords_paths): %d != %d' % (len(image_coords_paths), len(world_coords_paths)))

    people_paths = [None]*len(image_coords_paths)

    for index in range(len(image_coords_paths)):
        i_coords_path = image_coords_paths[index]
        w_coords_path = world_coords_paths[index]
        person_path = create_person(i_coords_path, w_coords_path)

        if index != 0:
            while does_id_already_exists(person_path.id_number, people_paths):
                person_path.id_number += 1

        people_paths[index] = person_path

    return PeoplePaths(people_paths)


def does_id_already_exists(id_number, people_paths):
    id_number_list = [person_path.id_number for person_path in people_paths if person_path is not None]
    return id_number in id_number_list


def create_person(image_coords_path, world_coords_path):
    """

    :param image_coords_path: [int]
    :type image_coords_path: list
    :param world_coords_path: [int]
    :type world_coords_path: list
    :return:
    :rtype: PersonPath
    """
    id_number_i, image_coords = create_frame_coords_list(image_coords_path)
    id_number_w, world_coords = create_frame_coords_list(world_coords_path)

    if id_number_i != id_number_w:
        raise Exception('id_number_i != id_number_w: %d != %d' % (id_number_i, id_number_w))

    return PersonPath(id_number_i, FrameCoordList(image_coords), FrameCoordList(world_coords))


def create_frame_coords_list(coords_path):
    """
    
    :param coords_path: [int]
    :type coords_path: list
    :return: int, [int]
    :rtype: tuple
    """
    id_number = coords_path[0]
    fr_coordinates = [None]*int((len(coords_path) - 1) / 3)  # excluding the index 0 (which is the id) the number of triples is the length of this array

    index = 0
    for i in range(1, len(coords_path), 3):
        x = coords_path[i]
        y = coords_path[i + 1]
        frame_number = coords_path[i + 2]
        fr_coordinates[index] = FrameCoord(x, y, frame_number)
        index += 1

    return id_number, fr_coordinates


def calc_world_dimensions(people_paths):
    world_min_x = people_paths.people_paths[0].world_frame_coordinates_list.frame_coords[0].x
    world_max_x = world_min_x
    world_min_y = people_paths.people_paths[0].world_frame_coordinates_list.frame_coords[0].y
    world_max_y = world_min_y

    for person_path in people_paths.people_paths:
        for frame_coord in person_path.world_frame_coordinates_list.frame_coords:
            world_min_x = frame_coord.x if frame_coord.x < world_min_x else world_min_x
            world_max_x = frame_coord.x if frame_coord.x > world_max_x else world_max_x
            world_min_y = frame_coord.y if frame_coord.y < world_min_y else world_min_y
            world_max_y = frame_coord.y if frame_coord.y > world_max_y else world_max_y

    world_width = world_max_x - world_min_x
    world_height = world_max_y - world_min_y

    return world_min_x, world_min_y, world_max_x, world_max_y, world_width, world_height


def create_graph(people_paths):
    """
    
    :param people_paths: 
    :type people_paths: PeoplePaths
    :return: 
    :rtype: Graph
    """
    people_graph = Graph()

    for person_path in people_paths.people_paths:
        people_graph.add_node(person_path.id_number)

    return people_graph


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

        for i in range(len(ids)):
            id_number = ids[i]

            if id_number == person_path.id_number:  # if it's the same id as the person_path's id
                continue

            distance = all_euclidean_distances[i]
            people_graph.add_edge(person_path.id_number, id_number, distance)

            if distance < too_far_distance:  # if it's not too far
                distance_event(person_path.id_number, id_number, people_graph, minimum_distance_change)

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
    except IndexError:
        return None
    else:
        if abs(edge.weight - previous_weight) > minimum_distance_change:    # ignoring little distance changes
            if edge.weight < previous_weight:   # if it's getting closer
                if not (previous_weight < before_previous_weight):  # if before it was getting further: it means the event has changed
                    print('%3d is getting CLOSER  to   %3d: %03.4f < %03.4f' % (id_number_a, id_number_b, edge.weight, previous_weight))
                return DistanceEvent.CLOSER
            elif edge.weight > previous_weight:     # if it's getting further
                if not (previous_weight > before_previous_weight):  # if before it was getting closer: it means the event has changed
                    print('%3d is getting FURTHER from %3d: %03.4f > %03.4f' % (id_number_a, id_number_b, edge.weight, previous_weight))
                return DistanceEvent.FURTHER
    return None


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
