import itertools
import dataclasses
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
        if board_scores[r][c] <= 0:
            board_scores[r][c] += 20
        else:
            board_scores[r][c] += 75

    return CustomBot(victory_cell, cell, you, board_scores)


def CustomBot(victory_cell, cell, you, board_scores):
    color = 'B' if you == "BLACK" else 'W'

    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            possible_positions.append(c + r)

    if len(possible_positions) > 0:
       return minimax(victory_cell, cell, color, board_scores)

    else:
        return "NULL"


def minimax(victory_cell, cell, you, board_scores):
    return minimax_max(victory_cell, cell, you, board_scores, 1)


def minimax_max(victory_cell, cell, you, board_scores, depth):
    possible_positions = []
    if type(cell) is tuple:
        new_board = Board()
        for i in range(8):
            for j in range(8):
                new_board.data[i][j] = cell[i][j]

        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            if new_board.isPlaceable(c + r, you):
                possible_positions.append(c + r)
        move_states = {move: play_move(new_board, you, new_board.getColumnId(move[0]), new_board.getRowId(move[1])) for move in
                       possible_positions}
    else:
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            if cell.isPlaceable(c + r, you):
                possible_positions.append(c + r)
        move_states = {move: play_move(cell, you, cell.getColumnId(move[0]), cell.getRowId(move[1])) for move in
                       possible_positions}

    best_move = None
    best_value = None

    if len(possible_positions) > 0:
        if depth == 1:
            for move, state in move_states.items():
                if best_move == None or minimax_min(victory_cell, state, you, board_scores, depth + 1) > best_value:
                    best_move = move
                    best_value = minimax_min(victory_cell, state, you, board_scores, depth + 1)

            return best_move

        else:
            for move, state in move_states.items():
                if best_move == None or minimax_min(victory_cell, state, you, board_scores, depth + 1) > best_value:
                    best_value = minimax_min(victory_cell, state, you, board_scores, depth + 1)
            return best_value

    return compute_heuristic_score(victory_cell, cell, you, board_scores)


def minimax_min(victory_cell, cell, you, board_scores, depth):
    opponent = 'W' if you == 'B' else 'B'
    possible_positions = []

    new_board = Board()
    for i in range(8):
        for j in range(8):
            new_board.data[i][j] = cell[i][j]

    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if new_board.isPlaceable(c + r, opponent):
            possible_positions.append(c + r)
    move_states = {move: play_move(new_board, opponent, new_board.getColumnId(move[0]), new_board.getRowId(move[1])) for move in
                   possible_positions}

    best_move = None
    best_value = None

    if len(possible_positions) > 0:
        if depth <= 3:
            for move, state in move_states.items():

                if best_move == None or minimax_max(victory_cell, state, you, board_scores, depth + 1) < best_value:
                    best_move = move
                    best_value = minimax_max(victory_cell, state, you, board_scores, depth + 1)

            return best_value

        else:
            for move, state in move_states.items():

                if best_value == None or compute_heuristic_score(victory_cell, state, you, board_scores) < best_value:
                    best_value = compute_heuristic_score(victory_cell, state, you, board_scores)

            return best_value
    return compute_heuristic_score(victory_cell, cell, you, board_scores)


def play_move(cell, you, i, j):          # column i, row j
    """
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
    """
    new_board = Board()
    changing_cells = new_board.(position, color) + [(row_id, column_id)]
    for (r, c) in changing_cells:
        self.data[r, c] = color


def compute_heuristic_score(victory_cell, cell, you, board_scores):
    p1_score = 0
    p2_score = 0
    my_victory_cell = 0
    new_board = Board()

    for i in victory_cell:
        c = new_board.getColumnId(i[0])
        r = new_board.getRowId(i[1])
        if (type(cell) is tuple and cell[r][c] == you) or (type(cell) is Board and cell.data[r][c] == you):
            my_victory_cell += 1

    if my_victory_cell >= 3:
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

    for r in range(8):
        for c in range(8):
            if (type(cell) is tuple and cell[r][c] == you) or (type(cell) is Board and cell.data[r][c] == you):
                p1_score += board_scores[r][c]

            elif (type(cell) is tuple and cell[r][c] != 'E') or (type(cell) is Board and cell.data[r][c] != 'E'):
                p2_score += board_scores[r][c]
    return p1_score - p2_score


