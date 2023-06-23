import math
import random

nodes_explored = 0

def minimax(bd, depth, is_maximizing, bot_piece, player_piece, alpha, beta, turns, ind):
    global nodes_explored
    nodes_explored += 1
    result = bd.is_terminal()
    if result == 'TIE':
        return 0
    elif result == bot_piece:
        return 42-turns
    elif result == player_piece:
        return -(42-turns)
    elif depth == 0: return 0

    if is_maximizing:
        best_score = -math.inf
        moves = bd.get_valid_moves()
        for move in moves:
            bd.make_move(move, ind+1)
            best_score = max(best_score, minimax(bd=bd, depth=depth-1, is_maximizing=not is_maximizing,
                                                 bot_piece=bot_piece, player_piece=player_piece, alpha=alpha,
                                                 beta=beta, ind=ind, turns=turns+1))
            alpha = max(alpha, best_score)
            bd.remove_piece(move)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        moves = bd.get_valid_moves()
        for move in moves:
            bd.make_move(move, 3-(ind+1))
            best_score = min(best_score, minimax(bd=bd, depth=depth-1, is_maximizing=not is_maximizing,
                                                 bot_piece=bot_piece, player_piece=player_piece, alpha=alpha,
                                                 beta=beta, ind=ind, turns=turns+1))
            beta = min(beta, best_score)
            bd.remove_piece(move)
            if beta <= alpha:
                break
        return best_score


def find_best_move(bd, bot_piece, player_piece, depth, ind, turns):
    global nodes_explored
    nodes_explored = 0
    highest_score = -math.inf
    moves = bd.get_valid_moves()
    best_move = random.choice(moves)
    for move in moves:
        bd.make_move(move, ind+1)
        score = minimax(bd=bd, depth=depth, is_maximizing=False, bot_piece=bot_piece, player_piece=player_piece,
                        alpha=-math.inf, beta=math.inf, ind=ind, turns=turns+1)
        bd.remove_piece(move)
        if score > highest_score:
            highest_score = score
            best_move = move
    return best_move, nodes_explored
