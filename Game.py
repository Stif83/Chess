class Game:
    def __init__(self):
        from Board import Board
        self.board = Board()
        self.current_player = "W"
        self.game_over = False
        self.move_history = []

    def find_king(self,color):

        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.kind == "K" and piece.color == color:
                    return r,c
        return None

    def is_square_attacked(self,pos,by_color):
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == by_color:
                    possible_moves = piece.get_possible_moves((r, c), self.board)
                    if pos in possible_moves:
                        return  True
        return False

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False

        opponent_color = "B" if color == "W" else "W"
        return self.is_square_attacked(king_pos,opponent_color)


    def can_castle_kingside(self, color):
        if not self.board.castling_rights[color]["k"]:
            return False

        row = 7 if color == "W" else 0

        for col in [5,6]:
            if self.board.grid[row][col] is not None:
                return False

        if self.is_in_check(color):
            return False

        opponent_color = "B" if color == "W" else "W"

        for col in [5,6]:
            if self.is_square_attacked((row,col), opponent_color):
                return False
        return True

    def can_castle_queenside(self, color):
        if not self.board.castling_rights[color]["Q"]:
            return False

        row = 7 if color == "W" else 0

        for col in [1,2,3]:
            if self.board.grid[row][col] is not None:
                return False

        if self.is_in_check(color):
            return False

        opponent_color = "B" if color == "W" else "W"

        for col in [2,3]:
            if self.is_square_attacked((row, col), opponent_color):
                return False
        return True

    def perform_castle(self, color, side):
        row = 7 if color == "W" else 0

        if side == "K":
            king = self.board.grid[row][4]
            self.board.grid[row][6] = king
            self.board.grid[row][4] = None

            rook = self.board.grid[row][7]
            self.board.grid[row][5] = rook
            self.board.grid[row][7] = None

        else:
            king = self.board.grid[row][4]
            self.board.grid[row][2] = king
            self.board.grid[row][4] = None

            rook = self.board.grid[row][0]
            self.board.grid[row][3] = rook
            self.board.grid[row][0] = None


        self.board.castling_rights[color]["K"] = False
        self.board.castling_rights[color]["Q"] = False

    def update_castling_right(self,src):
        piece = self.board.piece(src) if hasattr(self.board, "piece") else self.board.grid[src[0]][src[1]]

        if piece and piece.kind == 'K':
            color = piece.color
            self.board.castling_rights[color]['K'] = False
            self.board.castling_rights[color]['Q'] = False

        elif piece and piece.kind == "R":
            color = piece.color
            row = 7 if color == "W" else 0

            if src == (row,0 ):
                self.board.castling_rights[color]['Q'] = False
            elif src == (row,7):
                self.board.castling_rights[color]['K'] = False

    def is_valid_move(self, src, dest):
        piece = self.board.piece(src) if hasattr(self.board, 'piece') else self.board.grid[src[0]][src[1]]

        if not piece or piece.color != self.current_player:
            return False

        if piece.kind =="k":
            king_row = 7 if piece.color == "W" else 0
            if src == (king_row,4):
                if dest == (king_row, 6) and self.can_castle_kingside(piece.color):
                    return True
                elif dest == (king_row, 2) and self.can_castle_queenside(piece.color):
                    return True

        if not self.board.inside(dest):
            return False

        dest_piece = self.board.piece(dest) if hasattr(self.board, 'piece') else self.board.grid[dest[0]][dest[1]]
        if dest_piece and dest_piece.color == piece.color:
            return False

        possible_moves = piece.get_possible_moves(src, self.board)
        if dest not in possible_moves:
            return False

        return self.would_move_be_legal(src,dest)


    def would_move_be_legal(self,src,dest):
        piece = self.board.grid[src[0]][src[1]]
        captured_piece = self.board.grid[dest[0]][dest[1]]

        self.board.grid[dest[0]][dest[1]] = piece
        self.board.grid[src[0]][src[1]] = None

        is_legal = not self.is_in_check(piece.color)

        self.board.grid[src[0]][src[1]] = piece
        self.board.grid[dest[0]][dest[1]] = captured_piece


        return is_legal

    def make_move(self, src,dest):
        if not self.is_valid_move(src,dest):
            return False

        piece = self.board.grid[src[0]][src[1]]

        if piece.kind == "K":
            king_row = 7 if piece.color == "W" else 0
            if src == (king_row,4) and dest == (king_row,6):
                self.perform_castle(piece.color, "K")
                self.current_player = "B" if self.current_player == "W" else "W"
                return True
            elif src == (king_row, 4) and dest == (king_row, 2):
                self.perform_castle(piece.color, "Q")
                self.current_player = "B" if self.current_player == "W" else "W"
                return True


        self.update_castling_right(src)

        self.board.grid[dest[0]][dest[1]] = piece
        self.board.grid[src[0]][src[1]] = None

        self.move_history.append((src,dest,piece))

        self.current_player = "B" if self.current_player == "W" else 'W'

        if self.is_check_mat(self.current_player):
            self.game_over = True

        return True

    def is_check_mat(self, color):
        if not self.is_in_check(color):
            return False

        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == color:
                    possible_moves = piece.get_possible_moves((r,c), self.board)
                    for move in possible_moves:
                        if self.would_move_be_legal((r,c), move):
                            return False
        return True


    def get_all_possible_moves(self, position):
        piece = self.board.piece(position)
        if not piece:
            return []
        all_moves = piece.get_possible_moves(position, self.board)
        valid_moves = []

        for move in all_moves:
            if self.board.inside(move):
                dest_piece = self.board.piece(move)
                if dest_piece is None or dest_piece.color != piece.color:
                    valid_moves.append(move)


        return valid_moves