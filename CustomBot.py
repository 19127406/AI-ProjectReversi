import itertools, random

from array import *
from random import *
from copy import deepcopy
from init import Board

def callCustomBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]

    board_weights = [
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
        board_weights[r][c] = 100

    return CustomBot(victory_cell, cell, you, board_weights)

def CustomBot(victory_cell, cell, you, board_weights):
    color = 'B' if you == "BLACK" else 'W'

    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            possible_positions.append(c + r)

    if len(possible_positions) > 0:

        #chinh o day, bo random


        return random.choice(possible_positions)
    else:
        return "NULL"

