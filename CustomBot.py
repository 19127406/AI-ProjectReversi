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

    return CustomBot(victory_cell, cell, you)


def CustomBot(victory_cell, cell, you):
    color = 'B' if you == "BLACK" else 'W'

    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            possible_positions.append(c + r)

    if len(possible_positions) > 0:
       return minimax(victory_cell, cell, color)

    else:
        return "NULL"


def minimax(victory_cell, cell, you):
    return minimax_max(victory_cell, cell, you, 1)


def minimax_max(victory_cell, cell, you, depth):
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
                if best_move == None or minimax_min(victory_cell, state, you, depth + 1) > best_value:
                    best_move = move
                    best_value = minimax_min(victory_cell, state, you, depth + 1)

            return best_move

        else:
            for move, state in move_states.items():
                if best_move == None or minimax_min(victory_cell, state, you, depth + 1) > best_value:
                    best_value = minimax_min(victory_cell, state, you, depth + 1)
            return best_value

    return compute_heuristic_score(victory_cell, cell, you)


def minimax_min(victory_cell, cell, you, depth):
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

                if best_move == None or minimax_max(victory_cell, state, you, depth + 1) < best_value:
                    best_move = move
                    best_value = minimax_max(victory_cell, state, you, depth + 1)

            return best_value

        else:
            for move, state in move_states.items():

                if best_value == None or compute_heuristic_score(victory_cell, state, you) < best_value:
                    best_value = compute_heuristic_score(victory_cell, state, you)

            return best_value
    return compute_heuristic_score(victory_cell, cell, you)


def play_move(cell, you, i, j):         #column i, row j
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


def find_lines(board, i, j, you):          #column i, row j
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


def compute_heuristic_score(victory_cell, cell, you):
    p1_score = 0
    p2_score = 0
    my_victory_cell = 0
    my_corner = 0
    new_board = Board()
    board_scores = [
            [120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]
        ]

    for i in [0, 7]:
        for j in [0, 7]:
            if cell[i][j] == you:
                my_corner += 1

    for i in victory_cell:
        c = new_board.getColumnId(i[0])
        r = new_board.getRowId(i[1])
        if cell[r][c] == you:
            my_victory_cell += 1

    if (my_victory_cell == 0 or my_victory_cell == 4) and my_corner >= 2:
        for i in victory_cell:
            c = new_board.getColumnId(i[0])
            r = new_board.getRowId(i[1])
            if board_scores[r][c] <= 0:
                board_scores[r][c] += 20
            else:
                board_scores[r][c] += 60

    for r in range(8):
        for c in range(8):
            if cell[r][c] == you:
                p1_score += board_scores[r][c]
            elif cell[r][c] != 'E':
                p2_score += board_scores[r][c]
    return p1_score - p2_score


