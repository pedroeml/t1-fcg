from persistence import frame_data_reader
from analysis import utils
import numpy as np
from const import *
import visualization.utils
from visualization import display_frame
from analysis import distancing
from analysis import grouping


# Some directories doesn't have %06d.jpg file name format! In this case, try %04.jpg

if FPS > 0:
    time_per_frame = int(1000/FPS)   # 24 fps = 1000 ms/24 frames = 41,666 ms
else:
    time_per_frame = 0

number_of_frames = frame_data_reader.number_of_lines(INPUT_FOLDER_PATH + '\imageList.txt')
all_frames_filespath = frame_data_reader.all_frames_filespath(INPUT_FOLDER_PATH, number_of_frames)
image_coords_paths = frame_data_reader.image_coords_paths(INPUT_FOLDER_PATH + '\Paths_N.txt')
world_coords_paths = frame_data_reader.world_coords_paths(INPUT_FOLDER_PATH + '\Paths_D.txt')
people_paths = utils.create_people_paths(image_coords_paths, world_coords_paths)

world_min_x, world_min_y, world_max_x, world_max_y, world_width, world_height = utils.calc_world_dimensions(people_paths)
print('%dx%d' % (world_width, world_height))

people_graph = utils.create_graph(people_paths)

world_background = np.ones((world_height, world_width, 3), np.uint8)*175

colors = visualization.utils.generate_colors()

# TODO: Comparar grupos entre frames para verificar o evento split

previous_groups = None
frame_number = 0
for frame_filepath in all_frames_filespath:
    everyone_in_frame = people_paths.everyone_in_frame(frame_number)
    people_graph = distancing.calc_distances_for_everyon_in_frame(everyone_in_frame, people_graph, TOO_FAR_DISTANCE, MINIMUM_DISTANCE_CHANGE)
    groups = grouping.detect_group(people_graph, everyone_in_frame, GROUPING_MAX_DISTANCE)
    if previous_groups is not None:
        grouping.compare_groups(previous_groups, groups)
        previous_groups = groups
    else:
        previous_groups = groups
    display_frame.display(frame_filepath, world_background, everyone_in_frame, groups, colors, world_min_x, world_min_y, time_per_frame)
    frame_number += 1
