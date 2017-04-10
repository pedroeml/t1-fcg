import cv2 as cv
from collections import deque
from analysis import utils


def display(frame_filepath, world_background, everyone_in_frame, people_graph, too_far_distance, minimum_distance_change, grouping_max_distance, colors, world_min_x, world_min_y, time_per_frame):
    im = cv.imread(frame_filepath, 1)
    try:
        width, height, _ = im.shape
    except AttributeError as atterr:
        print(atterr, 'on file %s' % frame_filepath)
        return None
    world = world_background.copy()
    w = int(width * 0.05)
    h = int(height * 0.08)

    people_graph = utils.calc_distances_for_everyon_in_frame(everyone_in_frame, people_graph, too_far_distance, minimum_distance_change)
    groups = utils.detect_group(people_graph, everyone_in_frame, grouping_max_distance)

    groups_colors = deque(colors)
    for group in groups:
        color = groups_colors.pop()
        for node in group:
            person_path = [person_path for person_path in everyone_in_frame if person_path.id_number == node.item]

            if person_path:
                person_path = person_path[0]

                x, y = person_path.image_frame_coordinates_list.current_frame_coord_xy()

                min_x = x - int(w / 2)
                min_y = y - int(h / 2)

                person_path.image_frame_coordinates_list.next_frame_coord()

                cv.rectangle(im, (min_x, min_y), (min_x + w, min_y + h), color, 2)
                cv.putText(im, str(person_path.id_number), (min_x, min_y), 0, 1, (0, 0, 0), 2)

                x, y = person_path.world_frame_coordinates_list.current_frame_coord_xy()
                min_x = x - world_min_x
                min_y = y - world_min_y

                person_path.world_frame_coordinates_list.next_frame_coord()
                cv.rectangle(world_background, (min_x, min_y), (min_x + 2, min_y + 2), (0, 0, 0), 4)
                cv.rectangle(world, (min_x, min_y), (min_x + w, min_y + w), color, 2)
                cv.putText(world, str(person_path.id_number), (min_x, min_y), 0, 1, (0, 0, 0), 2)

    cv.imshow('im', im)
    cv.imshow('world', world)
    cv.waitKey(time_per_frame)
