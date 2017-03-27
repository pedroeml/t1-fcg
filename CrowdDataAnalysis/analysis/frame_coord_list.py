
class FrameCoordList:

    def __init__(self, frame_coords):
        """

        :param frame_coords:
        :type frame_coords: [FrameCoord]
        """
        self.frame_coords = frame_coords
        self.current_index = 0

    def current_frame_coord(self):
        return self.frame_coords[self.current_index]

    def next_frame_coord(self):
        if self.current_index < len(self.frame_coords) - 1:
            self.current_index += 1
        return self.current_frame_coord()
