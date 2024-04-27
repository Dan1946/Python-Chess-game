import pygame


class Tile:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    rect_d = (113, 113, 525, 525)



    def __init__(self, x, y, width, height, grid_pos):
        self.rect = pygame.Rect(x, y, width, height) #dimensions for the rectangle
        self.grid_position = grid_pos
        self.selected = False
        self.safe = False
        self.special = False
        self.highlight = False
        self.color = "white" if (grid_pos[0] + grid_pos[1]) % 2 == 0 else "green"
        self.special_tile_color = None
        self.special_tile_circle_color = "white"
        self.highlight_color = "brown"
        self.highlight_attack = False
        self.attack_color = "yellow"

    def draw(self, win):
        radius = 5
        if self.highlight:
            pygame.draw.rect(win, self.color, self.rect)
            pygame.draw.circle(win, "brown", (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), radius)

        else:
             pygame.draw.rect(win, self.color, self.rect)
        
        if self.highlight_attack:
            pygame.draw.rect(win, self.attack_color, self.rect)

    
    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected
    
    def toggle_highlight(self, toggle=True):
        if toggle:
            self.highlight = not self.highlight
    
    def attack_highlight(self, toggle = True):
        if toggle:
            self.highlight_attack = not self.highlight_attack

    
    def reset_color(self):
        self.color = "white" if (self.grid_position[0] + self.grid_position[1]) % 2 == 0 else "green"