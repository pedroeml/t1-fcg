
class PersonPath:

    def __init__(self, id_number, image_frame_coordinates_list, world_frame_coordinates_list):
        """

        :param id_number:
        :param image_frame_coordinates_list:
        :type image_frame_coordinates_list: FrameCoordList
        :param world_frame_coordinates_list:
        :type world_frame_coordinates_list: FrameCoordList
        """
        self.id_number = id_number
        self.image_frame_coordinates_list = image_frame_coordinates_list
        self.world_frame_coordinates_list = world_frame_coordinates_list
