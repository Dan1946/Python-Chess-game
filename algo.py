

def dfs_movement(piece, bo):
    start_pos = (piece.row, piece.col)
    # #print(start_pos)

    stack = [start_pos]
    grid = bo.board
    directions = ["up", "down", "left", "right", "up-l-d", "down-l-d", "up-r-d", "down-r-d"]
    direction_moves = {direc: [] for direc in directions}
    d_m = {direc: [] for direc in directions}

    # #print("algo-working")
    for direction in directions:
        # #print(direction)
        visited = set()
        while len(stack):
            row, col = stack.pop()

            if (row, col) in visited:
                continue

            value = bo.board[row][col]


            if value is not piece and value != 0:
                if value.color == piece.color:
                    # #print("skip")
                    d_m[direction].append((row, col))
                    
                    continue

                elif not(value.color == piece.color) and piece.pawn and direction not in ["up", "down"]:
                    direction_moves[direction].append((row, col))
                    d_m[direction].append((row, col))
                    break

                elif not(value.color == piece.color) and piece.pawn:
                    break

                else:
                    if not(value.king) or piece.king:
                        direction_moves[direction].append((row, col))
                        d_m[direction].append((row, col))

                        break

                    # if value.king:
                    #     bo.check = True

                    elif (piece.queen or piece.rook or piece.bishop) and value.king: 
                        piece.detect_k = True
                        # #print("stop him")
                        
                        # bo.check = True

            
            visited.add((row, col))
            # #print(visited)

            if (row, col) != start_pos:
                direction_moves[direction].append((row, col))
                d_m[direction].append((row, col))
           

            neighbours = find_neighbours(grid, piece, row, col, direction)
            # #print(neighbours, "bad")

            # if not(len(neighbours)):
            #     #print("not possible")
            #     break
            if value != 0:
                if piece.detect_k and len(neighbours) and value.king:
                    value.include_k_m.clear()
                    value.include_k_m.append(neighbours[0])
                    value.detected = True
                    break
            
            piece.detect_k = False
            
            
            for neighbour in neighbours:
                stack.append(neighbour)
        
        stack.append(start_pos)
    
    valid_m = filter_moves(piece, d_m, directions, bo, True)
    get_proct_pos(piece, valid_m, grid)
    
    valid_moves = filter_moves(piece, direction_moves, directions, bo)
    # #print(direction_moves)
    return valid_moves


def find_neighbours(grid, piece, row, col, direction):
    neighbours = []
    if direction == "up":
        if row > 0 and (piece.queen or piece.rook or piece.king or piece.pawn):# up
            neighbours.append((row - 1, col))
    
    if direction == "up-l-d":
        if row > 0 and col > 0 and (piece.queen or piece.bishop or piece.king or piece.pawn): # up left diagonal
                neighbours.append((row - 1, col - 1))
    
    if direction == "up-r-d":
        if row > 0 and (piece.queen or piece.bishop or piece.king or piece.pawn): # up right diagonal
            if col < len(grid[row - 1]) - 1:
                neighbours.append((row - 1, col + 1))

    if direction == "down":
        if row < len(grid) - 1 and (piece.queen or piece.rook or piece.king or piece.pawn): # down
            neighbours.append((row + 1, col))
    
    if direction == "down-l-d":
        if row < len(grid) - 1 and col > 0 and (piece.queen or piece.bishop or piece.king or piece.pawn): # down lft diagonal
            neighbours.append((row + 1, col - 1))
        
    if direction == "down-r-d":
        if row < len(grid) - 1 and (piece.queen or piece.bishop or piece.king or piece.pawn): #down right diagonal
            if col < len(grid[row + 1]) - 1:
                neighbours.append((row + 1, col + 1))
    
    if direction == "left":
        if col > 0 and (piece.queen or piece.rook or piece.king): # left
            neighbours.append((row, col - 1))
    
    if direction == "right":
        if col < len(grid[row]) - 1 and (piece.queen or piece.rook or piece.king): # right
            neighbours.append((row, col + 1))
    
    return neighbours


def filter_moves(piece, direc_moves, direcs, bo, reset = False):
    moves = []
    up = direcs[0]
    down = direcs[1]
    left = direcs[2]
    right = direcs[3]
    u_l_d = direcs[4]
    u_r_d = direcs[6]
    d_l_d = direcs[5]
    d_r_d = direcs[7]

    up_move = direc_moves[up]
    down_move = direc_moves[down]
    left_move = direc_moves[left]
    right_moves = direc_moves[right]
    u_l_d_moves = direc_moves[u_l_d]
    u_r_d_moves = direc_moves[u_r_d]
    d_l_d_moves = direc_moves[d_l_d]
    d_r_d_moves = direc_moves[d_r_d]

    piece.diag_assualt.clear()

    all_dir_moves = [up_move, down_move, left_move, right_moves, u_l_d_moves, u_r_d_moves, d_l_d_moves, d_r_d_moves]

    # white pawns
    if piece.pawn and piece.first and piece.color == "w" and len(up_move):
        if len(up_move) > 1:
            combine = [up_move[0], up_move[1]]
            moves.extend(combine)

        elif len(up_move) > 0:
            combine = [up_move[0]]
            moves.extend(combine)
    
    if piece.pawn and not(piece.first) and piece.color == "w" and len(up_move):
        moves.extend([up_move[0]])
        
    if piece.pawn and piece.color == "w":
        m = []

        for dir_move in all_dir_moves[4:6]:
            if len(dir_move):
                 piece.diag_assualt.append(dir_move[0])

                 x, y = dir_move[0]

                 if bo.board[x][y] != 0:
                    if bo.board[x][y].color != piece.color:
                        m.append(dir_move[0])

                        # if bo.board[x][y].king:
                        #     bo.check = True

        piece.attack_moves.extend(m)

    # black pawns
    if piece.pawn and piece.first and piece.color == "b" and len(down_move):
        if len(down_move) > 1:
            combine = [down_move[0], down_move[1]]
            moves.extend(combine)

        elif len(down_move) > 0:
            combine = [down_move[0]]
            moves.extend(combine)
    
    if piece.pawn and not(piece.first) and piece.color == "b" and len(down_move):
        moves.extend([down_move[0]])

    if  piece.pawn and piece.color == "b":
        m = []

        for dir_move in all_dir_moves[6:]:
            if len(dir_move):
                piece.diag_assualt.append(dir_move[0])

                i, j = dir_move[0]
                if bo.board[i][j] != 0:
                    if bo.board[i][j].color != piece.color:
                        m.append(dir_move[0])

                        # if bo.board[x][y].king:
                        #     bo.check = True

        piece.attack_moves.extend(m)

    
    if piece.king:
        m = []
        for dir_move in all_dir_moves:
            if len(dir_move):
                if dir_move == left and not(len(piece.left)):
                    piece.left.append(dir_move[0])
                
                elif dir_move == right and not(len(piece.left)):
                    piece.right.append(dir_move[0])

            if len(dir_move):
                m.append(dir_move[0])

        moves.extend(m)
        piece.king_moves.extend(moves)

    
    if piece.king and piece.first and not(bo.check):
        m = []
        for dir_move in all_dir_moves[2:4]:

             if len(dir_move):
                if dir_move == left and not(len(piece.left)):
                    piece.left.extend(dir_move[1:])
                
                elif dir_move == right and not(len(piece.left)):
                    piece.right.extend(dir_move[1:])


             if len(dir_move):
                m.append(dir_move[1:])

        for mv in m:
            moves.extend(mv)


    
    if piece.rook:
        combine = left_move + right_moves + up_move + down_move
        moves.extend(combine)

    
    if piece.queen:
        combine = left_move + right_moves + up_move + down_move + u_l_d_moves + u_r_d_moves + d_l_d_moves + d_r_d_moves
        moves.extend(combine)


    
    if piece.bishop:
        combine = u_l_d_moves + u_r_d_moves + d_l_d_moves + d_r_d_moves
        moves.extend(combine)
    
    # if piece.pawn:
    #     for attack in piece.attack_moves:
    #         a, b = attack

    #         if bo.board[a][b].king:
    #             bo.check = True

    #         else:
    #             bo.check = False
    
    # else:
    #     for att in moves:
    #         k, l = att
    #         if bo.board[k][l].king:
    #             bo.check = True
            
    #         else:
    #            bo.check = False
    # bo.is_checked(bo.turn)
    if not(piece.pawn or piece.king) and not(reset):
        opp_pieces = bo.get_opp_pieces(piece.color)

        if piece.queen:
            total = [left_move, right_moves, up_move, down_move, u_l_d_moves, u_r_d_moves, d_l_d_moves, d_r_d_moves]
        
        elif piece.rook:
            total = [left_move, right_moves, up_move, down_move]
        
        elif piece.bishop:
            total = [u_l_d_moves, u_r_d_moves, d_l_d_moves, d_r_d_moves]


        for opp in opp_pieces:
            if opp.king:
                pos = opp.get_pos()
                for direction in total:
                    if pos in direction:
                        piece.direction = direction
                        # #print(f"{piece}:{piece.direction}", "direct")

    if reset:
        piece.attack_moves = []

    
    return moves

def get_proct_pos(piece, valid_m, grid):
    
    piece.protected_pos.clear()

    if not(piece.pawn):
        for pos in valid_m:
            i, j = pos
            if grid[i][j] != 0:
                if grid[i][j].color == piece.color:
                    piece.protected_pos.append(pos)
    
    else:
        for move in piece.diag_assualt:
            a, b = move

            if grid[a][b] != 0:
                if grid[a][b].color == piece.color:
                    piece.protected_pos.append(move)



def dfs_movement_king(piece, bo):
    start_pos = (piece.row, piece.col)
    # #print(start_pos)

    stack = [start_pos]
    grid = bo.board
    directions = ["up", "down", "left", "right", "up-l-d", "down-l-d", "up-r-d", "down-r-d"]
    direction_moves = {direc: [] for direc in directions}

    # #print("algo-working")
    for direction in directions:
        # #print(direction)
        visited = set()
        while len(stack):
            row, col = stack.pop()

            if (row, col) in visited:
                continue

            value = bo.board[row][col]
                        # bo.check = True
            
            visited.add((row, col))
            # #print(visited)

            if (row, col) != start_pos:
                direction_moves[direction].append((row, col))
           

            neighbours = find_neighbours(grid, piece, row, col, direction)
            
            
            for neighbour in neighbours:
                stack.append(neighbour)
        
        stack.append(start_pos)
    
    # #print(direction_moves)
    return direction_moves

    
        
    
    # #print(f"{piece}:{piece.protected_pos}", "proct")


    



    
    






    
    
    

        
    

