class Piece:
    VALID_KINDS = ["R", "Kn", "B", "K", "Q", "P", None]
    VALID_COLORS = ["W", "B", None]

    def __init__(self, kind, color):
        if kind not in self.VALID_KINDS:
            raise ValueError(f"Kind invalide: {kind}")
        if color not in self.VALID_COLORS:
            raise ValueError(f"Couleur invalide: {color}")

        self.kind = kind
        self.color = color

    def __str__(self):
        symbols = {
            'W': {'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'Kn': '♘', 'P': '♙'},
            'B': {'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'Kn': '♞', 'P': '♟'}
        }
        return symbols[self.color][self.kind]

    def __repr__(self):
        return f"Piece('{self.kind}', '{self.color}')"

    def get_possible_moves(self, pos, board):
        move_methodes = {
            "P": self._pawn_moves,
            "Kn": self._knight_moves,
            "B": self._bishop_moves,
            "R": self._rook_moves,
            "K": self._king_moves,
            "Q": self._queen_moves
        }

        return move_methodes[self.kind](pos,board)

    def _pawn_moves(self,pos,board):
        moves =[]
        r,c = pos
        direction = -1 if self.color == "W" else 1
        start_row = 6 if self.color == "W" else 1

        if board.inside((r+direction,c)) and board.grid[r + direction][c] is None:
            moves.append((r+ direction,c))

            if r == start_row and board.grid[r + 2*direction][c] is None:
                moves.append((r + 2 * direction,c))

        for direction_c in [-1,1]:
            new_pos = (r + direction, c+direction_c)
            if board.inside(new_pos):
                target = board.piece(new_pos)
                if target and target.color != self.color:
                    moves.append(new_pos)

        return moves

    def _rook_moves(self,pos,board):
        moves = []
        r,c = pos
        direction = [(0,1),(0,-1),(1,0),(-1,0)]

        for dr,dc in direction:
            for i in range(1,8):
                new_pos = (r + i*dr, c+ i*dc)
                if not board.inside(new_pos):
                    break

                target = board.piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                elif target.color != self.color:
                    moves.append(new_pos)
                    break
                else:
                    break

        return moves

    def _knight_moves(self, pos, board):
        moves = []
        r,c = pos
        direction = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

        for dr,dc in direction:
            new_pos = (r + dr,c + dc)
            if not board.inside(new_pos):
                continue

            target = board.piece(new_pos)
            if target is None or target.color != self.color:
                moves.append(new_pos)


        return moves

    def _bishop_moves(self, pos, board):
        moves = []
        r,c = pos
        direction = [(1,1),(-1,1),(1,-1),(-1,-1)]

        for dr,dc in direction:
            for i in range(1,8):
                new_pos = (r + i*dr, c + i*dc)
                if not board.inside(new_pos):
                    break
                target = board.piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                elif target.color != self.color:
                    moves.append(new_pos)
                    break
                else:
                    break

        return moves

    def _king_moves(self, pos, board):
        moves = []
        r,c = pos
        direction = [(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(0,-1)]

        for dr,dc in direction:
            new_pos = (r + dr, c +dc)
            if not board.inside(new_pos):
                break
            target = board.piece(new_pos)
            if target is None or target.color != self.color:
                moves.append(new_pos)

        if self.kind == "K":
            king_row = 7 if self.color == "W" else 0
            if pos == (king_row, 4):
                if board.castling_rights[self.color]["K"]:
                    moves.append((king_row,6))
                if board.castling_rights[self.color]["Q"]:
                    moves.append((king_row,2))
        return moves

    def _queen_moves(self, pos, board):
        return self._bishop_moves(pos,board) + self._rook_moves(pos, board)