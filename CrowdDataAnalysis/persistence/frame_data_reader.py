import re


def number_of_lines(filepath):
    line_number = None
    with open(filepath) as f:
        for line_number, line in enumerate(f):
            pass
    return line_number + 1


def convert_number_to_image_file_name(number):
    return '%06d.jpg' % number


def create_all_filepaths(folder_directory, number_of_images):
    """

    :param folder_directory:
    :param number_of_images:
    :return:
    :rtype: [str]
    """
    filepaths = [None]*(number_of_images+1)

    for frame_number in range(number_of_images+1):
        filepaths[frame_number] = '%s\%s' % (folder_directory, convert_number_to_image_file_name(frame_number))

    return filepaths


def image_coords_paths(filepath):
    """

    :param filepath:
    :return:
    :rtype: [[int]]
    """
    paths = [None]*(number_of_lines(filepath))

    with open(filepath) as f:
        for line_number, line in enumerate(f):
            paths[line_number] = split_frame_coord_str(line)

    return paths


def split_frame_coord_str(frame_coord_str):
    """
    Split a string by white spaces, parentheses, commas and '\n'

    :param frame_coord_str:
    :return:
    :rtype: [int]
    """
    return [int(frame_coord) for frame_coord in re.split(r'[(,)]', frame_coord_str) if frame_coord != '' and frame_coord != '\n']
