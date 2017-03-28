from analysis.frame_coord import FrameCoord
from analysis.frame_coord_list import FrameCoordList
from analysis.person_path import PersonPath
from analysis.people_paths import PeoplePaths


def create_people_paths(image_coords_paths, world_coords_paths):
    """

    :param image_coords_paths:
    :type image_coords_paths: [[int]]
    :param world_coords_paths
    :type world_coords_paths: [[int]]
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
        people_paths[index] = person_path

    return PeoplePaths(people_paths)


def create_person(image_coords_path, world_coords_path):
    """

    :param image_coords_path:
    :type image_coords_path: [int]
    :param world_coords_path:
    :type world_coords_path: [int]
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
    
    :param coords_path: 
    :type coords_path: [int]
    :return: 
    :rtype: int, [int]
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
