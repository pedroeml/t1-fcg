from collections import deque


class PeoplePaths:

    def __init__(self, people_paths):
        """

        :param people_paths: [PersonPath]
        :type people_paths: list
        """
        self.people_paths = people_paths

    def everyone_in_frame(self, frame_number):
        """

        :param frame_number:
        :return: [PersonPath]
        :rtype: list
        """
        everyone_in_frame = deque()

        for person_path in self.people_paths:
            if frame_number == person_path.image_frame_coordinates_list.current_frame_coord().frame_number:
                everyone_in_frame.append(person_path)

        return list(everyone_in_frame)

