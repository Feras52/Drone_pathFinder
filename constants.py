import pygame

EMPTY = 0
OBSTACLE = 1
FORBIDDEN = 2
DIFFICULT = 3
START = 4
END = 5

CELL_COSTS = {
    EMPTY: 1,
    OBSTACLE: float('inf'),
    FORBIDDEN: float('inf'),
    DIFFICULT: 3,
    START: 1,
    END: 1
}

COLORS = {
    EMPTY: (245, 245, 245),
    OBSTACLE: (40, 40, 40),
    FORBIDDEN: (231, 76, 60),
    DIFFICULT: (241, 196, 15),
    START: (46, 204, 113),
    END: (52, 152, 219),
    'explored': (241, 196, 15),
    'path': (155, 89, 182),
    'button': (236, 240, 241),
    'button_hover': (189, 195, 199),
    'button_active': (52, 152, 219),
    'button_text': (44, 62, 80),
    'sidebar_bg': (236, 240, 241),
    'slider_bg': (200, 200, 200),
    'slider_fill': (100, 100, 100)
}

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
grid_width  :int = 31
grid_height = 21
CELL_SIZE = 40



grid_pixel_width = grid_width * CELL_SIZE
grid_pixel_height = grid_height * CELL_SIZE

grid_offset_x = 20
GRID_OFFSET_Y = 20


SIDEBAR_WIDTH = 300
SIDEBAR_X = SCREEN_WIDTH - SIDEBAR_WIDTH - 10

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 45
BUTTON_MARGIN = 12
BUTTON_FONT_SIZE = 13
BUTTON_RADIUS = 8

FPS = 60
ANIMATION_SPEED = 0.5
DRONE_SPEED = 4.0

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

TOOL_NONE = 0
TOOL_START = 1
TOOL_END = 2
TOOL_OBSTACLE = 3
TOOL_FORBIDDEN = 4
TOOL_DIFFICULT = 5
