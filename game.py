'''
the main game
author:@techwithtim
requirements:see requirements.txt
'''

import subprocess
import sys
import get_pip
from minimax_algo import get_piece_and_best_move, get_piece_and_best_move2, get_piece_and_best_move3, minimax
from piece import Piece
from constants import win, width, height
import asyncio

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    #print("[GAME] Trying to import pygame")
    import pygame
except:
    #print("[EXCEPTION] Pygame not installed")

    try:
        #print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        #print("[GAME] Pygame has been installed")
    except:
        #print("[EXCEPTION] Pip not installed on system")
        #print("[GAME] Trying to install pip")
        get_pip.main()
        #print("[GAME] Pip has been installed")
        try:
            #print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            #print("[GAME] Pygame has been installed")
        except:
            #print("[ERROR 1] Pygame could not be installed")
            pass


import pygame
import os
import time

import pickle
from board import Board
from player import Player
pygame.font.init()

board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("img", "chessbg.png"))
rect = (113,113,525,525)
bo = Board(8, 8)
h_moves = set()

turn = "w"


def menu_screen(win, name):
    global bo, chessbg
    run = True
    offline = False

    while run:
        win.blit(chessbg, (0,0))
        small_font = pygame.font.SysFont("comicsans", 50)
        
        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
            win.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
               pass

    

def redraw_gameWindow(win, bo):
    win.blit(board, (0, 0))
    for tile in bo.lst_tiles.values():
        tile.draw(win)

    bo.draw(win, bo.turn)

    pygame.display.update()
    # pygame.time.delay(400)


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False



def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2]/8))
            j = int(divY / (rect[3]/8))
            return i, j

    return -1, -1


def set_piece_to_move(piece, piece_to_move, valid_moves, attack_moves, invalid):
    # #print(valid_moves, "valid_moves")

    # if piece.pawn and len(attack_moves):
    #     valid_moves.extend(attack_moves)

    # #print(attack_moves, "attack")

    if len(piece_to_move) and not(piece in  piece_to_move):
        items = tuple(piece_to_move.items())
        prev_p = items[0][0]
        prev_p.selected = False
        toggle_show_moves(piece_to_move)
        toggle_piece_attack(prev_p)
        piece_to_move.clear() 

    if piece in  piece_to_move:
        piece.selected = False
        toggle_show_moves(piece_to_move)
        toggle_piece_attack(piece)
        del piece_to_move[piece]
    
    # if len(piece_to_move):
    #     piece = piece_to_move
    
    elif len(valid_moves) and not(invalid):
        piece_to_move[piece] = valid_moves
        # toggle_piece_attack(piece)
        # #print(valid_moves)
    
    elif len(attack_moves) and not invalid:
        piece_to_move[piece] = attack_moves
        # #print("att")
        # toggle_piece_attack(piece)
    
    else:
        piece.selected = False
        toggle_piece_attack(piece)
        # #print(valid_moves)
    

    if len(piece_to_move):
        items = tuple(piece_to_move.items())
        prev_p = items[0][0]
        toggle_piece_attack(prev_p)



def handle_player_pieces(current_player, mouse_pos, piece_to_move):
    invalid_move = False


    for i in range(8):
            for j in range(8):
                if bo.board[i][j] != 0:
                    # #print()
                    if bo.board[i][j].color == current_player.color and bo.board[i][j].isSelected(mouse_pos):
                        piece = bo.board[i][j]
                        attack_moves = piece.attack_moves
                        valid_moves = piece.move_list
                        # #print(valid_moves)
                        
                        # for inval in invalid:
                        #     if inval.isSelected(mouse_pos, piece):
                        #         piece.selected = False
                        #         invalid_move = True

                        if piece in bo.prevent_block:
                            piece.selected = False
                            break

                        if bo.check and not(piece.king):
                            piece.selected = False
                            continue
                        
                        if not(bo.check) or piece.king:
                            set_piece_to_move(piece, piece_to_move, valid_moves, attack_moves, invalid_move)

                        
                        # elif  pos in bo.valid_piece_pos and bo.check or (pos in invalid):
                        #     set_piece_to_move(p, piece_to_move, only_moves[piece], [], invalid_move)
    
    
    if bo.check:
        checking = bo.checking_piece
        #print(checking)
        piece_attk_or_block = checking.possible_opp_block_or_attk
        #print(piece_attk_or_block)

        for p in bo.invalid_lst:
                if p in piece_attk_or_block:
                   del piece_attk_or_block[p]


        for piece in piece_attk_or_block:
            if piece not in bo.invalid_lst:
                if piece.isSelected(mouse_pos):
                    #print("yeah")
                    set_piece_to_move(piece, piece_to_move, piece_attk_or_block[piece], [], invalid_move)
                    

    
    # block_check = handle_check_and_invalid(only_moves, piece_to_move, mouse_pos, invalid)

    # #print(piece_to_move)
        
    # return block_check
            

def toggle_show_moves(piece_to_move):

    for piece in piece_to_move:
        for move in piece_to_move[piece]:   
            bo.lst_tiles[move].toggle_highlight(toggle_hint = False)
    
    # for pos in h_moves:
    #     bo.lst_tiles[pos].toggle_highlight(False)


def make_move(piece, lost_pieces, tile, invalid, attack, p):
    piece.rect_i.x = tile.rect.x
    piece.rect_i.y = tile.rect.y

    i, j = attack

    if not(invalid):
        lost_pieces.append(p)

    bo.board[i][j] = piece
    a, b = piece.row, piece.col
    bo.board[a][b] = 0
    piece.change_pos(attack)
          

def handle_piece_movement(piece_to_move, event, lost_pieces):
    moved = False
    piece_moved = None
    invalid = False

    for piece in piece_to_move:
        for move in piece_to_move[piece]:
            tile = bo.lst_tiles[move]
            i, j = move
            p = bo.board[i][j]

            if p != 0:

                invalid = p.color == piece.color

                # if not(invalid):
                #     bo.post_move_capture()
            
            else:
                invalid = False

                # if invalid:
                #     continue
            # #print(invalid)
            # #print(p)
            # #print(bo.board)
            if event.button == 1 and tile.clicked(event.pos) and tile.highlight and not(invalid):

                # piece.rect_i.x = tile.rect.x
                # piece.rect_i.y = tile.rect.y
                destination = [tile.rect.x, tile.rect.y]

            
                rook = bo.castle(piece, move)
                #print(rook)
                
                if rook is not None:
                    pos = rook.get_pos()
                    til = bo.lst_tiles[pos]
                    des = [til.rect.x, til.rect.y]
                    #print("castle")
                    piece.animate_piece_movement(destination, win, redraw_gameWindow, bo)
                    bo.post_castle()
                    rook.animate_piece_movement(des, win, redraw_gameWindow, bo)

                if rook is None:
                    piece.animate_piece_movement(destination, win, redraw_gameWindow, bo)

                    if p == 0:
                        bo.post_move_self()
                        

                if not(invalid):
                    lost_pieces.append(p)
                
                if p == 0 and not(piece.pawn):
                    bo.halfmove_clock += 1
                
                else:
                    bo.halfmove_clock = 0


                if piece.color == "b":
                    bo.fullmove_number += 1
                
                if rook is None:
                    bo.board[i][j] = piece
                    a, b = piece.row, piece.col
                    bo.board[a][b] = 0
                    piece.change_pos(move)
        
                    bo.promotion(piece)
                
                if not(isinstance(p, int)):
                    bo.post_move_capture()


                piece_moved = piece
                moved = True
                piece.selected = False
                tile.selected = False

    # if len(piece_to_move):   
    #     items = tuple(piece_to_move.items())
    #     prev_p = items[0][0]

    #     for attack in prev_p.attack_moves:
    #         tile = bo.lst_tiles[attack]
    #         p = bo.board[i][j]
    #         if event.button == 1 and tile.clicked(event.pos) and tile.highlight and not(invalid) and moved == False:
    #             make_move(prev_p, lost_pieces, tile, invalid, attack, p)
    #             moved = True


    if moved:
        toggle_show_moves(piece_to_move)
        toggle_piece_attack(piece_moved)
        del piece_to_move[piece_moved]
        reset_piece_state(piece_moved)
    
    return moved


def  handle_check_and_invalid(only_moves, piece_to_move, mouse_pos, invalid):
    block_check = None
    for p in only_moves:

        pos = (p.row, p.col)

        if (p.color == bo.turn and bo.check and p.isSelected(mouse_pos)) or (pos in invalid):
            # piece_to_move[piece]  = only_moves[piece]
            invalid_move = False
            #print("active")
            set_piece_to_move(p, piece_to_move, only_moves[p], [], invalid_move)
            items = tuple(piece_to_move.items())

            if len(piece_to_move) and not(pos in invalid):
               block_check = items[0][0]
    
    return block_check


def reset_piece_state(piece):
    piece.first = False

def toggle_piece_attack(piece):
    # #print("attack")
    # #print()
    for attack in piece.attack_moves:
        bo.lst_tiles[attack].attack_highlight()
    

def handle_player_turn(players, current_player_idx):

    current_player_idx = (current_player_idx + 1) % len(players)

    return current_player_idx 

def handle_sound(event):
    if event.type == bo.move_check()[0]:
        bo.move_check()[1].play()
    
    elif event.type == bo.move_capture()[0]:
        bo.move_capture()[1].play()
    
    elif event.type == bo.promote()[0]:
        bo.promote()[1].play()
    
    elif event.type == bo.move_self()[0]:
        bo.move_self()[1].play()
    
    elif event.type == bo.game_start()[0]:
        bo.game_start()[1].play()
        pygame.time.delay(1000)
    
    elif event.type == bo.game_end()[0]:
        bo.game_end()[1].play()
        

async def calculate():
    my_piece, b_m = get_piece_and_best_move(bo)
    if isinstance(my_piece, Piece):
        current_pos = my_piece.get_pos()
        
    h_moves.add(current_pos)
    h_moves.add(b_m)


async def main():
    color = "w"
    clock = pygame.time.Clock()
    run = True
    players = [Player(i) for i in range(2)]
    current_player_idx = 0
    current_player = players[current_player_idx]
    piece_to_move = {}
    lost_pieces = []
    start = True
    switch = False
    move_interval = 2000
    last_move_time = pygame.time.get_ticks()
    


    while run:
        
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        try:
            redraw_gameWindow(win, bo)
        except Exception as e:
            #print(e)
            end_screen(win, "Other player left")
            run = False
            break


        # if bo.winner == "w":
        #     pygame.time.delay(2000)
        #     end_screen(win, "White is the Winner!")
        #     run = False
        
        if start:
             bo.update_moves()
             bo.post_start()
             start = False
    

        # if bo.winner == "b":
        #     pygame.time.delay(2000)
        #     end_screen(win, "Black is the winner")
        #     run = False
        current_time = pygame.time.get_ticks()



        if not(player_color):
            if current_time - last_move_time >= move_interval: 
                if bo.turn == "b" and bo.winner == None:
                    p, best_move = get_piece_and_best_move2(bo)
                    # pygame.time.delay(400)
                    if p is not None:
                        bo.simulate_move(p, best_move, redraw_gameWindow, win)
                
                        current_player_idx = handle_player_turn(players, current_player_idx)
                        current_player = players[current_player_idx]
                        bo.turn = current_player.color
                        bo.is_checked(bo.turn)
                        bo.update_moves()

                

                elif bo.turn == "w" and bo.winner == None:
                    p, best_move = get_piece_and_best_move(bo) 

                    if p is not None:
                        # pygame.time.delay(300)
                        bo.simulate_move(p, best_move, redraw_gameWindow, win)
                
                        current_player_idx = handle_player_turn(players, current_player_idx)
                        current_player = players[current_player_idx]
                        bo.turn = current_player.color
                        bo.is_checked(bo.turn) 
                        bo.update_moves()
                
                last_move_time = current_time

                # score, lst = minimax(bo, 1, float("-inf"), float("inf"), bo.turn)
                # m_p = lst[0]
                # best_move = lst[2]
            
                # #print(score, "score")
                # #print(best_move, "best")

                # if m_p is not None: 
                #     row, col = m_p.get_pos()
                #     #print(row, col, "piece")
                #     piece_  = bo.get_piece(row, col)

                #     bo.simulate_move(piece_, best_move, redraw_gameWindow, win)
                #     #print("mini_max")

                #     current_player_idx = handle_player_turn(players, current_player_idx)
                #     current_player = players[current_player_idx]
                #     bo.turn = current_player.color
                #     bo.is_checked(bo.turn)
                #     bo.update_moves()


        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
            

            if event.type == bo.move_check()[0]:
                bo.move_check()[1].play()
            
            elif event.type == bo.move_capture()[0]:
                bo.move_capture()[1].play()
            
            elif event.type == bo.promote()[0]:
                bo.promote()[1].play()
            
            elif event.type == bo.move_self()[0]:
                bo.move_self()[1].play()
            
            elif event.type == bo.game_start()[0]:
                bo.game_start()[1].play()
                pygame.time.delay(1000)
            
            elif event.type == bo.game_end()[0]:
                bo.game_end()[1].play()
            
            elif event.type == bo.castle_sound()[0]:
                bo.castle_sound()[1].play()
        

            
            if player_color:
                if bo.turn != player_color and bo.winner == None:
                    p, best_move = get_piece_and_best_move3(bo)
                    # pygame.time.delay(400)

                    if p is not None:
                        bo.simulate_move(p, best_move, redraw_gameWindow, win)
                
                        current_player_idx = handle_player_turn(players, current_player_idx)
                        current_player = players[current_player_idx]
                        bo.turn = current_player.color
                        bo.is_checked(bo.turn)
                        bo.update_moves()

            

                if event.type == pygame.MOUSEBUTTONDOWN and bo.turn == player_color:
                        # null = await calculate()
                        

                        if event.button == 3:  
                            # #print("hi")
                            handle_player_pieces(current_player, event.pos, piece_to_move) 
                            toggle_show_moves(piece_to_move)

                        moved = handle_piece_movement(piece_to_move, event, lost_pieces)

                        if moved:
                            current_player_idx = handle_player_turn(players, current_player_idx)
                            current_player = players[current_player_idx]
                            bo.turn = current_player.color
                            bo.is_checked(bo.turn)
                
                            bo.update_moves()

                            # if bo.check:
                            #      only_moves, _ = bo.simulate_move(bo.turn)
                             
                            # else:
                            #     only_moves.clear()
                            for piece in bo.prevent_block[:]:
                                    for move in piece.move_list[:]:
                                            for direc in bo.path:
                                                if move not in direc and move in piece.move_list:
                                                    piece.move_list.remove(move)
                                                    #print(move, "removed....")
                                    
                                    if len(piece.move_list):
                                        bo.prevent_block.remove(piece)
                    
                            

                        # only_moves, invalid_p = bo.simulate_move(bo.turn)
                        # #print(invalid_p)
            # handle_sound(event)
        
        
        if bo.winner == "w":
            pygame.time.delay(10000)
            end_screen(win, "White is the Winner!")
            run = False
        

        elif bo.winner == "b":
            pygame.time.delay(10000)
            end_screen(win, "Black is the winner")
            run = False
        
       
        elif bo.stalemate:
            pygame.time.delay(10000)
            end_screen(win, "Draw by Stalemate!")
            run = False
        
        
        if bo.check:
            checking = bo.checking_piece
            piece_attk_or_block = checking.possible_opp_block_or_attk
            #print(piece_attk_or_block)

            if not(len(piece_attk_or_block)) and bo.king_trapped():
                bo.post_end()

                if bo.turn == "w":
                    bo.winner = "b"

                else:
                    bo.winner = "w"

        bo.is_stalemate()
        # pygame.time.delay(1000)      
       
                
        # # try:
        #     redraw_gameWindow(win, bo)
        # except Exception as e:
        #     #print(e)ss
        #     end_screen(win, "Other player left")
        #     run = False
        #     break
       
        # for tile in bo.lst_tiles.values():
        #     if tile.clicked(mouse_pos) and not tile.highlight:
        #         tile.toggle_highlight()
        


# name = input("Please type your name: ")
while True:
    player_color = input("Select player color(w or b) press enter to watch gameplay: ").lower()

    if not(player_color) or player_color in ["w", "b"]:
        
        # if player_color == "b":
        #    bo.flip(player_color)

        break

pygame.display.set_caption("Chess Game")
asyncio.run(main())
# menu_screen(win, name)s
# for _ in range(3):
#     asyncio.run(main())
#     bo = Board(8, 8)
 