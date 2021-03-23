import itertools, dataclasses

from copy import deepcopy
from init import Board

def callCustomBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]

    board_scores = [
        [90, -60, 10, 10, 10, 10, -60, 90],
        [-60, -80, 5, 5, 5, 5, -80, -60],
        [10, 5, 1, 1, 1, 1, 5, 10],
        [10, 5, 1, 1, 1, 1, 5, 10],
        [10, 5, 1, 1, 1, 1, 5, 10],
        [10, 5, 1, 1, 1, 1, 5, 10],
        [-60, -80, 5, 5, 5, 5, -80, -60],
        [90, -60, 10, 10, 10, 10, -60, 90]
    ]

    for i in victory_cell:
        c = cell.getColumnId(i[0])
        r = cell.getRowId(i[1])
        board_scores[r][c] += 20

    return CustomBot(victory_cell, cell, you, board_scores)

def CustomBot(victory_cell, cell, you, board_scores):
    color = 'B' if you == "BLACK" else 'W'

    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            possible_positions.append(c + r)

    if len(possible_positions) > 0:
       return minimax(cell, color, board_scores)

    else:
        return "NULL"

def minimax(cell, you, board_scores):
    return minimax_max(cell, you, board_scores, 1)

def minimax_max(cell, you, board_scores, depth):
    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, you):
            possible_positions.append(c + r)

    move_states = {move: play_move(cell, you, cell.getRowId(move[1]), cell.getColumnId(move[0])) for move in possible_positions}
    best_move = None
    best_value = None

    if len(possible_positions) > 0:
        if depth == 1:
            for move, state in move_states.items():
                if best_move == None or minimax_min(state, you, board_scores, depth + 1) > best_value:
                    best_move = move
                    #best_value = minimax_min(state, you, board_scores, depth + 1)

            #best_move = cell.getRowId(best_move[0])
            return best_move

        else:
            for move, state in move_states.items():
                if best_move == None or minimax_min(state, you, board_scores, depth + 1) > best_value:
                    best_value = minimax_min(state, you, board_scores, depth + 1)
            return best_value

    return compute_heuristic_score(cell, you, board_scores)

def minimax_min(cell, you, board_scores, depth):
    opponent = 'W' if you == 'B' else 'B'
    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, opponent):
            possible_positions.append(c + r)

    move_states = {move: play_move(cell, opponent, cell.getRowId(move[1]), cell.getColumnId(move[0])) for move in possible_positions}
    best_move = None
    best_value = None

    if len(possible_positions) > 0:
        if depth <= 3:
            for move, state in move_states.items():

                if best_move == None or minimax_max(state, you, depth + 1) < best_value:
                    best_move = move
                    best_value = minimax_max(state, you, depth + 1)

            return best_value

        else:
            for move, state in move_states.items():

                if best_value == None or compute_heuristic_score(state, you) < best_value:
                    best_value = compute_heuristic_score(state, you)

            return best_value
    return compute_heuristic_score(cell, you, board_scores)

def play_move(cell, you, i, j):
    new_board = []
    for row in list(cell.data):
        new_board.append(list(row[:]))

    lines = find_lines(cell, i, j, you)
    new_board[j][i] = you
    for line in lines:
        for u, v in line:
           new_board[v][u] = you
    final = []
    for row in new_board:
        final.append(tuple(row))
    return tuple(final)

def find_lines(board, i, j, you):
    lines = []
    for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        u = i
        v = j
        line = []

        u += xdir
        v += ydir
        found = False
        while u >= 0 and u < len(board.data) and v >= 0 and v < len(board.data):
            if board.data[v][u] == 'E':
                break
            elif board.data[v][u] == you:
                found = True
                break
            else:
                line.append((u, v))
            u += xdir
            v += ydir
        if found and line:
            lines.append(line)
    return lines


def compute_heuristic_score(cell, you, board_scores):
    p1_score = 0
    p2_score = 0
    for r in range(8):
        for c in range(8):
            if cell.data[r, c] == you:
                p1_score += board_scores[r][c]
            elif cell.data[r, c] != 'E':
                p2_score += board_scores[r][c]
    return p1_score - p2_score