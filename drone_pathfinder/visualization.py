# ============================================================================
# VISUALIZATION MODULE - Pygame Rendering and Graphics
# ============================================================================

import pygame
from constants import (
    COLORS, CELL_SIZE, GRID_PIXEL_WIDTH, GRID_PIXEL_HEIGHT,
    GRID_OFFSET_X, GRID_OFFSET_Y,
    EMPTY, OBSTACLE, FORBIDDEN, DIFFICULT, START, END,
    ANIMATION_SPEED
)


class Visualizer:
    """Handles all visual rendering and animations."""
    
    def __init__(self, screen, grid):
        """
        Initialize the visualizer.
        
        Args:
            screen: Pygame screen surface
            grid: Grid object to visualize
        """
        self.screen = screen
        self.grid = grid
        self.explored_nodes = []
        self.path = []
        self.animation_progress = 0.0
        self.is_animating = False
    
    def set_pathfinding_data(self, explored_nodes, path):
        """
        Set the data to visualize from pathfinding.
        
        Args:
            explored_nodes (list): List of explored cells
            path (list): List of path cells
        """
        self.explored_nodes = explored_nodes
        self.path = path
        self.animation_progress = 0.0
        self.is_animating = True
    
    def update_animation(self):
        """Update animation progress."""
        if self.is_animating:
            self.animation_progress += ANIMATION_SPEED / 100.0
            if self.animation_progress >= 1.0:
                self.animation_progress = 1.0
                self.is_animating = False
    
    def draw_grid(self):
        """Draw the grid background."""
        pygame.draw.rect(self.screen, (245, 245, 245), 
                        (GRID_OFFSET_X, GRID_OFFSET_Y, GRID_PIXEL_WIDTH, GRID_PIXEL_HEIGHT))
        
        # Draw border around grid
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (GRID_OFFSET_X, GRID_OFFSET_Y, GRID_PIXEL_WIDTH, GRID_PIXEL_HEIGHT), 2)
        
        # Draw grid lines
        for r in range(self.grid.height + 1):
            pygame.draw.line(self.screen, (220, 220, 220),
                            (GRID_OFFSET_X, GRID_OFFSET_Y + r * CELL_SIZE),
                            (GRID_OFFSET_X + GRID_PIXEL_WIDTH, GRID_OFFSET_Y + r * CELL_SIZE), 1)
        
        for c in range(self.grid.width + 1):
            pygame.draw.line(self.screen, (220, 220, 220),
                            (GRID_OFFSET_X + c * CELL_SIZE, GRID_OFFSET_Y),
                            (GRID_OFFSET_X + c * CELL_SIZE, GRID_OFFSET_Y + GRID_PIXEL_HEIGHT), 1)
    
    def draw_cells(self):
        """Draw all cells with their colors."""
        for r in range(self.grid.height):
            for c in range(self.grid.width):
                cell = self.grid.get_cell(r, c)
                color = COLORS.get(cell.cell_type, (245, 245, 245))
                
                x = GRID_OFFSET_X + c * CELL_SIZE
                y = GRID_OFFSET_Y + r * CELL_SIZE
                
                pygame.draw.rect(self.screen, color,
                                (x, y, CELL_SIZE, CELL_SIZE))
    
    def draw_explored_nodes(self):
        """Draw the explored nodes with animation."""
        # Calculate how many nodes to show based on animation progress
        num_to_show = int(len(self.explored_nodes) * self.animation_progress)
        
        for i in range(num_to_show):
            cell = self.explored_nodes[i]
            x = GRID_OFFSET_X + cell.col * CELL_SIZE
            y = GRID_OFFSET_Y + cell.row * CELL_SIZE
            
            # Draw explored node in yellow
            pygame.draw.rect(self.screen, COLORS['explored'],
                            (x, y, CELL_SIZE, CELL_SIZE))
    
    def draw_path(self):
        """Draw the final path."""
        if not self.path or len(self.path) < 2:
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

        for i, cell in enumerate(valid_path):
            if i == 0 or i == len(valid_path) - 1:
                continue

            x = GRID_OFFSET_X + int(cell.col * CELL_SIZE)
            y = GRID_OFFSET_Y + int(cell.row * CELL_SIZE)
            pygame.draw.rect(self.screen, COLORS['path'], (x, y, CELL_SIZE, CELL_SIZE))

        if self.animation_progress >= 1.0:
            points = [
                (int(GRID_OFFSET_X + cell.col * CELL_SIZE + CELL_SIZE // 2),
                 int(GRID_OFFSET_Y + cell.row * CELL_SIZE + CELL_SIZE // 2))
                for cell in valid_path
            ]

            if len(points) >= 2:
                pygame.draw.lines(self.screen, (100, 0, 100), False, points, 3)

    def draw_cell_costs_text(self):
        """Draw text showing cost for difficult zones (optional)."""
        font = pygame.font.Font(None, 20)

        for r in range(self.grid.height):
            for c in range(self.grid.width):
                cell = self.grid.get_cell(r, c)

                if cell.cell_type == DIFFICULT:
                    x = GRID_OFFSET_X + c * CELL_SIZE + CELL_SIZE // 2
                    y = GRID_OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2

                    text_surface = font.render("3", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(x, y))
                    self.screen.blit(text_surface, text_rect)
    
    def draw_all(self):
        """Draw everything in the correct order."""
        # Background
        self.draw_grid()
        
        # Cells
        self.draw_cells()
        
        # Explored nodes (with animation)
        self.draw_explored_nodes()
        
        # Final path
        self.draw_path()
        
        # Optional: cost text
        self.draw_cell_costs_text()
    
    def clear_pathfinding_visualization(self):
        """Clear the pathfinding visualization."""
        self.explored_nodes = []
        self.path = []
        self.animation_progress = 0.0
        self.is_animating = False
    
    def get_cell_from_screen_pos(self, pos):
        """
        Convert screen coordinates to grid coordinates.
        
        Args:
            pos (tuple): (x, y) screen position
            
        Returns:
            tuple: (row, col) grid position or (None, None) if out of bounds
        """
        x, y = pos
        
        # Check if click is within grid area
        if x < GRID_OFFSET_X or x >= GRID_OFFSET_X + GRID_PIXEL_WIDTH:
            return None, None
        if y < GRID_OFFSET_Y or y >= GRID_OFFSET_Y + GRID_PIXEL_HEIGHT:
            return None, None
        
        col = (x - GRID_OFFSET_X) // CELL_SIZE
        row = (y - GRID_OFFSET_Y) // CELL_SIZE
        
        # Bounds check
        if row >= self.grid.height or col >= self.grid.width:
            return None, None
        
        return row, col
