import gravity
import pygame
import gui
from vector import *

pygame.init()

FRAME_RATE = 25
RESOLUTION = (600, 600)
FONT_PATH: str = None
FONT_SIZE: int = 30

APP_NAME = "Gravity-Engine"

EVENTS = {"QUITE": 0, "PAUSE": 1}
STATES = {"OFF": 0, "ON": 1, "PAUSE": 2}

COLORS = {
    "BLACK": (40, 40, 40),
    "L_RED": (255, 100, 100),
    "L_GREEN": (100, 255, 100),
    "L_BLUE": (100, 100, 255),
    "WHITE": (240, 240, 240),
}


# class Color(object):
#     red: int = None
#     green: int = None
#     blue: int = None

#     def __init__(self, red, green, blue):
#         self.red = red
#         self.green = green
#         self.blue = blue

#     def __call__(self):
#         return (self.red, self.green, self.blue)


class Window(object):
    resolution = None
    display: pygame.Surface = None
    frame_color: tuple = None

    def __init__(self, window_resolution: tuple, window_name: str, frame_color: tuple=COLORS["BLACK"]):
        self.resolution = window_resolution
        self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(window_name)
        self.frame_color = frame_color

    def get_events(self):
        events: list = []
        event: int = None

        for pygame_event in pygame.event.get():

            if pygame_event.type == pygame.QUIT:
                event = EVENTS["QUITE"]

            elif pygame_event.type == pygame.KEYDOWN:

                if pygame_event.key == pygame.K_ESCAPE:
                    event = EVENTS["PAUSE"]

            else:
                continue

            events.append(event)

        return events

    def render(self, gui_page: gui.Page):
        
        self.display.fill(self.frame_color)#clear screen
        gui_page.render(self.display)#render current gui page
        
        pygame.display.flip()#flip buffer
        


class Scene(object):
    objects: list = None
    connections: list = None  # 2D list: for each object there is a separate list with True on indexes, where object is influenced by object of this index.

    def __init__(self, objects: tuple = tuple(), objects_connections: list = list()):
        self.objects = objects
        self.connections = objects_connections

    def __generate_inluancing_objects__(self, connections_index):
        object_index: int = 0
        influancing_objects: list = []

        for connection in self.connections[connections_index]:
            if connection == True:
                influancing_objects.append(self.objects[object_index])

            object_index += 1

        return influancing_objects

    def add_object(
        self,
        material_object: gravity.Object,
        object_connections: list,
        is_influancer: bool = True,
    ):

        for i in range(len(self.connections)):
            self.connections[i].append(is_influancer)

        self.objects.append(material_object)
        self.connections.append(object_connections)

    def update(self):
        object_index: int = 0

        for material_object in self.objects:
            material_object.update(self.__generate_inluancing_objects__(object_index))
            object_index += 1


class Cam(object):

    translation: Vector = None
    scale: int = None

    def __init__(self, translation, scale):
        self.translation = translation
        self.scale = scale

    def transform(self, transformation: Vector):
        self.translation = add_vectors(self.translate, transformation)

    def set_scale(self, new_scale: int):
        self.scale = new_scale


class Simulation(object):

    window: Window = None
    cam: Cam = None
    scene: Scene = None
    state: int = None
    clock: pygame.time.Clock = None
    frame_rate: int = None

    def __init__(
        self,
        window_resolution: tuple,
        frame_rate: int,
        frame_color: tuple,
        cam_translation: Vector,
        scale: int
    ):
        self.window = Window(window_resolution, APP_NAME, frame_color)
        self.frame_rate = frame_rate
        self.cam = Cam(cam_translation, scale)
        self.scene = Scene()
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in self.window.get_events():
            if event == EVENTS["QUITE"]:
                pygame.quit()
                self.state = STATES["OFF"]
            elif event == EVENTS["PAUSE"]:
                
                if self.state != STATES["PAUSE"]:
                    self.state = STATES["PAUSE"]
                else:
                    self.state = STATES["ON"]

    def handle_keys(self):
        pass

    def main_loop(self):
        
        main_interface = gui.Page(FONT_PATH, FONT_SIZE)
        menu_interface = gui.Page(FONT_PATH, FONT_SIZE)
        menu_interface.add_frame((100, 100), (200, 200), COLORS["L_BLUE"])
        menu_interface.frames[0].add_textbox("Hello, World!", (20, 20), COLORS["L_GREEN"], None)

        self.state = STATES["ON"]

        while self.state != STATES["OFF"]:
            self.clock.tick(self.frame_rate)

            
            if self.state != STATES["PAUSE"]:
                self.scene.update()
                self.window.render(main_interface)
            else:
                self.window.render(menu_interface)
            
            self.handle_events()


app = Simulation(RESOLUTION, FRAME_RATE, COLORS["BLACK"], (0, 0), 1)
app.main_loop()
