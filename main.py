import pygame
import sys
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, grid_width, grid_height,
    EMPTY, OBSTACLE, FORBIDDEN, DIFFICULT, START, END,
    TOOL_NONE, TOOL_START, TOOL_END, TOOL_OBSTACLE,
    TOOL_FORBIDDEN, TOOL_DIFFICULT
)
from grid import Grid
from astar import AStar
from ui import UIManager
from visualization import Visualizer

class DronePathfinderApp:
    # initialiser app
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Drone Delivery Pathfinder (A* Algorithm)")

        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = FPS

        self.grid = Grid(grid_width, grid_height)
        self.astar = AStar(self.grid)
        self.ui_manager = UIManager()
        self.visualizer = Visualizer(self.screen, self.grid)

        self.path_found = False
        self.last_cost = 0
        self.last_explored_count = 0

    # traiter les evenements
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            action, data = self.ui_manager.handle_event(event, self.grid, self.astar)

            if action == 'run_astar':
                self.run_pathfinding()
            elif action == 'clear_grid':
                self.clear_grid()
            elif action == 'random_map':
                self.generate_random_map()
            elif action == 'set_tool':
                pass 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    row, col = self.visualizer.get_cell_from_screen_pos(event.pos)
                    print(row,col)
                    if row is not None and col is not None:
                        self.handle_grid_click(row, col)
    
    # gerer clic sur grille
    def handle_grid_click(self, row, col):
        tool = self.ui_manager.get_active_tool()

        if tool == TOOL_NONE:
            return
        
        cell_type_map = {
            TOOL_START: START,
            TOOL_END: END,
            TOOL_OBSTACLE: OBSTACLE,
            TOOL_FORBIDDEN: FORBIDDEN,
            TOOL_DIFFICULT: DIFFICULT
        }

        row = int(row)
        col = int(col)
        if tool in cell_type_map:
            if tool == TOOL_START:
                if self.grid.start:
                    self.grid.set_cell(self.grid.start.row, self.grid.start.col, EMPTY)
            elif tool == TOOL_END:
                if self.grid.end:
                    self.grid.set_cell(self.grid.end.row, self.grid.end.col, EMPTY)

            cell_type = cell_type_map[tool]
            self.grid.set_cell(row, col, cell_type)
            
            self.visualizer.clear_pathfinding_visualization()
            self.path_found = False
    
    # executer algorithme astar
    def run_pathfinding(self):
        if self.grid.start is None or self.grid.end is None:
            print("Error: Please set both start and end points!")
            return
        
        path, cost, explored_count = self.astar.find_path(self.grid.start, self.grid.end)
        
        self.last_cost = cost
        self.last_explored_count = explored_count
        
        if path:
            self.path_found = True
            print(f"Path found! Cost: {cost:.1f}, Explored: {explored_count} nodes")
        else:
            self.path_found = False
            print("No path found!")
        
        explored = self.astar.get_explored_nodes()
        self.visualizer.set_pathfinding_data(explored, path)
    
    # effacer grille
    def clear_grid(self):
        self.grid.clear()
        self.visualizer.clear_pathfinding_visualization()
        self.path_found = False
        self.ui_manager.set_active_tool(TOOL_NONE)
    
    # generer carte aleatoire
    def generate_random_map(self):
        self.grid.generate_random_map(
            obstacle_density=0.15,
            forbidden_density=0.10,
            difficult_density=0.12
        )
        self.visualizer.clear_pathfinding_visualization()
        self.path_found = False
        print("Random map generated!")
    
    # mettre a jour etat du jeu
    def update(self, x, y):
        self.grid.refill(x, y)
        self.visualizer.update_animation()
    
    # afficher graphiques
    def render(self):
        try:
            self.screen.fill((230, 235, 240))
            
            self.visualizer.draw_all()
            self.ui_manager.draw(self.screen)
            
            if self.path_found and self.visualizer.has_drone_reached_destination():
                self.ui_manager.draw_results(self.screen, self.last_cost, self.last_explored_count)
            pygame.display.flip()
        except Exception as e:
            print(f"Error during rendering: {e}")
    
    # boucle principale du jeu
    def run(self):
        try:
            while self.running:
                try:
                    x,y = self.ui_manager.getDimensions()
                    
                    self.handle_events()
                    self.update(x,y)
                    self.render()
                    self.clock.tick(self.fps)
                except Exception as e:
                    print(f"Error in game loop: {e}")
        except KeyboardInterrupt:
            pass
        finally:
            pygame.quit()
            sys.exit()

# point d entree
def main():
    app = DronePathfinderApp()
    app.run()


if __name__ == '__main__':
    main()
