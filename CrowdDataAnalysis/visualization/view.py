from const import *
from analysis import distancing, grouping, group_analysis
from visualization import display_frame
from pprint import pprint

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except Exception as expt:
    print("OpenGL wrapper for python not found")


class View:
    def __init__(self, all_frames_filespath, people_paths, world_background, people_graph, colors, world_min_x, world_min_y, time_per_frame):
        self.rotX = 0
        self.rotY = 0
        self.rotX_ini = 0
        self.rotY_ini = 0
        self.obsX = 0
        self.obsY = 450
        self.obsZ = 1000
        self.obsX_ini = 0
        self.obsY_ini = 0
        self.obsZ_ini = 0
        self.fAspect = 1
        self.angle = 44
        self.x_ini = 0
        self.y_ini = 0
        self.bot = 0
        self.SENS_ROT = 5.0
        self.SENS_OBS = 10.0
        self.SENS_TRANSL = 30.0
        self.clear = False
        self.all_frames_filespath = all_frames_filespath
        self.people_paths = people_paths
        self.world_background = world_background
        self.people_graph = people_graph
        self.colors = colors
        self.world_min_x = world_min_x
        self.world_min_y = world_min_y
        self.time_per_frame = time_per_frame
        self.previous_groups = None
        self.frame_number = 0
        self.group_analysis = None

    def posiciona_observador(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.obsX, self.obsY, self.obsZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    def especifica_parametros_visualizacao(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.angle, self.fAspect, 0.5, 3000)

        self.posiciona_observador()

    def desenha_chao(self):
        glColor3f(0, 0, 0)
        glLineWidth(3)
        glBegin(GL_LINES)

        for z in range(-1000, 1000, 10):
            glVertex3f(-1000, -0.1, z)
            glVertex3f(1000, -0.1, z)

        for x in range(-1000, 1000, 10):
            glVertex3f(x, -0.1, -1000)
            glVertex3f(x, -0.1, 1000)

        glEnd()
        glLineWidth(1)

    def add_solid_cube(self, x, z, width, height, r, g, b):
        glColor3f(r, g, b)
        glPushMatrix()
        y = height * width / 2
        glTranslatef(x, y, z)
        glRotatef(-90, 1, 0, 0)
        glEnable(GL_DEPTH_TEST)    # desenha na ordem certa

        glutSolidCube(height * height)

        glPopMatrix()

    def add_solid_cone(self, x, z, width, height, r, g, b):
        glColor3f(r, g, b)
        glPushMatrix()
        y = height * width / 2
        glTranslatef(x, y, z)
        glRotatef(-90, 1, 0, 0)
        glEnable(GL_DEPTH_TEST)    # desenha na ordem certa

        glutSolidCone(width * 7, height * 7, 6, 4)

        glPopMatrix()

    def add_solid_sphere(self, x, z, width, height, r, g, b):
        glColor3f(r, g, b)
        glPushMatrix()
        y = height * width / 2
        glTranslatef(x, y, z)
        glRotatef(-90, 1, 0, 0)
        glEnable(GL_DEPTH_TEST)    # desenha na ordem certa

        glutSolidSphere((height + height) * 3, 6, 4)

        glPopMatrix()

    def desenha(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if not self.clear:
            self.especifica_parametros_visualizacao()
            frame_filepath = ''
            try:
                frame_filepath = self.all_frames_filespath[self.frame_number]
            except:
                print('FINISHED!')
                if not self.group_analysis.exported:
                    analysis = self.group_analysis.export_analysis('group_analysis.json')
                sys.exit(0)

            if frame_filepath:
                everyone_in_frame = self.people_paths.everyone_in_frame(self.frame_number)
                people_graph = distancing.calc_distances_for_everyon_in_frame(everyone_in_frame, self.people_graph, TOO_FAR_DISTANCE, MINIMUM_DISTANCE_CHANGE)
                groups = grouping.detect_group(people_graph, everyone_in_frame, GROUPING_MAX_DISTANCE)
                if self.previous_groups is not None:
                    grouping.compare_groups(self.previous_groups, groups)
                    self.previous_groups = groups
                else:
                    self.previous_groups = groups

                if self.group_analysis is None and len(groups) > 0:
                    self.group_analysis = group_analysis.GroupAnalysis(groups)
                elif len(groups) > 0:
                    self.group_analysis.receive_groups(groups)

                displayed_frame = display_frame.display(frame_filepath, self.world_background, everyone_in_frame, groups, self.colors, self.world_min_x, self.world_min_y, self.time_per_frame)
                self.frame_number += 1

                i = 0
                if displayed_frame:
                    for person_coord in displayed_frame:
                        if i % 5 == 0:
                            self.add_solid_cube(person_coord[0] - 700, person_coord[1] - 700, 6, 6, person_coord[2][0], person_coord[2][1], person_coord[2][2])
                        elif i % 2 == 0:
                            self.add_solid_cone(person_coord[0] - 700, person_coord[1] - 700, 6, 6, person_coord[2][0], person_coord[2][1], person_coord[2][2])
                        else:
                            self.add_solid_sphere(person_coord[0] - 700, person_coord[1] - 700, 6, 6, person_coord[2][0], person_coord[2][1], person_coord[2][2])
                        i += 1

        self.desenha_chao()

        glFlush()

    def altera_tamanho_janela(self, w, h):
        # Para previnir uma divisão por zero
        if h == 0:
            h = 1

        # Especifica as dimensões da viewport
        glViewport(0, 0, w, h)

        # Calcula a correção de aspecto
        self.fAspect = w / h

        self.especifica_parametros_visualizacao()

    def teclado(self, *args):
        # If escape is pressed, kill everything.
        if args[0] == chr(27):
            print('ESC')
            sys.exit()

    def teclas_especiais(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.obsX -= 5
        elif key == GLUT_KEY_RIGHT:
            self.obsX += 5
        elif key == GLUT_KEY_UP:
            self.obsY += 5
        elif key == GLUT_KEY_DOWN:
            self.obsY -= 5
        elif key == GLUT_KEY_PAGE_UP:
            self.obsZ += 3
        elif key == GLUT_KEY_PAGE_DOWN:
            self.obsZ -= 3
        elif key == GLUT_KEY_END:
            self.clear = not self.clear

        glutPostRedisplay()

    def inicializa(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glLineWidth(2.0)

    def gerencia_mouse(self, button, state, x, y):
        if state == GLUT_DOWN:
            # Salva os parâmetros atuais
            self.x_ini = x
            self.y_ini = y
            self.obsX_ini = self.obsX
            self.obsY_ini = self.obsY
            self.obsZ_ini = self.obsZ
            self.rotX_ini = self.rotX
            self.rotY_ini = self.rotY
            self.bot = button

        else:
            self.bot = -1

    def gerencia_movim(self, x, y):
        if self.bot == GLUT_LEFT_BUTTON:
            deltax = self.x_ini - x
            deltay = self.y_ini - y

            self.rotY = self.rotY_ini - deltax / self.SENS_ROT
            self.rotX = self.rotX_ini - deltay / self.SENS_ROT
        elif self.bot == GLUT_RIGHT_BUTTON:
            deltaz = self.y_ini - y

            self.obsZ = self.obsZ_ini + deltaz / self.SENS_OBS
        elif self.bot == GLUT_MIDDLE_BUTTON:
            deltax = self.x_ini - x
            deltay = self.y_ini - y

            self.obsX = self.obsX_ini + deltax / self.SENS_TRANSL
            self.obsY = self.obsY_ini - deltay / self.SENS_TRANSL

        self.posiciona_observador()
        glutPostRedisplay()
