import re


def number_of_lines(filepath):
    line_number = None
    with open(filepath) as f:
        for line_number, line in enumerate(f):
            pass
    return line_number + 1


def convert_number_to_image_file_name(number):
    return '%06d.jpg' % number


def all_frames_filespath(folder_directory, number_of_frames):
    """

    :param folder_directory:
    :param number_of_frames:
    :return:
    :rtype: [str]
    """
    filepaths = [None]*(number_of_frames + 1)

    for frame_number in range(number_of_frames+1):
        filepaths[frame_number] = '%s\%s' % (folder_directory, convert_number_to_image_file_name(frame_number))

    return filepaths


def image_coords_paths(filepath):
    """

    :param filepath:
    :return:
    :rtype: [[int]]
    """
    return coords_paths(filepath, number_of_lines(filepath))


def split_frame_coord_str(frame_coord_str):
    """
    Split a string by white spaces, parentheses, commas and '\n'

    :param frame_coord_str:
    :return:
    :rtype: [int]
    """
    return [int(frame_coord) for frame_coord in re.split(r'[(,)]', frame_coord_str) if frame_coord != '' and frame_coord != '\n']


def world_coords_paths(filepath):
    return coords_paths(filepath, number_of_lines(filepath)-1, ignore_first_row=True)


def coords_paths(filepath, paths_length, ignore_first_row=False):
    paths = [None]*paths_length

    with open(filepath) as f:
        for line_number, line in enumerate(f):
            if ignore_first_row:
                if line_number == 0:    # if it's the first row
                    continue    # then ignore it
                paths[line_number-1] = split_frame_coord_str(line)  # if it's not, start adding coordinates from index 0
            else:
                paths[line_number] = split_frame_coord_str(line)

    return paths
