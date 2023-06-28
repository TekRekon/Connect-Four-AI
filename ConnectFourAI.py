import math
import random

import TranspositionTable

nodes_explored = 0


def minimax(bd, depth, is_maximizing, bot_piece, player_piece, alpha, beta, turns, ind, transp):
    if transp.get(bd.get_bitboard()) is not None: return transp.get(bd.get_bitboard())
    global nodes_explored
    nodes_explored += 1
    result = bd.get_board_state()
    if result == 'TIE':
        return 0
    elif result == bot_piece:
        return 100 * (43 - turns)
    elif result == player_piece:
        return 100 * (turns - 43)
    elif depth == 0:
        return bd.heuristic(ind + 1) + (100 * bd.get_num_threes(ind + 1))

    moves = bd.get_pruned_moves(ind + 1, 3 - (ind + 1), player_piece, bot_piece)
    # moves = bd.get_valid_moves()

    if is_maximizing:
        best_score = -math.inf
        for move in moves:
            bd.make_move(move, ind + 1)
            new_score = max(best_score, minimax(bd=bd, depth=depth - 1, is_maximizing=not is_maximizing,
                                                bot_piece=bot_piece, player_piece=player_piece, alpha=alpha,
                                                beta=beta, ind=ind, turns=turns + 1, transp=transp))
            transp.insert(bd.get_bitboard(), new_score)
            if new_score > best_score: best_score = new_score
            alpha = max(alpha, best_score)
            bd.remove_piece(move)
            # if alpha (our current move) is greater than beta (opponent best move)
            # the opponent will never play it, and we can prune this branch
            if alpha >= beta:
                break
        return best_score
    else:
        best_score = math.inf
        for move in moves:
            bd.make_move(move, 3 - (ind + 1))
            new_score = min(best_score, minimax(bd=bd, depth=depth - 1, is_maximizing=not is_maximizing,
                                                bot_piece=bot_piece, player_piece=player_piece, alpha=alpha,
                                                beta=beta, ind=ind, turns=turns + 1, transp=transp))
            transp.insert(bd.get_bitboard(), new_score)
            if new_score < best_score: best_score = new_score
            beta = min(beta, best_score)
            bd.remove_piece(move)
            if alpha >= beta:
                break
        return best_score


def find_best_move(bd, bot_piece, player_piece, depth, ind, turns):
    bd.print_bitboard()
    print(bd.heuristic(ind + 1))
    print('finding best move')
    global nodes_explored
    nodes_explored = 0
    best_move = random.choice(bd.get_valid_moves())
    highest_score = -math.inf
    moves = bd.get_pruned_moves(ind + 1, 3 - (ind + 1), player_piece, bot_piece)
    moves = bd.get_valid_moves()
    tp = TranspositionTable.TranspositionTable(10000000)
    for move in moves:
        print(f'checking move {move}')
        bd.make_move(move, ind + 1)
        score = minimax(bd=bd, depth=depth, is_maximizing=False, bot_piece=bot_piece, player_piece=player_piece,
                        alpha=-math.inf, beta=math.inf, ind=ind, turns=turns + 1, transp=tp)
        bd.remove_piece(move)
        if score > highest_score:
            highest_score = score
            best_move = move
    return best_move, nodes_explored, highest_score
