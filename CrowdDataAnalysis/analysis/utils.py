from analysis.frame_coord import FrameCoord
from analysis.frame_coord_list import FrameCoordList
from analysis.person_path import PersonPath


def create_people_paths(image_coords_paths):
    """

    :param image_coords_paths:
    :type image_coords_paths: [[int]]
    :return:
    :rtype: [PersonPath]
    """
    people_paths = [None]*len(image_coords_paths)

    index = 0
    for coords_path in image_coords_paths:
        person_path = create_person(coords_path)
        people_paths[index] = person_path
        index += 1

    return people_paths


def create_person(coords_path):
    """

    :param coords_path:
    :type coords_path: [int]
    :return:
    :rtype: PersonPath
    """
    id_number = coords_path[0]
    fr_coordinates = [None]*((len(coords_path)-1)/3)  # excluding the index 0 (which is the id) the number of triples is the length of this array

    index = 0
    for i in range(1, len(coords_path), 3):
        x = coords_path[i]
        y = coords_path[i+1]
        frame_number = coords_path[i+2]
        fr_coordinates[index] = FrameCoord(x, y, frame_number)
        index += 1

    return PersonPath(id_number, FrameCoordList(fr_coordinates))
