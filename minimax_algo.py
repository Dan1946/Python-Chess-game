from copy import deepcopy
import chess.engine
import chess
import subprocess
from stockfish import Stockfish
import pygame


stockfish = Stockfish(path=r"C:\Users\Daniel Oni\Documents\stockfish\stockfish-windows-x86-64-avx2.exe", depth=11, parameters={"Threads": 2, "Minimum Thinking Time": 30}) # 18
stockfish2 = Stockfish(path=r"C:\Users\Daniel Oni\Documents\stockfish\stockfish-windows-x86-64-avx2.exe", depth=11, parameters={"Threads": 2, "Minimum Thinking Time": 30})
# stockfish2.set_elo_rating(2500)

def board_to_fen(board):
    """
    Convert a chessboard to FEN (Forsyth-Edwards Notation) format.
    """
    fen = ""
    empty_count = 0

    # Iterate over each row of the board
    for row in board.board:
        for square in row:
            # If the square is empty, increment the empty square count
            if square == 0:
                empty_count += 1
            else:
                # If there are empty squares, add the count to the FEN string
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                # Add the piece symbol to the FEN string
                fen += square.square_symbol # Assuming each piece object has a method 'symbol' that returns its FEN symbol

                if square.pawn:
                    fen += square.promoted
                    square.promoted = ""
        # If there are empty squares at the end of the row, add the count to the FEN string
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        # Separate rows with a slash
        fen += "/"
    
    # Remove the trailing slash
    fen = fen[:-1]

    # Add additional FEN components for active color, castling rights, en passant square, halfmove clock, and fullmove number
    fen += " " + board.turn
    fen += " " + "-"
    fen += " " + "-"  # en passant
    fen += " " + str(board.halfmove_clock)
    fen += " " + str(board.fullmove_number)
    
    return fen


def minimax(position, depth, alpha, beta, max_player):
    if depth == 0 or position.winner is not None:
        return evaluate_board(position), position
    
    if max_player:
        current_piece = None
        maxEval = float('-inf')
        best_move = None
        current_chosen_move = None
        for move in get_all_moves(position, "b"):
            evaluation = minimax(move[0], depth-1, alpha, beta, False)[0]
            # print(evaluation, "evalw")
            maxEval = max(maxEval, evaluation)
            if maxEval >= beta:
                return maxEval, [current_piece, best_move, current_chosen_move]
            if maxEval > alpha:
                alpha = maxEval
                best_move = move[0]
                current_piece = move[1]
                current_chosen_move = move[2]
        
        return maxEval, [current_piece, best_move, current_chosen_move]
    
    else:
        opp_piece = None
        minEval = float('inf')
        best_move = None
        opp_chosen_move = None
        for move in get_all_moves(position, "w"):
            evaluation = minimax(move[0], depth-1, alpha, beta, True)[0]
            # print(evaluation, "evalb")
            minEval = min(minEval, evaluation)
            if minEval <= alpha:
                return minEval, [opp_piece, best_move, opp_chosen_move]
            if minEval < beta:
                beta = minEval
                best_move = move[0]
                opp_piece = move[1]
                opp_chosen_move = move[2]
        
        return minEval, [opp_piece, best_move, opp_chosen_move]


def get_all_moves(position, color):
    moves = []
    position.promoted = None
    position.is_checked(color)

    position.update_moves()
    
    piece_to_move = position.handle_player_pieces(color)

    for piece in piece_to_move:
        for move in piece_to_move[piece]:
            temp_board = deepcopy(position)
            temp_piece = temp_board.get_piece(piece.row, piece.col)

            moved = temp_board.simulate_move(temp_piece, move)
            new_pos = temp_piece.get_pos()


            if moved:
                # temp_board.draw(win, color)
                # pygame.display.update()
                moves.append([temp_board, piece, new_pos])
    
    return moves


def evaluate_board(board):
    fen = board_to_fen(board)
    engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Daniel Oni\Documents\stockfish\stockfish-windows-x86-64-avx2.exe")
    info = engine.analyse(chess.Board(fen), chess.engine.Limit(time=0.1))
    evaluation = info["score"].relative.score()
    engine.quit()
    return evaluation


def algebraic_to_coordinates(square):
    """
    Convert algebraic notation to coordinates.
    """
    file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    rank_map = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    file_letter = square[0]
    rank_number = square[1]
    file_index = file_map[file_letter]
    rank_index = rank_map[rank_number]
    return rank_index, file_index


def communicate_with_stockfish(command):
    """
    Communicate with Stockfish via UCI protocol.
    """
    stockfish_process = subprocess.Popen([r"C:\Users\Daniel Oni\Documents\stockfish\stockfish-windows-x86-64-avx2.exe"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stockfish_process.stdin.write(command + '\n')
    stockfish_process.stdin.flush()
    output = stockfish_process.stdout.readline().strip()
    stockfish_process.stdin.close()
    stockfish_process.stdout.close()
    stockfish_process.terminate()
    return output

def evaluate_position(board):
    """
    Evaluate the current position using Stockfish.
    """
    fen = board_to_fen(board)
    evaluation = stockfish.get_evaluation()
    return evaluation

def get_best_move(board):
    """
    Find the best move using Stockfish.
    """
    fen = board_to_fen(board)
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move


def get_best_move2(board):
    """
    Find the best move using Stockfish.
    """
    fen = board_to_fen(board)
    stockfish2.set_fen_position(fen)
    best_move = stockfish2.get_best_move()
    return best_move


def get_piece_and_best_move(bo):
    best_move_s = get_best_move(bo)

    if best_move_s is None:
        return None, None

    evaluation = evaluate_position(bo)
    print("Evaluation:", evaluation)
    print("Best move:", best_move_s)
    start_square = algebraic_to_coordinates(best_move_s[:2])
    best_move = algebraic_to_coordinates(best_move_s[2:])
    row, col = start_square

    piece = bo.get_piece(row, col)

    return piece, best_move


def get_piece_and_best_move2(bo):
    best_move_s = get_best_move2(bo)

    if best_move_s is None:
        return None, None

    evaluation = evaluate_position(bo)
    print("Evaluation:", evaluation)
    print("Best move:", best_move_s)
    start_square = algebraic_to_coordinates(best_move_s[:2])
    best_move = algebraic_to_coordinates(best_move_s[2:])
    row, col = start_square

    piece = bo.get_piece(row, col) 

    return piece, best_move






# Example usage
# # current_board = create_initial_board()
# evaluation = evaluate_position(current_board)
# best_move = get_best_move(current_board)
# print("Evaluation:", evaluation)
# print("Best move:", best_move)




# # Example usage
# start_square = "g1"
# best_move = "f3"
# start_square_coordinates = algebraic_to_coordinates(start_square)
# best_move_coordinates = algebraic_to_coordinates(best_move)
# print("Start square coordinates:", start_square_coordinates)
# print("Best move coordinates:", best_move_coordinates)




    


    
