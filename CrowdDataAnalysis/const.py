import configparser


def load_config_file(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)

    input_folder_path = config['DEFAULT']['InputFolderPath']
    too_far_distance = int(config['DEFAULT']['TooFarDistance'])
    grouping_max_distance = int(config['DEFAULT']['GroupingMaxDistance'])
    minimum_distance_change = int(config['DEFAULT']['MinimumDistanceChange'])
    fps = int(config['DEFAULT']['FPS'])

    return input_folder_path, too_far_distance, grouping_max_distance, minimum_distance_change, fps


INPUT_FOLDER_PATH, TOO_FAR_DISTANCE, GROUPING_MAX_DISTANCE, MINIMUM_DISTANCE_CHANGE, FPS = load_config_file('..\constants.conf')
