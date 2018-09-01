from game import *

class ChessboardApp(App):
    def build(self):
        game = ChessGame()
        game.draw_board()
        game.update_board(board)
        game.setup_engine()

        Window.size = (1046, 718)

        Config.set('graphics', 'resizable', '1')
        Config.write()
        return game

if __name__ == '__main__':
   ChessboardApp().run()
