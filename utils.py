from kivy.app import App
from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.clock import Clock

from kivy.config import Config

from kivy.properties import StringProperty

import chess
import chess.uci

from functools import partial
import threading
import string

import numpy as np

board = chess.Board()

engine = chess.uci.popen_engine("data/engines/stockfish-mac-64")

data_dir = 'data/'
image_dir = data_dir + 'images/'
cp_images = image_dir + 'chess-pieces/'
other_images = image_dir + 'other/'


def update_board_piece_level_matrix(matrix, colors):
    for p in chess.PIECE_TYPES:
        piece_level_matrix = [[0 for j in range(8)] for i in range(8)]
        for c in colors:
            for idx in board.pieces(p, c):
                piece_level_matrix[int(idx / 8)][idx % 8] = 1

            matrix[chess.PIECE_NAMES[p]] = piece_level_matrix


def print_board_piece_level_matrix(to_print):
    for key in chess.PIECE_NAMES:
        if key != "":
            print(key + ":")
            matrix = to_print[key]
            print(np.matrix(matrix))
    print("\n")

# matrix with one dimension per unique piece that represents current state of the board (your pieces only)
# (updated by sensing / inference updates for both sides)
board_piece_level_matrix = dict()
update_board_piece_level_matrix(board_piece_level_matrix, [chess.WHITE])
print_board_piece_level_matrix(board_piece_level_matrix)

# represents sensory input gained from sensing board (last round seen only)
# 0 = nothing, 1 = something, -1 = ambiguous
board_visibility_matrix = []

