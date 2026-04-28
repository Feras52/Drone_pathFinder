# ============================================================================
# CONSTANTS - Configuration for Drone Pathfinder Simulator
# ============================================================================

import pygame

# ============================================================================
# CELL TYPES
# ============================================================================
EMPTY = 0
OBSTACLE = 1
FORBIDDEN = 2
DIFFICULT = 3
START = 4
END = 5

# ============================================================================
# COST VALUES FOR EACH CELL TYPE
# ============================================================================
CELL_COSTS = {
    EMPTY: 1,
    OBSTACLE: float('inf'),  # Cannot pass
    FORBIDDEN: float('inf'),  # Cannot pass
    DIFFICULT: 3,  # Higher energy cost
    START: 1,
    END: 1
}

# ============================================================================
# COLORS (RGB)
# ============================================================================
COLORS = {
    EMPTY: (245, 245, 245),       # Very light gray (not pure white)
    OBSTACLE: (40, 40, 40),         # Dark gray/black
    FORBIDDEN: (231, 76, 60),       # Red
    DIFFICULT: (241, 196, 15),      # Orange/Gold
    START: (46, 204, 113),          # Green
    END: (52, 152, 219),            # Blue
    'explored': (241, 196, 15),     # Gold/Yellow
    'path': (155, 89, 182),         # Purple
    'button': (236, 240, 241),      # Light gray
    'button_hover': (189, 195, 199), # Medium gray
    'button_active': (52, 152, 219), # Blue
    'button_text': (44, 62, 80),    # Dark text
    'sidebar_bg': (236, 240, 241),  # Light gray background
    'slider_bg': (200, 200, 200),   # Light gray slider background
    'slider_fill': (100, 100, 100)   # Dark gray slider fill
}

# ============================================================================
# SCREEN AND GRID SETTINGS
# ============================================================================
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
grid_width  :int = 31
grid_height = 21
CELL_SIZE = 40  # pixels per cell


# Calculate actual grid dimensions
grid_pixel_width = grid_width * CELL_SIZE
grid_pixel_height = grid_height * CELL_SIZE

# Position grid on the left with sidebar on right
grid_offset_x = 20
GRID_OFFSET_Y = 20  # Top padding


# Sidebar for UI - positioned on the right
SIDEBAR_WIDTH = 300
SIDEBAR_X = SCREEN_WIDTH - SIDEBAR_WIDTH - 10

# ============================================================================
# UI BUTTON SETTINGS
# ============================================================================
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 45
BUTTON_MARGIN = 12
BUTTON_FONT_SIZE = 13
BUTTON_RADIUS = 8  # Rounded corners

# ============================================================================
# ANIMATION AND PERFORMANCE
# ============================================================================
FPS = 60
ANIMATION_SPEED = 0.5  # Controls speed of node exploration visualization (0.1 to 1.0)
DRONE_SPEED = 4.0  # Controls drone travel speed multiplier (1.0 = normal, 2.0 = twice as fast)

# ============================================================================
# MOVEMENT DIRECTIONS (4-way: up, down, left, right)
# ============================================================================
DIRECTIONS = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1)    # Right
]

# ============================================================================
# UI TOOL TYPES
# ============================================================================
TOOL_NONE = 0
TOOL_START = 1
TOOL_END = 2
TOOL_OBSTACLE = 3
TOOL_FORBIDDEN = 4
TOOL_DIFFICULT = 5
