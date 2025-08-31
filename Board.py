from Piece import Piece

class Board:

    def __init__(self):
        self.grid = [[None]* 8 for _ in range(8)]
        self.setup_start_position()
        self.castling_rights ={"W":{'K': True, 'Q': True}, 'B': {'K': True, 'Q': True}}

    def setup_start_position(self):
        back = ["R","Kn","B","Q","K","B","Kn","R"]
        self.grid[7] = [Piece(kind,'W') for kind in back]
        self.grid[0] = [Piece(kind, 'B') for kind in back]
        self.grid[6] = [Piece("P", 'W') for _ in range(8)]
        self.grid[1] = [Piece("P", 'B') for _ in range(8)]

    def inside(self, rc):
        r,c, = rc; return 0 <= r < 8 and 0 <= c < 8

    def piece(self, rc):
        r,c = rc; return self.grid[r][c]

    def mouv(self, src, dest):
        pos = self.piece(src)
        self.grid[dest[0]][dest[1]] = pos
        self.grid[src[0]][src[1]] = None


