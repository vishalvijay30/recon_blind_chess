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

board = chess.Board()
# matrix with one dimension per unique piece that represents current belief about state of the board
# (updated by sensing / inference updates for both sides)
board_piece_level_matrix = []

# represents sensory input gained from sensing board
# 0 = nothing, 1 = something, -1 = ambiguous
board_visibility_matrix = []

engine = chess.uci.popen_engine("data/engines/stockfish-mac-64")

data_dir = 'data/'
image_dir = data_dir + 'images/'
cp_images = image_dir + 'chess-pieces/'
other_images = image_dir + 'other/'