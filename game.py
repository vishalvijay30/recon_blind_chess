from chessboard import *

class ChessGame(BoxLayout):
    selected_square = None

    movebox_moves = 'This is a move'

    black_time = StringProperty()
    white_time = StringProperty()
    time_interval = 0.5

    def id_to_square(self, id, *args):
        id = int(id)
        row = abs(id // 8 - 8)
        column = id % 8
        return (row - 1) * 8 + column

    def id_to_san(self, id, *args):
        id = int(id)
        row = abs(id // 8 - 8)
        column = list(string.ascii_lowercase)[id % 8]
        return column + str(row)

    def san_to_id(self, san, *args):
        column = san[0]
        row = int(san[1])
        id_row = 64 - (row * 8)
        id_column = list(string.ascii_lowercase).index(column)
        id = id_row + id_column
        return id

    def create_legal_move_dict(self, *args):
        legal_moves = list(board.legal_moves)
        legal_move_dict = {}
        for move in legal_moves:
            move = str(move)
            if move[:2] in legal_move_dict:
                legal_move_dict[move[:2]] = \
                    legal_move_dict[move[:2]] + [move[2:]]
            else:
                legal_move_dict[move[:2]] = [move[2:]]

        return legal_move_dict

    def draw_board(self, *args):
        for child in self.children:
            if type(child) == ChessboardCentered:
                c_board = child.children[0]

        for num in range(64):
            button = ChessCell(id=str(num))
            c_board.add_widget(button)

    def update_board(self, *args):
        self.ids.board.update_positions(board)

    def select_piece(self, id, *args):
        square_num = self.id_to_square(id)
        square_san = self.id_to_san(id)
        piece = board.piece_at(square_num)

        legal_move_dict = self.create_legal_move_dict()

        if square_san in legal_move_dict:
            id_list = []
            for move in legal_move_dict[square_san]:
                id_list.append(self.san_to_id(move))
            self.ids.board.highlight_chesscell(id_list)
        self.selected_square = id

    def move_piece(self, id, *args):
        legal_move_dict = self.create_legal_move_dict()
        legal_ids = []
        try:
            for san in legal_move_dict[ \
                    self.id_to_san(self.selected_square)]:
                legal_ids.append(self.san_to_id(san))
        except KeyError:
            pass

        if int(id) in legal_ids:
            original_square = self.id_to_san(self.selected_square)
            current_square = self.id_to_san(id)
            move = chess.Move.from_uci(original_square + current_square)

            board.push(move)
            self.update_board()
            self.selected_square = None

            if not self.game_end_check():
                Clock.schedule_once(self.start_engine_move)

        else:
            self.update_board()
            self.select_piece(id)

    def start_engine_move(self, *args):
        threading.Thread(target=self.engine_move).start()

    def engine_move(self, *args, wtime=60 * 100, btime=60 * 100):
        engine.isready()
        engine.position(board)
        engine_move = engine.go(wtime=wtime, btime=btime)[0]
        str_move = str(engine_move)
        move = [self.san_to_id(x) for x in [str_move[:2], str_move[2:]]]

        self.ids.board.press_button(move[0])
        self.select_piece(move[0])
        Clock.schedule_once(partial(self.ids.board.press_button,
                                    move[1], is_engine_move=True, engine_move=engine_move), 1)

        Clock.schedule_once(self.game_end_check, 1)

    def setup_engine(self, *args):
        engine.uci()

    def turn(self, *args):
        return str(board.fen).split()[5]

    def chesscell_clicked(self, id, *args):
        if self.turn() == 'w':

            if id == self.selected_square:
                self.update_board()
            elif self.selected_square == None:
                self.select_piece(id)
            else:
                self.move_piece(id)

    def setup_clocks(self, *args, time=60, interval=0.1):
        self.black_time = str(time)
        self.white_time = str(time)
        self.interval = interval

    def end_game(self, reason, *args):

        print(reason)
        if 'white' in reason:
            print('Black won')
        elif 'black' in reason:
            print('White won')
        else:
            if board.result()[-1] == '1':
                print('Black won')
            elif board.result()[0] == '1':
                print('White won')
            else:
                print('Draw')

    def game_end_check(self, *args):
        if board.is_game_over():
            if board.is_checkmate():
                self.end_game('checkmate')
            elif board.is_stalemate():
                self.end_game('stalemate')
            elif board.is_insufficient_material():
                self.end_game('insufficient_material')
            elif board.is_seventy_five_moves():
                self.end_game('seventy five moves')
            elif board.is_fivefold_repetition():
                self.end_game('fivefold_repetition')
            return True

        return False