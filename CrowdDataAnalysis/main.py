from persistence import frame_data_reader
from analysis import utils
import numpy as np
from const import *
import visualization.utils
from visualization import display_frame, view
from analysis import distancing, grouping

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print('OpenGL wrapper for Python not found!')


# The main function
def main():
    # Initialize OpenGL
    glutInit(sys.argv)

    # Set display mode
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    # Set size and position of window size
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)

    # Create window with given title
    glutCreateWindow(b'3DView')

    viewing = view.View(all_frames_filespath, people_paths, world_background, people_graph, colors, world_min_x, world_min_y, time_per_frame)
    viewing.inicializa()

    # The callback for display function
    glutDisplayFunc(viewing.desenha)

    # The callback for reshape function
    glutReshapeFunc(viewing.altera_tamanho_janela)

    glutKeyboardFunc(viewing.teclado)

    # The callback function for keyboard controls
    glutSpecialFunc(viewing.teclas_especiais)

    glutMotionFunc(viewing.gerencia_movim)

    glutMouseFunc(viewing.gerencia_mouse)

    # Start the main loop
    glutMainLoop()


# Call the main function
if __name__ == '__main__':
    # Some directories doesn't have %06d.jpg file name format! In this case, try %04.jpg

    if FPS > 0:
        time_per_frame = int(1000 / FPS)  # 24 fps = 1000 ms/24 frames = 41,666 ms
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

    world_background = np.ones((world_height, world_width, 3), np.uint8) * 175

    colors = visualization.utils.generate_colors()

    main()
