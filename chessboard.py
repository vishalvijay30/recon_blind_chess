from utils import *

class Chessboard(GridLayout):
    def gen_image_dict(self, *args, image_dir=cp_images):
        if image_dir[-1] != '/':
            image_dir += '/'
        d = {'p': image_dir + 'BlackPawn.png',
             'r': image_dir + 'BlackRook.png',
             'n': image_dir + 'BlackKnight.png',
             'b': image_dir + 'BlackBishop.png',
             'q': image_dir + 'BlackQueen.png',
             'k': image_dir + 'BlackKing.png',
             'P': image_dir + 'WhitePawn.png',
             'R': image_dir + 'WhiteRook.png',
             'N': image_dir + 'WhiteKnight.png',
             'B': image_dir + 'WhiteBishop.png',
             'Q': image_dir + 'WhiteQueen.png',
             'K': image_dir + 'WhiteKing.png',
             }
        return d

    def update_positions(self, *args):
        # Can't call ids directly for some reason so ...
        # Dictionary mapping ids to children (Chess cells)
        ids = {child.id: child for child in self.children}

        # Get the board positions from the fen
        b = str(board.fen).split()[4].replace('/', '')[7:]

        print("harambe", b)

        # Replace empty spaces with dots
        for num in range(1, 10):
            b = b.replace(str(num), '.' * num)

        # Generate dictionary that maps pieces to images
        image_dict = self.gen_image_dict()

        # Map Chess cell ids to board positions
        for x in zip(range(64), list(b)):
            if x[1] != '.':
                image = image_dict[x[1]]
            else:
                image = other_images + 'transparency.png'
            ids[str(x[0])].children[0].source = image

    def highlight_chesscell(self, id_list, *args):
        self.update_positions()
        ids = {child.id: child for child in self.children}
        highlight_image = other_images + 'highlight.png'
        for id in id_list:
            ids[str(id)].children[0].source = highlight_image

    def on_size(self, *args):
        board_dimensions = sorted([self.width, self.height])[0]

        self.row_force_default = True
        self.col_force_default = True

        self.row_default_height = board_dimensions / self.rows
        self.col_default_width = board_dimensions / self.columns

    def button_down(self, id, *args):
        ids = {child.id: child for child in self.children}

        background_down = 'atlas://data/images/defaulttheme/button_pressed'
        ids[id].background_normal = background_down

    def button_up(self, id, *args):
        ids = {child.id: child for child in self.children}

        background_normal = 'atlas://data/images/defaulttheme/button'
        ids[id].background_normal = background_normal

    def press_button(self, id, *args, is_engine_move=False, engine_move=''):
        id = str(id)
        self.button_down(id)

        if is_engine_move == False:
            Clock.schedule_once(partial(self.button_up, id), .7)
        else:
            Clock.schedule_once(partial(self.button_up, id), .3)
            board.push(engine_move)
            Clock.schedule_once(self.update_positions)

        # print("belief:\n")
        # update_board_piece_level_matrix(board_piece_level_matrix, [chess.WHITE])
        # print_board_piece_level_matrix(board_piece_level_matrix)
        # print("sensory input:\n", board_visibility_matrix)

    def engine_move(self, move, *args):
        ids = {child.id: child for child in self.children}
        starter_pos = move[0]
        current_pos = move[1]

        self.press_button(starter_pos)

class ChessboardCentered(BoxLayout):
    def on_size(self, *args):
        board_dimensions = sorted([self.width, self.height])[0]
        self.padding = [(self.width-board_dimensions)/2,
            (self.height-board_dimensions)/2, 0, 0]

class ChessCell(Button):
    pass

class Sidebar(FloatLayout):
    pass

class ChessClockContainer(BoxLayout):
    pass

class BlackChessClock(BoxLayout):
    pass

class ChessClockDisplay(TextInput):
    pass

class ChessClockButton(Button):
    pass

class WhiteChessClock(BoxLayout):
    pass

class Movebox(BoxLayout):
    pass