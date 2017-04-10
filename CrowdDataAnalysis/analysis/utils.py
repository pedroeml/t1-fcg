from analysis.frame_coord import FrameCoord
from analysis.frame_coord_list import FrameCoordList
from analysis.people_paths import PeoplePaths
from analysis.person_path import PersonPath
from graph.graph import Graph


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
