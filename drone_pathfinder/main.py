# ============================================================================
# MAIN APPLICATION - Drone Delivery Pathfinder Simulator
# ============================================================================
# 
# This is a complete implementation of an A* pathfinding algorithm for
# drone delivery optimization. The application visualizes a 2D grid-based
# environment with obstacles, forbidden zones, and difficult terrain, and
# finds the optimal energy-efficient path from start to destination.
#
# Features:
# - Interactive grid with multiple cell types
# - A* algorithm with Manhattan distance heuristic
# - Real-time visualization of pathfinding process
# - UI controls for element placement
# - Results display showing energy cost and explored nodes
# ============================================================================

import pygame
import sys
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRID_WIDTH, GRID_HEIGHT,
    EMPTY, OBSTACLE, FORBIDDEN, DIFFICULT, START, END,
    TOOL_NONE, TOOL_START, TOOL_END, TOOL_OBSTACLE,
    TOOL_FORBIDDEN, TOOL_DIFFICULT
)
from grid import Grid, Cell
from astar import AStar
from ui import UIManager
from visualization import Visualizer


class DronePathfinderApp:
    """
    Main application class for the Drone Delivery Pathfinder Simulator.
    
    This class manages the entire application, including:
    - Grid management
    - A* algorithm execution
    - UI interactions
    - Visualization and rendering
    """
    
    def __init__(self):
        """Initialize the application."""
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Drone Delivery Pathfinder - A* Algorithm Simulator")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = FPS
        
        # Initialize components
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.astar = AStar(self.grid)
        self.ui_manager = UIManager()
        self.visualizer = Visualizer(self.screen, self.grid)
        
        # Application state
        self.path_found = False
        self.last_cost = 0
        self.last_explored_count = 0
    
    def handle_events(self):
        """Handle all user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle UI events
            action, data = self.ui_manager.handle_event(event, self.grid, self.astar)
            
            if action == 'run_astar':
                self.run_pathfinding()
            elif action == 'clear_grid':
                self.clear_grid()
            elif action == 'random_map':
                self.generate_random_map()
            elif action == 'set_tool':
                pass  # Tool is already set by UI manager
            
            # Handle grid clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    row, col = self.visualizer.get_cell_from_screen_pos(event.pos)
                    if row is not None and col is not None:
                        self.handle_grid_click(row, col)
    
    def handle_grid_click(self, row, col):
        """
        Handle a click on the grid.
        
        Args:
            row (int): Grid row
            col (int): Grid column
        """
        tool = self.ui_manager.get_active_tool()
        
        if tool == TOOL_NONE:
            return
        
        # Get the cell type to set
        cell_type_map = {
            TOOL_START: START,
            TOOL_END: END,
            TOOL_OBSTACLE: OBSTACLE,
            TOOL_FORBIDDEN: FORBIDDEN,
            TOOL_DIFFICULT: DIFFICULT
        }
        
        if tool in cell_type_map:
            # Clear previous start/end if placing new one
            if tool == TOOL_START:
                # Clear previous start
                if self.grid.start:
                    self.grid.set_cell(self.grid.start.row, self.grid.start.col, EMPTY)
            elif tool == TOOL_END:
                # Clear previous end
                if self.grid.end:
                    self.grid.set_cell(self.grid.end.row, self.grid.end.col, EMPTY)
            
            cell_type = cell_type_map[tool]
            self.grid.set_cell(row, col, cell_type)
            
            # Clear pathfinding visualization when grid changes
            self.visualizer.clear_pathfinding_visualization()
            self.path_found = False
    
    def run_pathfinding(self):
        """Execute the A* algorithm and visualize results."""
        if self.grid.start is None or self.grid.end is None:
            print("Error: Please set both start and end points!")
            return
        
        # Run A* algorithm
        path, cost, explored_count = self.astar.find_path(self.grid.start, self.grid.end)
        
        # Store results
        self.last_cost = cost
        self.last_explored_count = explored_count
        
        if path:
            self.path_found = True
            print(f"Path found! Cost: {cost:.1f}, Explored: {explored_count} nodes")
        else:
            self.path_found = False
            print("No path found!")
        
        # Set visualization data
        explored = self.astar.get_explored_nodes()
        self.visualizer.set_pathfinding_data(explored, path)
    
    def clear_grid(self):
        """Clear the grid back to empty state."""
        self.grid.clear()
        self.visualizer.clear_pathfinding_visualization()
        self.path_found = False
        self.ui_manager.set_active_tool(TOOL_NONE)
    
    def generate_random_map(self):
        """Generate a random map with obstacles and zones."""
        self.grid.generate_random_map(
            obstacle_density=0.15,
            forbidden_density=0.10,
            difficult_density=0.12
        )
        self.visualizer.clear_pathfinding_visualization()
        self.path_found = False
        print("Random map generated!")
    
    def update(self):
        """Update application state."""
        self.visualizer.update_animation()
    
    def render(self):
        """Render everything to the screen."""
        try:
            # Clear screen with background color
            self.screen.fill((230, 235, 240))
            
            # Draw grid and cells
            self.visualizer.draw_all()
            
            # Draw UI
            self.ui_manager.draw(self.screen)
            
            # Draw results if path was found
            if self.path_found:
                self.ui_manager.draw_results(self.screen, self.last_cost, self.last_explored_count)
            
            # Update display
            pygame.display.flip()
        except Exception as e:
            print(f"Error during rendering: {e}")
            # Continue running despite render errors
    
    def run(self):
        """Main application loop."""
        print("=" * 60)
        print("Drone Delivery Pathfinder - A* Algorithm Simulator")
        print("=" * 60)
        print("\nInstructions:")
        print("1. Select a tool button (Set Start, Set End, etc.)")
        print("2. Click on the grid to place elements")
        print("3. Click 'Run A*' to find the optimal path")
        print("4. Results will show energy cost and explored nodes")
        print("\nCell Types:")
        print("- White: Empty (cost = 1)")
        print("- Black: Obstacle (blocked)")
        print("- Red: Forbidden zone (blocked)")
        print("- Orange: Difficult zone (cost = 3)")
        print("- Green: Start point")
        print("- Blue: End point")
        print("- Yellow: Explored nodes")
        print("- Purple: Final path")
        print("\n" + "=" * 60 + "\n")
        
        try:
            while self.running:
                try:
                    self.handle_events()
                    self.update()
                    self.render()
                    self.clock.tick(self.fps)
                except Exception as e:
                    print(f"Error in game loop: {e}")
                    import traceback
                    traceback.print_exc()
                    # Continue running instead of crashing
        except KeyboardInterrupt:
            print("\nApplication closed by user")
        finally:
            pygame.quit()
            sys.exit()


def main():
    """Entry point for the application."""
    app = DronePathfinderApp()
    app.run()


if __name__ == '__main__':
    main()
