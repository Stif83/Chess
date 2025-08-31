import tkinter as tk
from tkinter import messagebox
from Game import Game


class ChessGUI:
    def __init__(self,root):

        self.root = root
        self.root.title("Echec")
        self.canvas = tk.Canvas(root, width=480, height=480)
        self.canvas.pack()

        self.game = Game()
        self.selected = None
        self.possible_moves = []

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.cancel_selection)

        self.root.bind("<Escape>", self.cancel_selection)
        self.draw_board()


    def draw_board(self):
        self.canvas.delete("all")
        color = ["#F0D9B5", "#B58863"]
        for r in range(8):
            for c in range(8):
                x1,y1 = c*60, r*60
                x2,y2 = x1+60, y1 + 60
                square_color = color[(r+c)%2]

                if (r,c) in self.possible_moves:
                    square_color = "#90EE90"

                self.canvas.create_rectangle(x1,y1,x2,y2, fill=square_color, outline="black")

                piece = self.game.board.grid[r][c]
                if piece:
                    piece_text = str(piece)
                    self.canvas.create_text(x1+30,y1+30, text=piece_text, font=("Arial", 32))
            if self.selected:
                r,c, = self.selected
                self.canvas.create_rectangle(c*60,r*60, c*60+60,r*60+60, outline="yellow", width=3)

    def show_possible_moves(self, pos):
        self.possible_moves = self.game.get_all_possible_moves(pos)
        self.draw_board()

    def on_click(self, event):
        c,r = event.x//60, event.y//60

        if not (0 <= r < 8 and 0 <= c < 8):
            return

        if self.selected is None:
            piece = self.game.board.piece((r, c))
            if piece and piece.color == self.game.current_player:
                self.selected = (r, c)
                self.show_possible_moves((r,c))

        else:
            src = self.selected
            dest = (r,c)
            if self.game.make_move(src, dest):
                self.selected = None
                self.possible_moves = []

                if self.game.game_over:
                    winner = "Blancs" if self.game.current_player == "W" else "Noirs"
                    messagebox.showinfo("Jeu terminé", f"Les {winner} ont gagné!")
            else:
                piece = self.game.board.piece(dest)
                if piece and piece.color == self.game.current_player:
                    self.selected = dest
                    self.show_possible_moves(dest)
                else:
                    self.cancel_selection()
        self.draw_board()


    def cancel_selection(self, event=None):
            self.selected = None
            self.possible_moves = []
            self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()

