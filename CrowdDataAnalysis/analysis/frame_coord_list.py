
class FrameCoordList:

    def __init__(self, frame_coords):
        """

        :param frame_coords: [FrameCoord]
        :type frame_coords: list
        """
        self.frame_coords = frame_coords
        self.current_index = 0

    def current_frame_coord(self):
        """

        :return:
        :rtype: FrameCoord
        """
        return self.frame_coords[self.current_index]

    def next_frame_coord(self):
        """

        :return:
        :rtype: FrameCoord
        """
        if self.current_index < len(self.frame_coords) - 1:
            self.current_index += 1
        return self.current_frame_coord()

    def reset_current_index(self):
        self.current_index = 0

    def current_frame_coord_xy(self):
        """

        :return: int, int
        :rtype: tuple
        """
        return self.current_frame_coord().x, self.current_frame_coord().y
