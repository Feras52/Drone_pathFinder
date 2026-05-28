import random
from constants import (
    CELL_SIZE, EMPTY, OBSTACLE, FORBIDDEN, DIFFICULT, START, END,
    CELL_COSTS, grid_width, grid_height,grid_pixel_height,grid_pixel_width
)


class Cell:
    
    # initialiser cellule
    def __init__(self, row, col, cell_type=EMPTY):
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.cost = CELL_COSTS.get(cell_type, 1)
    
    # verifier egalite de la cellule
    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.row == other.row and self.col == other.col
    
    # hasher la cellule
    def __hash__(self):
        return hash((self.row, self.col))
    
    # representation textuelle de la cellule
    def __repr__(self):
        return f"Cell({self.row}, {self.col}, type={self.cell_type})"


class Grid:
    
    # initialiser grille
    def __init__(self, width=grid_width, height=grid_height):
        self.width = width
        self.height = height
        self.cells = [[Cell(r, c, EMPTY) for c in range(width)] for r in range(height)]
        self.start = None
        self.end = None

    # redimensionner et reinitialiser la grille
    def refill(self, width, height):
        if self.width == width and self.height == height:
            return
        self.width = width
        self.height = height

        
        self.cells = [[Cell(r, c, EMPTY) for c in range(width)] for r in range(height)]
        self.start = None
        self.end = None
    
    # obtenir cellule a position
    def get_cell(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.cells[row][col]
        return None
    
    # definir type de cellule
    def set_cell(self, row, col, cell_type):
   
        if 0 <= row < self.height and 0 <= col < self.width:
            cell = self.cells[row][col]
            cell.cell_type = cell_type
            cell.cost = CELL_COSTS.get(cell_type, 1)
            
            if cell_type == START:
                self.start = cell
            elif cell_type == END:
                self.end = cell
    
    # verifier si cellule est praticable
    def is_walkable(self, row, col):
        cell = self.get_cell(row, col)
        if cell is None:
            return False
        return cell.cost != float('inf')
    
    # obtenir cellules adjacentes
    def get_neighbors(self, cell):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = cell.row + dr, cell.col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append(self.get_cell(new_row, new_col))
        
        return neighbors
    
    # effacer toutes les cellules
    def clear(self):
        self.cells = [[Cell(r, c, EMPTY) for c in range(self.width)] for r in range(self.height)]
        self.start = None
        self.end = None
    
    # generer obstacles aleatoires
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
        
        self.set_cell(0, 0, START)
        self.set_cell(self.height - 1, self.width - 1, END)
    
    # obtenir cellules par type
    def get_all_cells_of_type(self, cell_type):
        cells = []
        for r in range(self.height):
            for c in range(self.width):
                if self.cells[r][c].cell_type == cell_type:
                    cells.append(self.cells[r][c])
        return cells
 