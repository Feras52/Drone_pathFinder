import pygame

from constants import (
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, BUTTON_FONT_SIZE,
    SIDEBAR_WIDTH, SIDEBAR_X, SCREEN_HEIGHT, grid_pixel_width,
    COLORS, TOOL_NONE, TOOL_START, TOOL_END, TOOL_OBSTACLE,
    TOOL_FORBIDDEN, TOOL_DIFFICULT, BUTTON_RADIUS
)

class NumSlider:
    # initialiser curseur
    def __init__(self, x, y, width, min_value, max_value, initial_value,text ="eee"):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.is_dragging = False
        self.text = text
        self.font = pygame.font.Font(None, 20)

    # gerer evenements curseur
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.update_value_from_pos(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.update_value_from_pos(event.pos[0])

    # mettre a jour valeur du curseur
    def update_value_from_pos(self, x):
        relative_x = max(0, min(x - self.rect.x, self.rect.width))
        self.value = self.min_value + (relative_x / self.rect.width) * (self.max_value - self.min_value)

    # dessiner curseur
    def draw(self, surface):
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.x, self.rect.y - 20))

        pygame.draw.rect(surface, (60, 60, 60), self.rect, border_radius=10)

        percent = (self.value - self.min_value) / (self.max_value - self.min_value)
        fill_width = int(self.rect.width * percent)

        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, (100, 180, 255), fill_rect, border_radius=10)

        knob_x = self.rect.x + fill_width
        knob_y = self.rect.centery
        knob_radius = self.rect.height // 2 + 2

        pygame.draw.circle(surface, (255, 255, 255), (knob_x, knob_y), knob_radius)

class Button:
    # initialiser bouton
    def __init__(self, x, y, width, height, text, tool_id=TOOL_NONE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.tool_id = tool_id
        self.is_hovered = False
        self.is_active = False

    # verifier si bouton survole
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    # dessiner bouton
    def draw(self, surface, font):
        if self.is_active:
            color = COLORS['button_active']
            text_color = (255, 255, 255)
        elif self.is_hovered:
            color = COLORS['button_hover']
            text_color = (44, 62, 80)
        else:
            color = COLORS['button']
            text_color = COLORS['button_text']

        shadow = self.rect.copy()
        shadow.x += 2
        shadow.y += 2
        pygame.draw.rect(surface, (200, 200, 200), shadow, border_radius=BUTTON_RADIUS)

        pygame.draw.rect(surface, color, self.rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(surface, (52, 152, 219) if self.is_active else (120, 120, 120), self.rect, 2, border_radius=BUTTON_RADIUS)

        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    # verifier si bouton clique
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class UIManager:
    # initialiser gestionnaire ui
    def __init__(self):
        self.buttons = []

        start_x = SIDEBAR_X + 10
        start_y = 40
        gap = BUTTON_HEIGHT + BUTTON_MARGIN
        
        self.xSliders = (NumSlider(start_x, start_y + 8 * gap + 20, BUTTON_WIDTH, 5, 100, 15,"grid x"))
        self.ySliders = (NumSlider(start_x, start_y + 8 * gap + 60, BUTTON_WIDTH, 5, 100, 15,"grid y"))
        self.active_tool = TOOL_NONE
        self.create_buttons()
 
        self.font_large = pygame.font.Font(None, BUTTON_FONT_SIZE + 2)
        self.font_small = pygame.font.Font(None, BUTTON_FONT_SIZE - 4)
        self.font_title = pygame.font.Font(None, BUTTON_FONT_SIZE + 8)

    # obtenir dimensions de grille
    def getDimensions(self):
        return max(5,int(self.xSliders.value)), max(5,int(self.ySliders.value))

    # creer tous les boutons
    def create_buttons(self):
        start_x = SIDEBAR_X + 10
        start_y = 40
        gap = BUTTON_HEIGHT + BUTTON_MARGIN

        buttons = [
            ("Set Start", TOOL_START),
            ("Set End", TOOL_END),
            ("Add Obstacle", TOOL_OBSTACLE),
            ("Forbidden Zone", TOOL_FORBIDDEN),
            ("Difficult Zone", TOOL_DIFFICULT),
            ("Run A*", -1),
            ("Clear Grid", -2),
            ("Random Map", -3),
        ]

        for index, (label, tool_id) in enumerate(buttons):
            y = start_y + index * gap
            self.buttons.append(Button(start_x, y, BUTTON_WIDTH, BUTTON_HEIGHT, label, tool_id))

    # gerer evenements ui
    def handle_event(self, event, grid, astar):

        self.xSliders.handle_event(event)
        self.ySliders.handle_event(event)
        
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_clicked(event.pos):
                    if button.tool_id == -1:
                        return 'run_astar', None
                    if button.tool_id == -2:
                        return 'clear_grid', None
                    if button.tool_id == -3:
                        return 'random_map', None
                    self.set_active_tool(button.tool_id)
                    return 'set_tool', button.tool_id

        return None, None

    # definir outil actif
    def set_active_tool(self, tool_id):
        self.active_tool = tool_id
        for button in self.buttons:
            button.is_active = button.tool_id == tool_id

    # obtenir outil actif
    def get_active_tool(self):
        return self.active_tool

    # dessiner ui
    def draw(self, surface):
        sidebar_rect = pygame.Rect(SIDEBAR_X - 20, 0, SIDEBAR_WIDTH + 40, SCREEN_HEIGHT)
        pygame.draw.rect(surface, COLORS['sidebar_bg'], sidebar_rect)

        pygame.draw.line(surface, (180, 180, 180), (SIDEBAR_X - 20, 0), (SIDEBAR_X - 20, SCREEN_HEIGHT), 2)
        pygame.draw.rect(surface, (220, 220, 220), (SIDEBAR_X - 18, 0, SIDEBAR_WIDTH + 36, SCREEN_HEIGHT), 2, border_radius=20)

        for button in self.buttons:
            button.draw(surface, self.font_large)
        
        self.xSliders.draw(surface)
        self.ySliders.draw(surface)

        self.draw_info_panel(surface)

    # dessiner panneau info
    def draw_info_panel(self, surface):
        x = SIDEBAR_X + 10
        y = 610

        guide_font = pygame.font.Font(None, 14)
        
        title = self.font_title.render("Quick Guide", True, (44, 62, 80))
        surface.blit(title, (x, y))

        y += 32
        
        lines = [
            "1. Select a tool",
            "2. Click on grid",
            "3. Click Run A*",
            "",
            "Colors:",
            "White - Unexplored",
            "Wall - Obstacle",
            "Military Base - Forbidden",
            "Yellow - Explored",
            "Purple - Path",
        ]

        list_x = x
        list_y = y
        for line in lines:
            if line == "":
                list_y += 8
                continue
            text = guide_font.render(line, True, (50, 50, 50))
            surface.blit(text, (list_x, list_y))
            list_y += 22

    # afficher resultats
    def draw_results(self, surface, path_cost, explored_count):
        from constants import SCREEN_WIDTH, SCREEN_HEIGHT
        
        box_width = BUTTON_WIDTH
        box_height = 110
        x = (SCREEN_WIDTH - box_width) // 2
        y = (SCREEN_HEIGHT - box_height) // 2

        box = pygame.Rect(x - 10, y - 10, box_width, box_height)
        pygame.draw.rect(surface, (46, 204, 113), box, border_radius=12)
        pygame.draw.rect(surface, (39, 174, 96), box, 2, border_radius=12)

        title = self.font_large.render("A* Results", True, (255, 255, 255))
        title_rect = title.get_rect(center=(x + box_width // 2, y + 5))
        surface.blit(title, title_rect)

        y += 36
        cost_text = self.font_large.render(f"Cost: {path_cost:.1f}", True, (255, 255, 255))
        cost_rect = cost_text.get_rect(center=(x + box_width // 2, y))
        surface.blit(cost_text, cost_rect)

        y += 30
        nodes_text = self.font_large.render(f"Nodes: {explored_count}", True, (255, 255, 255))
        nodes_rect = nodes_text.get_rect(center=(x + box_width // 2, y))
        surface.blit(nodes_text, nodes_rect)