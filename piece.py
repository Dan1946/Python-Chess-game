import pygame
import os
from algo import dfs_movement, dfs_movement_king

b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))

for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))


class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.attack_moves = []
        self.moves = []
        self.first = False
        self.diag_assualt = []
        self.protected_pos = []
        self.detect_k = False
        self.include_k_m = []
        self.possible_opp_block_or_attk = {}
        self.direction = []

        self.king = False
        self.pawn = False
        self.rook = False
        self.bishop = False
        self.queen = False
        self.knight = False

        x = (4 - self.col) + round(self.startX + (self.col * self.rect[2] / 8))
        y = 3 + round(self.startY + (self.row * self.rect[3] / 8))
        self.rect_i = pygame.Rect(x, y, 50, 50)
        self.x = self.rect_i.x
        self.y = self.rect_i.y
        # self.rect.x, self.rect.y = self.startX, self.startY

    def isSelected(self, mouse_pos):
        if self.rect_i.collidepoint(mouse_pos):
            self.selected = True
        # else:
        #     self.selected = False
            
        return self.selected
    

    def update_valid_moves(self, bo):
        self.move_list = self.valid_moves(bo)

    def get_pos(self):
        return self.row, self.col

    def draw(self, win, color):
        if self.color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        x = (4 - self.col) + round(self.startX + (self.col * self.rect[2] / 8))
        y = 3 + round(self.startY + (self.row * self.rect[3] / 8))

        # self.rect_i.x = x
        # self.rect_i.y = y

        self.x = self.rect_i.x
        self.y = self.rect_i.y

        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        win.blit(drawThis, (self.x, self.y))
        # pygame.draw.rect(win, "red", self.rect_i)
        # pygame.display.update()

        '''if self.selected and self.color == color:  # Remove false to draw dots
            moves = self.move_list

            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                pygame.draw.circle(win, (255, 0, 0), (x, y), 10)'''

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]
    
    def valid_moves(self, bo):

        self.attack_moves = []
        self.move_list = []
        self.diag_assualt = []
        self.protected_pos = []
        self.possible_opp_block_or_attk.clear()

        valid_moves = dfs_movement(self, bo)
        board = bo.board

        for move in valid_moves:
            i, j = move
            if board[i][j] != 0:
                if board[i][j].color == self.color:
                    valid_moves.remove(move)
                else:
                    self.attack_moves.append(move)
        
        if self.pawn and len(self.attack_moves):
            valid_moves.extend(self.attack_moves)
        
        # self.move_list.extend(valid_moves)
        self.moves = valid_moves

        if bo.check:
            self.check_for_block_and_attack_move(bo, valid_moves)


        return valid_moves
    

    def animate_piece_movement(self, destination, win, redraw, bo):
        # Set up the screen
        clock = pygame.time.Clock()

        # Define movement speed
        speed = 30

        while True:
            # Calculate movement vector
            dx = destination[0] - self.rect_i.x
            dy = destination[1] - self.rect_i.y

            # Calculate distance to destination
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance <= speed:
                # If distance is small enough, set position to destination
                self.rect_i.x, self.rect_i.y = destination
                break

            # Normalize movement vector
            dx /= distance
            dy /= distance

            # Move the piece
            self.rect_i.x += dx * speed
            self.rect_i.y += dy * speed

            # Draw the updated position
            redraw(win, bo)
            # pygame.draw.circle(win, (255, 0, 0), (int(piece.x), int(piece.y)), 20)
            pygame.display.flip()

            # Control the frame rate
            clock.tick(60)

        # bo.last = self
    
    def check_for_block_and_attack_move(self, bo, valid_moves):
        opp_pieces = bo.get_opp_pieces(self.color)

        for opp in opp_pieces:
            moves = opp.move_list
            lst = []
            for move in moves:
                if (move in self.direction or move == (self.row, self.col)) and (not (self.pawn or self.knight or opp.king)):
                    lst.append(move)
                    self.possible_opp_block_or_attk[opp] = lst

                elif move == (self.row, self.col) and not(opp.king):
                    lst.append(move)
                    self.possible_opp_block_or_attk[opp] = lst

    

    def __str__(self):
        return str(self.row) + " " + str(self.col)


class Bishop(Piece):
    img = 0
    directions = ["up-l-d", "down-l-d", "up-r-d", "down-r-d"]

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.bishop = True
        self.square_symbol = "B" if self.color == "w" else "b"


class King(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True
        self.first = True
        self.castle = False
        self.king_moves = []
        self.left = []
        self.right = []
        self.square_symbol = "K" if self.color == "w" else "k"
        # self.detected = False

    def valid_moves(self, bo):
        self.attack_moves = []
        self.moves = []
        self.king_moves.clear()
        # self.include_k_m.clear()

        valid_moves = dfs_movement(self, bo)
        enemy_moves = []
        board = bo.board
        
        self.prevent_kings_meet(bo, valid_moves)
        self.check_for_block(bo)

        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    if board[i][j].color != self.color:
                        opp_piece = board[i][j]
                        # print(f"{opp_piece}:{opp_piece.move_list}")
                        
                        if opp_piece.pawn:
                            enemy_moves.extend(opp_piece.diag_assualt)
                            enemy_moves.extend(opp_piece.protected_pos)

                            # print(f"p {opp_piece}:{opp_piece.diag_assualt}")
                        
                        else:
                            enemy_moves.extend(opp_piece.move_list)
                            enemy_moves.extend(opp_piece.protected_pos)
                            # print(f"p {opp_piece}:{opp_piece.move_list}")
                        
        # print(enemy_moves, "enme")
        for move in valid_moves[:]:
            i, j = move
            if move in enemy_moves:
                print("remove")
                valid_moves.remove(move)
            
            if move in self.include_k_m and self.detected and move in valid_moves:
                print(self.include_k_m, "worked")
                self.detected = False
                valid_moves.remove(move)
                # self.include_k_m.clear()
            
            if board[i][j] != 0:
                if board[i][j].color != self.color and move in valid_moves:
                    self.attack_moves.append(move)

            
        if not(len(valid_moves)):
            bo.stalemate = True
        
        # self.move_list.extend(valid_moves)
        self.move = valid_moves
        
        
        return valid_moves
    
    def prevent_kings_meet(self, bo, valid_moves):
        opp_pieces = bo.get_opp_pieces(self.color)
        for opp in opp_pieces:
            if opp.king:
                for move in opp.king_moves:
                    if move in valid_moves:
                        valid_moves.remove(move)

    
    def check_for_block(self, bo):
        direction_moves = dfs_movement_king(self, bo)
        first_piece = None
        second_piece = None
        block  = False
        direc_pieces = {d: [first_piece, second_piece] for d in direction_moves}
        path = []
        bo.path.clear()

        if bo.turn == self.color:
            if len(bo.prevent_block):
                bo.prevent_block.clear()
            
            if len(bo.invalid_lst):
                bo.invalid_lst.clear()


            for direc in direction_moves:
                piece_count = 0
                for move in direction_moves[direc]:
                    i, j = move
                    piece = bo.board[i][j]
                    if piece != 0:
                        if piece.color == self.color and direc_pieces[direc][0] is None:
                            direc_pieces[direc][0] = piece
                        
                        if direc_pieces[direc][0] is not None and piece.color == self.color:
                            piece_count += 1
                        
                        
                        if (piece.rook or piece.queen or piece.bishop) and piece.color != self.color and piece_count == 1:
                            if direc in piece.directions and (direc_pieces[direc][1] is None) and (direc_pieces[direc][0] is not None):
                                direc_pieces[direc][1] = piece
                                path.append(direction_moves[direc])
                                bo.path.append(direction_moves[direc])
            

            for direction in direc_pieces:
                if direc_pieces[direction][0] != None and direc_pieces[direction][1] != None:
                    bo.prevent_block.append(direc_pieces[direction][0])
                    bo.invalid_lst.append(direc_pieces[direction][0])
            
            # if self.color == "w":
            #     color = "b"
            
            # else:
            #     color = "w"

            # for piece in bo.prevent_block[:]:
            #     for move in piece.move_list[:]:
            #             for direc in path:
            #                 if move not in direc and move in piece.move_list:
            #                     piece.move_list.remove(move)
            #                     print(move, "removed....")
                
            #     if len(piece.move_list):
            #         bo.prevent_block.remove(piece)
                
         
            print(bo.prevent_block)
            print(bo.invalid_lst)



class Knight(Piece):
    img = 2


    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.knight = True
        self.square_symbol = "N" if self.color == "w" else "n"

    def valid_moves(self, bo):
        self.attack_moves = []
        self.move_list = []
        self.protected_pos.clear()
        self.possible_opp_block_or_attk.clear()

        valid_moves  = self.get_knight_moves(bo)

        if bo.check:
            self.check_for_block_and_attack_move(bo, valid_moves)

        return valid_moves
    
    # Function to get all possible moves of a knight from a given position (x, y) following normal chess movement rules
    def get_knight_moves(self, bo):
        x, y = self.row, self.col
        board = bo.board

        possible_moves = [
            (x + 1, y + 2), (x + 2, y + 1),
            (x + 2, y - 1), (x + 1, y - 2),
            (x - 1, y - 2), (x - 2, y - 1),
            (x - 2, y + 1), (x - 1, y + 2)
        ]
        
        # Filter out moves that are out of bounds (outside the 8x8 chessboard)
        valid_moves = [(new_x, new_y) for new_x, new_y in possible_moves if 0 <= new_x < 8 and 0 <= new_y < 8]

        for move in valid_moves[:]:
            i, j = move
            if board[i][j] != 0:
                if board[i][j].color == self.color:
                    self.protected_pos.append(move)
                    valid_moves.remove(move)
                else:
                    self.attack_moves.append(move)

        self.move_list.extend(valid_moves)
        # print(f"{self}:{self.protected_pos}", "proct")


        
        return valid_moves


class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False
        self.pawn = True
        self.square_symbol = "P" if self.color == "w" else "p"
        self.promoted = "-"


class Queen(Piece):
    img = 4
    directions = ["up", "down", "left", "right", "up-l-d", "down-l-d", "up-r-d", "down-r-d"]


    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.queen = True
        self.square_symbol = "Q" if self.color == "w" else "q"


class Rook(Piece):
    img = 5 
    directions = ["up", "down", "left", "right"]

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.rook = True
        self.first = True
        self.castle = False
        self.square_symbol = "R" if self.color == "w" else "r"
