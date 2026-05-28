import pygame
from constants import (
    COLORS, CELL_SIZE, grid_pixel_width, grid_pixel_height,
    grid_offset_x, GRID_OFFSET_Y,
    EMPTY, OBSTACLE, FORBIDDEN, DIFFICULT, START, END,
    ANIMATION_SPEED, DRONE_SPEED
)
import math


class Visualizer:
    # initialiser visualiseur
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.explored_nodes = []
        self.path = []
        self.animation_progress = 0.0
        self.is_animating = False
        self.animation_endedAt = 0
        self.image = pygame.image.load("./drone.png").convert_alpha()
        self.brickwall_image = pygame.image.load("./brickwall.png").convert()
        self.base_image = pygame.image.load("./base.png").convert_alpha()
        self.start_image = pygame.image.load("./start.png").convert_alpha()
        self.destination_image = pygame.image.load("./destination.png").convert_alpha()

    # dessiner animation drone
    def drawDroneImage(self):
        if self.is_animating or not self.path or len(self.path) < 2:
            return

        t = (pygame.time.get_ticks() - self.animation_endedAt) * DRONE_SPEED / 1000.0

        cell_index = int(t)
        percentage = t % 1

        if cell_index >= len(self.path) - 1:
            cell_index = len(self.path) - 2
            percentage = 1.0

        cell_a = self.path[cell_index]
        cell_b = self.path[cell_index + 1]

        if cell_a is None or cell_b is None:
            return

        cell_w = grid_pixel_width / self.grid.width
        cell_h = grid_pixel_height / self.grid.height

        ax = cell_a.col * cell_w
        ay = cell_a.row * cell_h

        bx = cell_b.col * cell_w
        by = cell_b.row * cell_h

        interp_x = ax + (bx - ax) * percentage
        interp_y = ay + (by - ay) * percentage

        x = grid_offset_x + interp_x
        y = GRID_OFFSET_Y + interp_y

        drone_size = min(cell_w, cell_h) * 0.6
        drone_x = x + (cell_w - drone_size) / 2
        drone_y = y + (cell_h - drone_size) / 2

        dx = bx - ax
        dy = by - ay
        angle = math.degrees(math.atan2(-dy, dx) + math.pi / 2)
        
        rotated = pygame.transform.rotate(self.image, angle)
        rect = rotated.get_rect(center=(drone_x + drone_size/2, drone_y + drone_size/2))
        
        self.screen.blit(rotated, rect.topleft)        
            

    # definir donnees de recherche de chemin
    def set_pathfinding_data(self, explored_nodes, path):
        cellheight = grid_pixel_height / self.grid.height
        
        self.image = pygame.transform.scale(self.image, (int(cellheight), int(cellheight)))

        self.explored_nodes = explored_nodes
        self.path = path
        self.animation_progress = 0.0
        self.is_animating = True
        self.animation_endedAt = 0

    # mettre a jour animation
    def update_animation(self):
        if self.is_animating:
            self.animation_progress += ANIMATION_SPEED / 100.0
            if self.animation_progress >= 1.0:
                self.animation_progress = 1.0
                self.is_animating = False
                self.animation_endedAt = pygame.time.get_ticks()

    # verifier si drone a la destination
    def has_drone_reached_destination(self):
        return not self.is_animating and self.animation_endedAt > 0 and self.path and len(self.path) >= 2

    # dessiner lignes de grille
    def draw_grid(self):
        pygame.draw.rect(self.screen, (245, 245, 245), 
                        (grid_offset_x, GRID_OFFSET_Y, grid_pixel_width, grid_pixel_height))
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (grid_offset_x, GRID_OFFSET_Y, grid_pixel_width, grid_pixel_height), 2)
        
        cellheight = grid_pixel_height / self.grid.height
        cellwidth = grid_pixel_width / self.grid.width
        
        for r in range(self.grid.height + 1):
            pygame.draw.line(self.screen, (220, 220, 220),
                            (grid_offset_x, GRID_OFFSET_Y + r * cellheight),
                            (grid_offset_x + grid_pixel_width, GRID_OFFSET_Y + r * cellheight), 1)

        for c in range(self.grid.width + 1):
            pygame.draw.line(self.screen, (220, 220, 220),
                            (grid_offset_x + c * cellwidth, GRID_OFFSET_Y),
                            (grid_offset_x + c * cellwidth, GRID_OFFSET_Y + grid_pixel_height), 1)
    
    # dessiner couleurs des cellules
    def draw_cells(self):
        cellheight = grid_pixel_height / self.grid.height
        cellwidth = grid_pixel_width / self.grid.width

        for r in range(self.grid.height):
            for c in range(self.grid.width):
                cell = self.grid.get_cell(r, c)
                x = grid_offset_x + c * cellwidth
                y = GRID_OFFSET_Y + r * cellheight

                if cell.cell_type == OBSTACLE:
                    brick_scaled = pygame.transform.scale(self.brickwall_image, (int(cellwidth), int(cellheight)))
                    self.screen.blit(brick_scaled, (x, y))
                elif cell.cell_type == FORBIDDEN:
                    base_scaled = pygame.transform.scale(self.base_image, (int(cellwidth), int(cellheight)))
                    self.screen.blit(base_scaled, (x, y))
                elif cell.cell_type == START:
                    start_scaled = pygame.transform.scale(self.start_image, (int(cellwidth), int(cellheight)))
                    self.screen.blit(start_scaled, (x, y))
                elif cell.cell_type == END:
                    destination_scaled = pygame.transform.scale(self.destination_image, (int(cellwidth), int(cellheight)))
                    self.screen.blit(destination_scaled, (x, y))
                else:
                    color = COLORS.get(cell.cell_type, (245, 245, 245))
                    pygame.draw.rect(self.screen, color,
                                    (x, y, cellwidth, cellheight))

    # dessiner cellules explorees
    def draw_explored_nodes(self):
        cellheight = grid_pixel_height / self.grid.height
        cellwidth = grid_pixel_width / self.grid.width

        num_to_show = int(len(self.explored_nodes) * self.animation_progress)

        for i in range(num_to_show):
            cell = self.explored_nodes[i]
            x = grid_offset_x + cell.col * cellwidth
            y = GRID_OFFSET_Y + cell.row * cellheight

            pygame.draw.rect(self.screen, COLORS['explored'],
                            (x, y, cellwidth, cellheight))

    # dessiner ligne de chemin
    def draw_path(self):
        if not self.path or len(self.path) < 2 or self.is_animating:
            return

        valid_path = []
        for cell in self.path:
            if cell is None:
                continue
            if not hasattr(cell, 'row') or not hasattr(cell, 'col'):
                continue
            if not isinstance(cell.row, (int, float)) or not isinstance(cell.col, (int, float)):
                continue
            if cell.row < 0 or cell.col < 0:
                continue
            if cell.row >= self.grid.height or cell.col >= self.grid.width:
                continue
            valid_path.append(cell)

        if len(valid_path) < 2:
            return

        cellheight = grid_pixel_height / self.grid.height
        cellwidth = grid_pixel_width / self.grid.width
        
        for i, cell in enumerate(valid_path):
            if i == 0 or i == len(valid_path) - 1:
                continue

            x = grid_offset_x + int(cell.col * cellwidth)
            y = GRID_OFFSET_Y + int(cell.row * cellheight)
            pygame.draw.rect(self.screen, COLORS['path'], (x, y, cellwidth, cellheight))

        points = [
            (int(grid_offset_x + cell.col * cellwidth + cellwidth // 2),
                int(GRID_OFFSET_Y + cell.row * cellheight + cellheight // 2))
            for cell in valid_path
        ]

        if len(points) >= 2:
            pygame.draw.lines(self.screen, (100, 0, 100), False, points, 3)

    # dessiner nombres de cout
    def draw_cell_costs_text(self):
        cellheight = grid_pixel_height / self.grid.height
        cellwidth = grid_pixel_width / self.grid.width

        font = pygame.font.Font(None, 20)

        for r in range(self.grid.height):
            for c in range(self.grid.width):
                cell = self.grid.get_cell(r, c)

                if cell.cell_type == DIFFICULT:
                    x = grid_offset_x + int(cell.col * cellwidth) + cellwidth // 2
                    y = GRID_OFFSET_Y + int(cell.row * cellheight) + cellheight // 2

                    text_surface = font.render("3", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(x, y))
                    self.screen.blit(text_surface, text_rect)
    
    # dessiner tout
    def draw_all(self):
        self.draw_grid()
        self.draw_cells()
        self.draw_explored_nodes()
        self.draw_path()
        self.draw_cell_costs_text()
        self.drawDroneImage()
        
    # effacer visualisation
    def clear_pathfinding_visualization(self):
        self.explored_nodes = []
        self.path = []
        self.animation_progress = 0.0
        self.is_animating = False
        self.animation_endedAt = 0
    
    # obtenir cellule depuis position ecran
    def get_cell_from_screen_pos(self, pos):
        x, y = pos
        
        if x < grid_offset_x or x >= grid_offset_x + grid_pixel_width:
            return None, None
        if y < GRID_OFFSET_Y or y >= GRID_OFFSET_Y + grid_pixel_height:
            return None, None
        cellheight = grid_pixel_height / self.grid.height
        cellwidth = grid_pixel_width / self.grid.width
            
        col = (x - grid_offset_x) // cellwidth
        row = (y - GRID_OFFSET_Y) // cellheight
        
        if row >= self.grid.height or col >= self.grid.width:
            return None, None
        
        return row, col
        
    def cell_to_screen(self, row, col):
        cell_w, cell_h = self.grid.cellSize
        x = grid_offset_x + col * cell_w
        y = GRID_OFFSET_Y + row * cell_h
        return x, y