# ============================================================================
# A* ALGORITHM MODULE - Pathfinding Implementation
# ============================================================================

import heapq
from constants import START, END


class Node:
    """Represents a node in the A* search space."""
    
    def __init__(self, cell, parent=None, g=0, h=0):
        """
        Initialize a node.
        
        Args:
            cell (Cell): The grid cell this node represents
            parent (Node): Parent node in the path
            g (float): Cost from start to this node
            h (float): Heuristic estimate from this node to goal
        """
        self.cell = cell
        self.parent = parent
        self.g = g  # Cost from start
        self.h = h  # Heuristic estimate
        self.f = g + h  # Total estimated cost (f = g + h)
    
    def __lt__(self, other):
        """Comparison for heap ordering."""
        return self.f < other.f
    
    def __eq__(self, other):
        """Equality based on cell position."""
        if not isinstance(other, Node):
            return False
        return self.cell == other.cell
    
    def __hash__(self):
        """Make node hashable."""
        return hash(self.cell)
    
    def __repr__(self):
        return f"Node({self.cell.row}, {self.cell.col}, f={self.f:.2f})"


class AStar:
    """
    Implements the A* pathfinding algorithm.
    
    A* uses: f(n) = g(n) + h(n)
    - g(n): actual cost from start to node n
    - h(n): heuristic estimate from node n to goal
    """
    
    def __init__(self, grid):
        """
        Initialize A* pathfinder.
        
        Args:
            grid (Grid): The grid to search on
        """
        self.grid = grid
        self.explored = []  # Nodes we've already processed
        self.frontier = []  # Nodes we need to explore (priority queue)
        self.path = []  # Final path from start to end
        self.total_cost = 0
        self.explored_count = 0
    
    def heuristic(self, cell, goal_cell):
        """
        Manhattan distance heuristic.
        
        Estimates the minimum distance from a cell to the goal.
        
        Args:
            cell (Cell): Current cell
            goal_cell (Cell): Goal cell
            
        Returns:
            float: Estimated distance
        """
        return abs(cell.row - goal_cell.row) + abs(cell.col - goal_cell.col)
    
    def reconstruct_path(self, node):
        """
        Reconstruct the path from start to goal.
        
        Args:
            node (Node): The goal node
            
        Returns:
            list: List of cells from start to goal
        """
        path = []
        current = node
        while current is not None:
            path.append(current.cell)
            current = current.parent
        path.reverse()
        return path
    
    def find_path(self, start_cell, end_cell):
        """
        Find the optimal path from start to end using A*.
        
        Args:
            start_cell (Cell): Starting cell
            end_cell (Cell): Goal cell
            
        Returns:
            tuple: (path, total_cost, explored_count) or ([], 0, 0) if no path found
        """
        # Reset state
        self.explored = []
        self.frontier = []
        self.path = []
        self.total_cost = 0
        self.explored_count = 0
        
        # Check for valid start and end
        if start_cell is None or end_cell is None:
            return [], 0, 0
        
        if not self.grid.is_walkable(start_cell.row, start_cell.col):
            return [], 0, 0
        
        if not self.grid.is_walkable(end_cell.row, end_cell.col):
            return [], 0, 0
        
        # Initialize with start node
        start_node = Node(
            start_cell,
            parent=None,
            g=0,
            h=self.heuristic(start_cell, end_cell)
        )
        heapq.heappush(self.frontier, start_node)
        
        # Track visited cells to avoid duplicates
        visited = {start_cell}
        
        # A* main loop
        while self.frontier:
            # Get node with lowest f value
            current_node = heapq.heappop(self.frontier)
            self.explored.append(current_node.cell)
            self.explored_count += 1
            
            # Check if we reached the goal
            if current_node.cell == end_cell:
                self.path = self.reconstruct_path(current_node)
                self.total_cost = current_node.g
                return self.path, self.total_cost, self.explored_count
            
            # Explore neighbors
            neighbors = self.grid.get_neighbors(current_node.cell)
            
            for neighbor_cell in neighbors:
                if neighbor_cell in visited:
                    continue
                
                visited.add(neighbor_cell)
                
                # Calculate g (cost from start to neighbor)
                new_g = current_node.g + neighbor_cell.cost
                
                # Calculate h (heuristic to goal)
                h = self.heuristic(neighbor_cell, end_cell)
                
                # Create neighbor node
                neighbor_node = Node(
                    neighbor_cell,
                    parent=current_node,
                    g=new_g,
                    h=h
                )
                
                # Add to frontier
                heapq.heappush(self.frontier, neighbor_node)
        
        # No path found
        return [], 0, self.explored_count
    
    def get_explored_nodes(self):
        """
        Get the list of explored nodes.
        
        Returns:
            list: Explored cells
        """
        return self.explored
    
    def get_path(self):
        """
        Get the final path.
        
        Returns:
            list: Path cells
        """
        return self.path
