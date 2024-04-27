from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight
from piece import Piece
from Tiles import Tile
from copy import deepcopy
import time
import pygame
import os
pygame.mixer.init()


piece_capture = pygame.USEREVENT + 1
piece_capture_sound = pygame.mixer.Sound(os.path.join("sound", "capture.mp3"))

piece_movement = pygame.USEREVENT + 2
piece_movement_sound = pygame.mixer.Sound(os.path.join("sound", "move-self.mp3"))

move_check = pygame.USEREVENT + 3
move_check_sound = pygame.mixer.Sound(os.path.join("sound", "move-check.mp3"))

promote = pygame.USEREVENT + 4
promote_sound = pygame.mixer.Sound(os.path.join("sound", "promote.mp3"))

game_start = pygame.USEREVENT + 5
game_start_sound = pygame.mixer.Sound(os.path.join("sound", "game-start.mp3"))

game_end = pygame.USEREVENT + 6
game_end_sound = pygame.mixer.Sound(os.path.join("sound", "game-end.mp3"))



class Board:
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.ready = True

        self.last = None
        

        self.lst_tiles = {}
        self.checking_piece = None
        self.checked_king = None
        self.prevent_block = []

        self.copy = True

        self.block_check = []
        self.invalid_lst = []
        self.valid_piece_pos = []
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.promoted = "-"
        self.check_count = 0

        self.board = [[0 for x in range(8)] for _ in range(rows)]

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"
        self.kings = [self.board[7][4], self.board[0][4]]
        self.path = []

        self.turn = "w"
        self.check = False

        self.time1 = 900
        self.time2 = 900

        self.storedTime1 = 0
        self.storedTime2 = 0

        self.winner = None
        self.stalement = False

        self.startTime = time.time()
        self.create_tiles()

    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self)

    def draw(self, win, color):
        if self.last and color == self.turn:
            y, x = self.last[0]
            y1, x1 = self.last[1]

            xx = (4 - x) +round(self.startX + (x * self.rect[2] / 8))
            yy = 3 + round(self.startY + (y * self.rect[3] / 8))
            pygame.draw.circle(win, (0,0,255), (xx+32, yy+30), 34, 4)
            xx1 = (4 - x) + round(self.startX + (x1 * self.rect[2] / 8))
            yy1 = 3+ round(self.startY + (y1 * self.rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

        s = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, color)
                    if self.board[i][j].isSelected:
                        s = (i, j)


    def get_danger_moves(self, color):
        danger_moves = {}
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        piece = self.board[i][j]

                        if not(piece.pawn):
                                danger_moves[piece] = piece.move_list
                        
                        else:
                            danger_moves[piece] = piece.attack_moves
                        

        return danger_moves
    
    def move_self(self):
        return piece_movement, piece_movement_sound
    
    def promote(self):
        return promote, promote_sound
    
    def move_check(self):
        return move_check, move_check_sound
    
    def move_capture(self):
        return piece_capture, piece_capture_sound
    
    def game_start(self):
        return game_start, game_start_sound
    
    def game_end(self):
        return game_end, game_end_sound
    
    def post_move_self(self):
        pygame.event.post(pygame.event.Event(piece_movement))
    
    def post_move_capture(self):
        pygame.event.post(pygame.event.Event(piece_capture))
    
    def post_move_check(self):
        pygame.event.post(pygame.event.Event(move_check))
    
    def post_promote(self):
        pygame.event.post(pygame.event.Event(promote))
    
    def post_start(self):
        pygame.event.post(pygame.event.Event(game_start))
    
    def post_end(self):
        pygame.event.post(pygame.event.Event(game_end))
    

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and self.board[i][j].color == color:
                        self.checked_king = self.board[i][j]
                        king_pos = (i, j)

        for piece in danger_moves:
            if king_pos in danger_moves[piece]:
                self.check = True
                self.checking_piece = piece
                self.post_move_check()
                break
        
        else:
            self.check = False


    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i, j)

        # if piece
        if self.board[row][col] == 0 and prev!=(-1,-1):
            moves = self.board[prev[0]][prev[1]].move_list
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)

        else:
            if prev == (-1,-1):
                self.reset_selected()
                if self.board[row][col] != 0:
                    self.board[row][col].selected = True
            else:
                if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                    moves = self.board[prev[0]][prev[1]].move_list
                    if (col, row) in moves:
                        changed = self.move(prev, (row, col), color)

                    if self.board[row][col].color == color:
                        self.board[row][col].selected = True

                else:
                    if self.board[row][col].color == color:
                        #castling
                        self.reset_selected()
                        if self.board[prev[0]][prev[1]].selected == False and self.board[prev[0]][prev[1]].rook and self.board[row][col].king and col != prev[1] and prev!=(-1,-1):
                            castle = True
                            if prev[1] < col:
                                for j in range(prev[1]+1, col):
                                    if self.board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 3), color)
                                    changed = self.move((row,col), (row, 2), color)
                                if not changed:
                                    self.board[row][col].selected = True

                            else:
                                for j in range(col+1,prev[1]):
                                    if self.board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 6), color)
                                    changed = self.move((row,col), (row, 5), color)
                                if not changed:
                                    self.board[row][col].selected = True
                            
                        else:
                            self.board[row][col].selected = True

        if changed:
            if self.turn == "w":
                self.turn = "b"
                self.reset_selected()
            else:
                self.turn = "w"
                self.reset_selected()

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        '''if self.is_checked(color):
            king = None
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] != 0:
                        if self.board[i][j].king and self.board[i][j].color == color:
                            king = self.board[i][j]
            if king is not None:
                valid_moves = king.valid_moves(self.board)

                danger_moves = self.get_danger_moves(color)

                danger_count = 0

                for move in valid_moves:
                    if move in danger_moves:
                        danger_count += 1
                return danger_count == len(valid_moves)'''

        return False
    

    def get_opp_pieces(self, color):
        opp_pieces = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        piece = self.board[i][j]
                        
                        if len(piece.move_list):
                            opp_pieces.append(piece)
        
        return opp_pieces

        

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self.board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            changed = False
            nBoard = self.board[:]
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        else:
            self.reset_selected()

        self.update_moves()
        if changed:
            self.last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed
    
    
    def create_tiles(self):
        padding = 750 // 6.3   # 12, 6.4 Adjust padding as desired
        square_size = (750 - padding * 2) // 8 # 8

        for row in range(self.rows):
            for col in range(self.cols):
                pos = row, col
                tile = Tile(padding + col * square_size, padding + row * square_size, square_size, square_size, pos)
                self.lst_tiles[pos] = tile

    
    def get_safe_moves(self, color):
        safe_moves = {}
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == color:
                        piece = self.board[i][j] 

                        if not(piece.pawn) and len(piece.move_list):
                                 safe_moves[piece] = piece.move_list
                        
                        elif piece.pawn and (len(piece.move_list)):
                            safe_moves[piece] = piece.move_list
        
        return safe_moves
    

    def get_pawns(self):
        pawns = []

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == self.turn and self.board[i][j].pawn:
                        piece = self.board[i][j] 
                        pawns.append(piece)
        
        return pawns


    def king_trapped(self):
        moves = self.checked_king.move_list
        if self.check and not(len(moves)):
            return True
        
        return False
    
    def castle(self, piece, pos):
        castle = True if piece.first and not(self.check) else False
        rook = None
    
        if piece.color == "w":
            positions= []
            r = self.board[7]

            for i in range(len(r)):
                p = (7, i)
                positions.append(p)
            
            left = positions[:4]
            right = positions[5:]

        
        else:
            r = self.board[0]
            positions = []
           
            for i in range(len(r)):
                p = (0, i)
                positions.append(p)

            left = positions[:4]
            right = positions[5:]

        if piece.first and not(self.check) and piece.king:
            opp_pieces = self.get_opp_pieces(piece.color)
            print(left, 'left')
            print(right, 'right')
            if pos in left:
                for opp in opp_pieces:
                    for move in left:
                        if move in opp.move_list:
                            castle = False
                            break
            
            elif pos in right:
                for opp in opp_pieces:
                    for move in right:
                        if move in opp.move_list:
                            castle = False
                            break

            
            if pos in right[1:] and castle:
                row, col = right[-1]
                if True:
                    new_row, new_col = right[-1]
                    value = self.board[new_row][new_col]

                    if value != 0:
                        if value.rook and value.first:
                            i, j = pos
                           
                            self.board[i][j] = piece
                            x, y = piece.get_pos()
                            self.board[x][y] = 0
                            piece.change_pos(pos)

                            a, b = right[0]
                            self.board[a][b] = value
                            m, n = value.get_pos()
                            self.board[m][n] = 0
                            value.change_pos((a, b))
                            rook = value


            elif pos in left[:3] and castle:
                row, col = left[-1]
                if True:
                    new_row, new_col = left[0]
                    value = self.board[new_row][new_col]

                    if value != 0:
                        if value.rook and value.first:
                            i, j = pos
                            
                            self.board[i][j] = piece
                            x, y = piece.get_pos()
                            self.board[x][y] = 0
                            piece.change_pos(pos)

                            a, b = left[2]
                            self.board[a][b] = value
                            m, n = value.get_pos()
                            self.board[m][n] = 0
                            value.change_pos((a, b))
                            rook = value

        return rook



    def promotion(self, piece):

        if piece.pawn:

            if piece.color == "w":
                positions = []
           
                for i in range(8):
                    p = (0, i)
                    positions.append(p)

            else:
                positions = []
           
                for i in range(8):
                    p = (7, i)
                    positions.append(p)
            
            row, col = piece.get_pos()

            if (row, col) in positions:

                while True:
                    inp = input("promote to which piece? ")
                    
                    if inp.lower() == "r":
                        self.board[row][col] = Rook(row, col, piece.color)
                        break
                    
                    elif inp.lower() == "q":
                        self.board[row][col] = Queen(row, col, piece.color)
                        break
                    
                    elif inp.lower() == "b":
                        self.board[row][col] = Bishop(row, col, piece.color)
                        break
                    
                    elif inp.lower() == "k":
                        self.board[row][col] = Knight(row, col, piece.color)
                        break
                
                self.post_promote()
    

    def ai_promotion(self, piece = None):
         pawns = self.get_pawns()

         for pawn in pawns:
             a, b= pawn.get_pos()
             if self.turn == "w" and a == 1:
                 if len(pawn.attack_moves) or self.board[a - 1][b] == 0:
                     pawn.promoted = "Q" if self.turn == "w" else ""
                 
             elif self.turn == "b" and a == 6:
                 if len(pawn.attack_moves) or self.board[a + 1][b] == 0:
                     pawn.promoted = "Q" if self.turn == "w" else "q"

         if piece is not None:
            if piece.pawn:

                if piece.color == "w":
                    positions = []
            
                    for i in range(8):
                        p = (0, i)
                        positions.append(p)

                else:
                    positions = []
            
                    for i in range(8):
                        p = (7, i)
                        positions.append(p)
                
                row, col = piece.get_pos()

                if (row, col) in positions:            
                    self.board[row][col] = Queen(row, col, piece.color)




    async def simulate_move(self, piece, move, redraw_gameWindow = None, win = None):
        moved = False
        piece_moved = None
        invalid = False


        tile = self.lst_tiles[move]
        i, j = move
        p = self.board[i][j]

        if isinstance(piece, int):
            piece = Queen(i, j, self.turn)
            pygame.event.post(pygame.event.Event(promote))


        if isinstance(p, Piece):
            invalid = p.color == piece.color

            if not(invalid):
                pygame.event.post(pygame.event.Event(piece_capture))
        
        elif p == 0:
            invalid = False

            # if invalid:
            #     continue
        # print(invalid)
        print(p)
        # print(bo.board)
        if not(invalid):

            # piece.rect_i.x = tile.rect.x
            # piece.rect_i.y = tile.rect.y
            destination = [tile.rect.x, tile.rect.y]

        
            # rook = self.castle(piece, move)
            rook = None
            # print(rook)
            
            if rook is not None:
                pos = rook.get_pos()
                til = self.lst_tiles[pos]
                des = [til.rect.x, til.rect.y]
                print("castle")

                if redraw_gameWindow != None:
                    piece.animate_piece_movement(destination, win, redraw_gameWindow, self)
                    rook.animate_piece_movement(des, win, redraw_gameWindow, self)

            if rook is None:
                if redraw_gameWindow != None:
                    piece.animate_piece_movement(destination, win, redraw_gameWindow, self)

                    if isinstance(p, int):
                        pygame.event.post(pygame.event.Event(piece_movement))


            if p == 0 and not(piece.pawn):
                self.halfmove_clock += 1
                
            else:
                self.halfmove_clock = 0


            if piece.color == "b":
                self.fullmove_number += 1

            
            if rook is None:
                self.board[i][j] = piece
                a, b = piece.row, piece.col
                self.board[a][b] = 0
                piece.change_pos(move)

                self.ai_promotion(piece)
            
            # if self.check and self.check_count == 0:
            #     pygame.event.post(pygame.event.Event(move_check))
            #     self.check_count += 1
            
            # elif not(self.check):
            #     self.check_count = 0


            piece_moved = piece
            moved = True


        if moved:
            # del piece_to_move[piece_moved]
            piece.first = False
        
        return moved



    def handle_player_pieces(self, color):
        piece_to_move = {}

        for pi in self.prevent_block[:]:
            for move in pi.move_list[:]:
                    for direc in self.path:
                        if move not in direc and move in pi.move_list:
                            pi.move_list.remove(move)
                            print(move, "removed....")
            
            if len(pi.move_list):
                self.prevent_block.remove(pi)


        for i in range(8):
                for j in range(8):
                    if self.board[i][j] != 0:
                        # print()
                        if self.board[i][j].color == color:
                            piece = self.board[i][j]
                            attack_moves = piece.attack_moves
                            valid_moves = piece.move_list

                            print(valid_moves)
                            pos = piece.get_pos()

                
                            if piece in self.prevent_block:
                                piece.selected = False
                                break

                            if self.check and not(piece.king):
                                piece.selected = False
                                continue
                            
                            if not(self.check) or piece.king and len(valid_moves):
                                piece_to_move[piece] = valid_moves
                                # set_piece_to_move(piece, piece_to_move, valid_moves, attack_moves, invalid_move)

                            
                            # elif  pos in bo.valid_piece_pos and bo.check or (pos in invalid):
                            #     set_piece_to_move(p, piece_to_move, only_moves[piece], [], invalid_move)
        
        
        if self.check:
            checking = self.checking_piece
            print(checking)
            piece_attk_or_block = checking.possible_opp_block_or_attk
            print(piece_attk_or_block)

            for p in self.invalid_lst:
                    if p in piece_attk_or_block:
                        del piece_attk_or_block[p]


            for piece in piece_attk_or_block:
                if piece not in self.invalid_lst:
                    piece_to_move[piece] = piece_attk_or_block[piece]
                        # set_piece_to_move(piece, piece_to_move, piece_attk_or_block[piece], [], invalid_move)
        
        return piece_to_move
    


    def get_piece(self, row, col):
            return self.board[row][col]
        

                    

        
    # def simulate_move(self, color, pos = None):
    #     only_moves = {}
    #     invalid_pieces = []
    #     copy_bo = deepcopy(self)
    #     copy_bo.update_moves()
    #     safe_moves = copy_bo.get_safe_moves(color)
    #     print(safe_moves)

    #     for piece in safe_moves:
    #         former_pos = piece.row, piece.col

    #         for move in safe_moves[piece]:
    #             i, j = move
    #             value = copy_bo.board[i][j] 
                
    #             # a, b = piece.row, piece.col
    #             copy_bo.board[i][j] = piece
    #             a, b = piece.row, piece.col
    #             copy_bo.board[a][b] = 0
    #             piece.change_pos(move)

    #             copy_bo.is_checked(color)

    #             if not(copy_bo.check):
    #                 if piece in only_moves:
    #                     piece.change_pos(former_pos)
    #                     only_moves[piece].append(move)
    #                     print('success')
                    
    #                 else:
    #                     only_moves[piece] = [move]

    #             else:
    #                 if (former_pos not in invalid_pieces):
    #                     self.invalid_lst.append(former_pos)

           
    #             if value != 0:
    #                 k, m = value.row, value.col
    #                 copy_bo.board[i][j] = value
    #                 copy_bo.board[a][b] = piece
    #                 piece.change_pos(former_pos)
                
    #             else:
    #                 copy_bo.board[i][j] = 0
    #                 copy_bo.board[a][b] = piece
    #                 piece.change_pos(former_pos)

        
    #     for piece in only_moves:
    #         self.valid_piece_pos.append((piece.get_pos()))
        
    #     if pos in self.valid_piece_pos and pos in self.block_check:
    #         print('off')
    #         self.block_check.remove(pos)
    #         # self.block_check.remove()
        
    #     # for piece in only_moves:
    #     #     pos = (piece.row, piece.col)
    #     #     if (piece.row, piece.col) in invalid_pieces:
    #     #         invalid_pieces.remove(pos)
        
    #     print(only_moves)


    #     print(invalid_pieces)

    #     return only_moves






        



