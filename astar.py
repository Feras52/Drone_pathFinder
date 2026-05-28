
import heapq
from constants import START, END


class Node:
    
    # initialiser noeud
    def __init__(self, cell, parent=None, g=0, h=0):
        self.cell = cell
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
    
    # comparer noeuds par valeur f
    def __lt__(self, other):
        return self.f < other.f
    
    # verifier egalite du noeud
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.cell == other.cell
    
    # hasher le noeud
    def __hash__(self):
        return hash(self.cell)
    
    # representation textuelle du noeud
    def __repr__(self):
        return f"Node({self.cell.row}, {self.cell.col}, f={self.f:.2f})"


class AStar:
    
    # initialiser pathfinder astar
    def __init__(self, grid):
        self.grid = grid
        self.explored = []
        self.frontier = []
        self.path = []
        self.total_cost = 0
        self.explored_count = 0
    
    # calculer distance manhattan
    def heuristic(self, cell, goal_cell):
        return abs(cell.row - goal_cell.row) + abs(cell.col - goal_cell.col)
    
    # reconstruire le chemin depuis le noeud
    def reconstruct_path(self, node):
        path = []
        current = node
        while current is not None:
            path.append(current.cell)
            current = current.parent
        path.reverse()
        return path
    
    # trouver le chemin optimal avec astar
    def find_path(self, start_cell, end_cell):
        self.explored = []
        self.frontier = []
        self.path = []
        self.total_cost = 0
        self.explored_count = 0
        
        if start_cell is None or end_cell is None:
            return [], 0, 0
        
        if not self.grid.is_walkable(start_cell.row, start_cell.col):
            return [], 0, 0
        
        if not self.grid.is_walkable(end_cell.row, end_cell.col):
            return [], 0, 0
        
        start_node = Node(
            start_cell,
            parent=None,
            g=0,
            h=self.heuristic(start_cell, end_cell)
        )
        heapq.heappush(self.frontier, start_node)
        
        visited = {start_cell}
        
        while self.frontier:
            current_node = heapq.heappop(self.frontier)
            self.explored.append(current_node.cell)
            self.explored_count += 1
            
            if current_node.cell == end_cell:
                self.path = self.reconstruct_path(current_node)
                self.total_cost = current_node.g
                return self.path, self.total_cost, self.explored_count
            
            neighbors = self.grid.get_neighbors(current_node.cell)
            
            for neighbor_cell in neighbors:
                if neighbor_cell in visited:
                    continue
                
                visited.add(neighbor_cell)
                
                new_g = current_node.g + neighbor_cell.cost
                
                h = self.heuristic(neighbor_cell, end_cell)
                
                neighbor_node = Node(
                    neighbor_cell,
                    parent=current_node,
                    g=new_g,
                    h=h
                )
                
                heapq.heappush(self.frontier, neighbor_node)
        
        return [], 0, self.explored_count
    
    # retourner la liste des noeuds explores
    def get_explored_nodes(self):
        return self.explored
    
    # retourner le chemin final
    def get_path(self):
        return self.path
