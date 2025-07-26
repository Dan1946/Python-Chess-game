import pygame


class Tile:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BROWN = (107, 62, 38)
    CREAM = (253, 245, 201)
    rect_d = (113, 113, 525, 525)



    def __init__(self, x, y, width, height, grid_pos):
        self.rect = pygame.Rect(x, y, width, height) #dimensions for the rectangle
        self.grid_position = grid_pos
        self.selected = False
        self.safe = False
        self.special = False
        self.highlight = False
        self.color = self.CREAM if (grid_pos[0] + grid_pos[1]) % 2 == 0 else self.BROWN
        self.special_tile_color = None
        self.special_tile_circle_color = "white"
        self.highlight_color =    (70, 95, 150) #(200, 80, 80) # brown
        self.highlight_attack = False
        self.attack_color = (210, 180, 90) # yellow
        self.hint_color = (70, 95, 150)  #"blue"
        self.hint_highlight = False

    def draw(self, win):
        radius = 5
        if self.highlight:
            pygame.draw.rect(win, self.color, self.rect)
            pygame.draw.circle(win, self.highlight_color, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), radius)

        else:
             pygame.draw.rect(win, self.color, self.rect)
        
        if self.highlight_attack:
            pygame.draw.rect(win, self.attack_color, self.rect)
        
        if self.hint_highlight:
            pygame.draw.rect(win, self.hint_color, self.rect)


    
    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected
    
    def toggle_highlight(self, toggle=True, toggle_hint = True):
        if toggle:
            self.highlight = not self.highlight
        
        if toggle_hint:
            self.hint_highlight = not self.hint_highlight
    
    def attack_highlight(self, toggle = True):
        if toggle:
            self.highlight_attack = not self.highlight_attack

    
    def reset_color(self):
        self.color = self.CREAM if (self.grid_position[0] + self.grid_position[1]) % 2 == 0 else self.BROWN