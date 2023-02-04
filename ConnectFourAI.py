import math
import random

nodes_explored = 0


def get_valid_locations(board, player_piece, bot_piece):
    valid_moves = []
    bad_moves = []
    for i in range(0, 7):
        column = [row[i] for row in board]
        for n in reversed(range(0, 6)):
            if list(column)[n] == '⚪':

                # Single turn win anticipation
                board[n][i] = bot_piece
                if check_board_state(board) == bot_piece:
                    valid_moves = [[n, i]]
                    board[n][i] = '⚪'
                    return valid_moves

                # Single turn loss anticipation
                board[n][i] = player_piece
                if check_board_state(board) == player_piece:
                    valid_moves = [[n, i]]
                    board[n][i] = '⚪'
                    return valid_moves

                # Double turn loss anticipation
                board[n][i] = bot_piece
                for k in range(0, 7):
                    column = [row[k] for row in board]
                    for j in reversed(range(0, 6)):
                        if list(column)[j] == '⚪':
                            board[j][k] = player_piece
                            if check_board_state(board) == player_piece:
                                bad_moves.append([n, i])
                            board[j][k] = '⚪'
                            break

                if [n, i] not in bad_moves:
                    # Sort moves so that the middle (more valuable) columns are searched first
                    for index, x in enumerate(valid_moves):
                        if abs(x[1]-3) >= abs(i-3):
                            valid_moves.insert(index, [n, i])
                            break
                    if not valid_moves:
                        valid_moves.append([n, i])

                board[n][i] = '⚪'
                break

    if not valid_moves:
        return bad_moves
    return valid_moves


def board_heuristic(board, bot_piece, player_piece, odd):
    bot_score = 0
    player_score = 0
    # Having a terminal move in certain rows is more valuable based on which player goes first
    bot_wanted_rows = [2, 4]
    player_wanted_rows = [1, 3]
    if odd:
        bot_wanted_rows = [1, 3]
        player_wanted_rows = [2, 4]

    accounted_terminal_cells = []
    for n, row in enumerate(board):
        for i, cell in enumerate(row):
            if cell in ['🔵', '🔴']:
                cell_value = 0
                current_wanted_rows = player_wanted_rows
                if cell == bot_piece:
                    current_wanted_rows = bot_wanted_rows

                # Gives the current piece a value based on the number opportunities it creates for a terminal move to
                # be made in specific rows
                if i < 4:
                    # Horizontal w/holes
                    if (n, i+1) not in accounted_terminal_cells:
                        if board[n][i+1] == '⚪':
                            if board[n][i] == board[n][i+2] == board[n][i+3]:
                                cell_value += 50
                                if n in current_wanted_rows and board[n+1][i+1] == '⚪':
                                    # Give more points to lower rows my multiplying by n
                                    cell_value += 100*n
                                accounted_terminal_cells.append((n, i+1))

                    elif (n, i+2) not in accounted_terminal_cells:
                        if board[n][i+2] == '⚪' and board[n][i] == board[n][i+1] == board[n][i+3]:
                            cell_value += 50
                            if n in current_wanted_rows and board[n+1][i+2] == '⚪':
                                cell_value += 100*n
                            accounted_terminal_cells.append((n, i+2))

                if i < 5:
                    # Horizontal
                    if (n, i+3) not in accounted_terminal_cells or (n, i-1) not in accounted_terminal_cells:
                        if board[n][i] == board[n][i+1] == board[n][i+2]:
                            if i < 4:
                                if board[n][i+3] == '⚪':
                                    cell_value += 50
                                    if n in current_wanted_rows and board[n+1][i+3] == '⚪':
                                        cell_value += 100*n
                                accounted_terminal_cells.append((n, i+3))

                            if i != 0:
                                if board[n][i-1] == '⚪':
                                    cell_value += 50
                                    if n in current_wanted_rows and board[n+1][i-1] == '⚪':
                                        cell_value += 100*n
                                accounted_terminal_cells.append((n, i-1))

                if n > 2 and i < 4:
                    # Diagonal up right w/holes
                    if (n-1, i+1) not in accounted_terminal_cells:
                        if board[n-1][i+1] == '⚪' and board[n][i] == board[n-2][i+2] == board[n-3][i+3]:
                                cell_value += 50
                                if n-1 in current_wanted_rows and board[n][i+1] == '⚪':
                                    cell_value += 100*n
                                accounted_terminal_cells.append((n-1, i+1))

                    if (n-2, i+2) not in accounted_terminal_cells:
                        if board[n-2][i+2] == '⚪' and (board[n][i] == board[n-1][i+1] == board[n-3][i+3]):
                            cell_value += 50
                            if n-2 in current_wanted_rows and board[n-1][i+2] == '⚪':
                                cell_value += 100*n
                            accounted_terminal_cells.append((n-2, i+2))

                if i < 5 and n > 1:
                    # Diagonal up right
                    if board[n][i] == board[n-1][i+1] == board[n-2][i+2]:
                        if (n+1, i-1) not in accounted_terminal_cells:
                            if n != 5 and i != 0:
                                if board[n+1][i-1] == '⚪':
                                    cell_value += 50
                                    if n+1 in current_wanted_rows and board[n+2][i-1] == '⚪':
                                        cell_value += 100*n
                                    accounted_terminal_cells.append((n+1, i-1))

                        if (n-3, i+3) not in accounted_terminal_cells:
                            if n != 2 and i != 4:
                                if board[n-3][i+3] == '⚪':
                                    cell_value += 50
                                    if n-3 in current_wanted_rows and board[n-2][i+3] == '⚪':
                                        cell_value += 100*n
                                    accounted_terminal_cells.append((n-3, i+3))

                if i > 1 and n > 1:
                    # Diagonal up left
                    if board[n][i] == board[n-1][i-1] == board[n-2][i-2]:
                        if (n+1, i+1) not in accounted_terminal_cells:
                            if n != 5 and i != 6:
                                if board[n+1][i+1] == '⚪':
                                    cell_value += 50
                                    if n+1 in current_wanted_rows and board[n+2][i+1] == '⚪':
                                        cell_value += 100*n
                                    accounted_terminal_cells.append((n+1, i+1))

                        if (n-3, i-3) not in accounted_terminal_cells:
                            if n != 2 and i != 2:
                                if board[n-3][i-3] == '⚪':
                                    cell_value += 50
                                    if n-3 in current_wanted_rows and board[n-2][i-3] == '⚪':
                                        cell_value += 100*n
                                    accounted_terminal_cells.append((n-3, i-3))

                if i > 2 and n > 2:
                    # Diagonal up left w/holes
                    if (n-1, i-1) not in accounted_terminal_cells:
                        if board[n-1][i-1] == '⚪' and board[n][i] == board[n-2][i-2] == board[n-3][i-3]:
                            cell_value += 50
                            if n-1 in current_wanted_rows and board[n][i-1] == '⚪':
                                cell_value += 100*n
                            accounted_terminal_cells.append((n-1, i-1))

                    elif (n-2, i-2) not in accounted_terminal_cells:
                        if board[n-2][i-2] == '⚪' and board[n][i] == board[n-1][i-1] == board[n-3][i-3]:
                            cell_value += 50
                            if n-2 in current_wanted_rows and board[n-1][i-2] == '⚪':
                                cell_value += 100*n
                            accounted_terminal_cells.append((n-2, i-2))

                # Vertical
                if n < 4 and n != 0:
                    if board[n][i] == board[n+1][i] == board[n+2][i]:
                        if board[n-1][i] == '⚪':
                            cell_value += 40

                if cell == bot_piece:
                    bot_score += cell_value
                elif cell == player_piece:
                    player_score += cell_value

    return bot_score - player_score


def minimax(board, depth, is_maximizing, bot_piece, player_piece, alpha, beta, odd):
    global nodes_explored
    nodes_explored += 1
    result = check_board_state(board)
    if result == 'TIE':
        return 0
    elif result == bot_piece:
        return math.inf
    elif result == player_piece:
        return -math.inf
    elif depth == 0:
        return board_heuristic(board=board, bot_piece=bot_piece, player_piece=player_piece, odd=odd)

    if is_maximizing:
        best_score = -math.inf
        moves = get_valid_locations(board=board, player_piece=player_piece, bot_piece=bot_piece)
        for move in moves:
            board[move[0]][move[1]] = bot_piece
            best_score = max(best_score, minimax(board=board, depth=depth-1, is_maximizing=not is_maximizing,
                                                 bot_piece=bot_piece, player_piece=player_piece, alpha=alpha,
                                                 beta=beta, odd=odd))
            alpha = max(alpha, best_score)
            board[move[0]][move[1]] = '⚪'
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        moves = get_valid_locations(board=board, player_piece=player_piece, bot_piece=bot_piece)
        for move in moves:
            board[move[0]][move[1]] = player_piece
            best_score = min(best_score, minimax(board=board, depth=depth-1, is_maximizing=not is_maximizing,
                                                 bot_piece=bot_piece, player_piece=player_piece, alpha=alpha,
                                                 beta=beta, odd=odd))
            beta = min(beta, best_score)
            board[move[0]][move[1]] = '⚪'
            if beta <= alpha:
                break
        return best_score


def find_best_move(board, bot_piece, player_piece, depth, odd):
    global nodes_explored
    nodes_explored = 0
    highest_score = -math.inf
    moves = get_valid_locations(board=board, player_piece=player_piece, bot_piece=bot_piece)
    best_move = random.choice(moves)
    for move in moves:
        board[move[0]][move[1]] = bot_piece
        score = minimax(board=board, depth=depth, is_maximizing=False, bot_piece=bot_piece, player_piece=player_piece,
                        alpha=-math.inf, beta=math.inf, odd=odd)
        board[move[0]][move[1]] = '⚪'
        if score > highest_score:
            highest_score = score
            best_move = [move[0], move[1]]
    return best_move, nodes_explored


def check_board_state(board):
    for n, row in enumerate(board):
        for i, cell in enumerate(row):
            if cell in ['🔴', '🔵']:
                if i < 4 and n > 2 and (board[n][i] == board[n-1][i+1] == board[n-2][i+2] == board[n-3][i+3]):
                    return cell
                if i > 2 and n > 2 and (board[n][i] == board[n-1][i-1] == board[n-2][i-2] == board[n-3][i-3]):
                    return cell
                if n < 3 and (board[n][i] == board[n+1][i] == board[n+2][i] == board[n+3][i]):
                    return cell
                if i < 4 and (board[n][i] == board[n][i+1] == board[n][i+2] == board[n][i+3]):
                    return cell
                if n == 0 and '⚪' not in board[n]:
                    return 'TIE'
    return 'NO_END'
