# ============================================================================
# GRID MODULE - Grid and Cell Management
# ============================================================================

import random
from constants import (
    CELL_SIZE, EMPTY, OBSTACLE, FORBIDDEN, DIFFICULT, START, END,
    CELL_COSTS, grid_width, grid_height,grid_pixel_height,grid_pixel_width
)


class Cell:
    
    def __init__(self, row, col, cell_type=EMPTY):
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.cost = CELL_COSTS.get(cell_type, 1)
    
    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __repr__(self):
        return f"Cell({self.row}, {self.col}, type={self.cell_type})"


class Grid:
    """Manages the 2D grid and cell operations."""
    
    def __init__(self, width=grid_width, height=grid_height):
        self.width = width
        self.height = height
        self.cells = [[Cell(r, c, EMPTY) for c in range(width)] for r in range(height)]
        self.start = None
        self.end = None

    def refill(self, width, height):
        if self.width == width and self.height == height:
            return
        self.width = width
        self.height = height

        
        self.cells = [[Cell(r, c, EMPTY) for c in range(width)] for r in range(height)]
        self.start = None
        self.end = None
    
    def get_cell(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.cells[row][col]
        return None
    
    def set_cell(self, row, col, cell_type):
   
        if 0 <= row < self.height and 0 <= col < self.width:
            cell = self.cells[row][col]
            cell.cell_type = cell_type
            cell.cost = CELL_COSTS.get(cell_type, 1)
            
            # Track start and end positions
            if cell_type == START:
                self.start = cell
            elif cell_type == END:
                self.end = cell
    
    def is_walkable(self, row, col):
        """Check if a cell can be walked on."""
        cell = self.get_cell(row, col)
        if cell is None:
            return False
        return cell.cost != float('inf')
    
    def get_neighbors(self, cell):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = cell.row + dr, cell.col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append(self.get_cell(new_row, new_col))
        
        return neighbors
    
    def clear(self):
        """Clear the grid back to all empty cells."""
        self.cells = [[Cell(r, c, EMPTY) for c in range(self.width)] for r in range(self.height)]
        self.start = None
        self.end = None
    
    def generate_random_map(self, obstacle_density=0.2, forbidden_density=0.1, difficult_density=0.15):
        self.clear()
        
        for r in range(self.height):
            for c in range(self.width):
                rand = random.random()
                
                if rand < obstacle_density:
                    self.set_cell(r, c, OBSTACLE)
                elif rand < obstacle_density + forbidden_density:
                    self.set_cell(r, c, FORBIDDEN)
                elif rand < obstacle_density + forbidden_density + difficult_density:
                    self.set_cell(r, c, DIFFICULT)
        
        # Set start and end points
        self.set_cell(0, 0, START)
        self.set_cell(self.height - 1, self.width - 1, END)
    
    def get_all_cells_of_type(self, cell_type):
        """Get all cells of a specific type."""
        cells = []
        for r in range(self.height):
            for c in range(self.width):
                if self.cells[r][c].cell_type == cell_type:
                    cells.append(self.cells[r][c])
        return cells
 