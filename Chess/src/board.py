import pygame

from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        #console board move update
        if self.squares[final.row][final.col].has_team_piece(piece.color):
            #print("first")
            if (self.squares[final.row][final.col].isrook(piece.color) and self.squares[initial.row][initial.col].isbishop(piece.color)) or (self.squares[final.row][final.col].isbishop(piece.color) and self.squares[initial.row][initial.col].isrook(piece.color)):
                piece = Bishop_Rook(piece.color)
            elif (self.squares[final.row][final.col].isbishop(piece.color) and self.squares[initial.row][initial.col].isknight(piece.color)) or (self.squares[final.row][final.col].isknight(piece.color) and self.squares[initial.row][initial.col].isbishop(piece.color)):
                piece = Bishop_Knight(piece.color)
            elif (self.squares[final.row][final.col].isrook(piece.color) and self.squares[initial.row][initial.col].isknight(piece.color)) or (self.squares[final.row][final.col].isknight(piece.color) and self.squares[initial.row][initial.col].isrook(piece.color)):
                piece = Rook_Knight(piece.color)
            elif (self.squares[final.row][final.col].isqueen(piece.color) and self.squares[initial.row][initial.col].isknight(piece.color)) or (self.squares[final.row][final.col].isknight(piece.color) and self.squares[initial.row][initial.col].isqueen(piece.color)):
                piece = Queen_Knight(piece.color)

        self.squares[initial.row][initial.col].piece = None 
        self.squares[final.row][final.col].piece = piece

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        #move
        piece.moved = True

        #clears valid moves
        piece.moves = []

        #if self.squares[final.row][final.col].has_team_piece:
            #self.squares[initial.row][initial.col].piece = None
            #self.squares[final.row][final.col].piece = Square(final.row, final.col, Bishop_Rook(piece.color))
        #else:
        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.moves

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        '''
            calculate all valid moves of a specific piece 
        '''

        def pawn_moves():
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)
                        #blocked
                    else: break
                else: break
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        piece.add_moves(move)

        def knight_moves():

            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    initial = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final = Square(possible_move_row, possible_move_col, final_piece)
                    move = Move(initial, final)
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color): 
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                print("1")
                                piece.add_moves(move)
                            else: break
                        else:
                            print("1")
                            piece.add_moves(move)
                    elif (self.squares[possible_move_row][possible_move_col].isrook(piece.color) or self.squares[possible_move_row][possible_move_col].isbishop(piece.color) or self.squares[possible_move_row][possible_move_col].isqueen(piece.color)):
                        # and self.squares[row][col].isknight():
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                        

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:

                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)

                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                            break
                        

                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            if self.squares[possible_move_row][possible_move_col].isbishop(piece.color) and not self.squares[row][col].isbishop(piece.color) and self.squares[row][col].fusionable() and not self.squares[row][col].isqueen(piece.color):
                                # and not self.squares[row][col].fusionp():
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                    else:
                                        piece.add_moves(move)
                                break
                            elif self.squares[possible_move_row][possible_move_col].isrook(piece.color) and not self.squares[row][col].isrook(piece.color) and self.squares[row][col].fusionable() and not self.squares[row][col].isqueen(piece.color):
                            # and not self.squares[row][col].fusionp():
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                    else:
                                        piece.add_moves(move)
                                break
                            elif self.squares[possible_move_row][possible_move_col].isqueen(piece.color) and self.squares[row][col].isknight(piece.color):
                                # and not self.squares[row][col].fusionp():
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                    else:
                                        piece.add_moves(move)
                                break
                            elif self.squares[possible_move_row][possible_move_col].isknight(piece.color) and self.squares[row][col].fusionable():
                                # and not self.squares[row][col].fusionp():
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                    else:
                                        piece.add_moves(move)
                                break
                            else: break
                        '''elif self.squares[possible_move_row][possible_move_col].isbishop(piece.color):
                            
                            if bool:
                                if self.squares[row][col].isrook(piece.color):
                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                    else:
                                        piece.add_moves(move)
                            break

                        elif self.squares[possible_move_row][possible_move_col].isrook(piece.color):
                            #print("torook")
                            #if self.squares[row][col].isbishop(piece.color):
                                #print("torook2")
                            # and self.squares[row, col].isrook(piece.color)) or (self.squares[possible_move_row][possible_move_col].isrook(piece.color) and self.squares[row, col].isbishop(piece.color))): 
                            #and self.squares[possible_move_row][possible_move_col].has_team_piece:
                            if bool:
                                if self.squares[row][col].isrook(piece.color):
                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                else:
                                    piece.add_moves(move)
                            break

                        elif self.squares[possible_move_row][possible_move_col].isknight(piece.color):
                            if bool:
                                if self.squares[row][col].isrook(piece.color) or self.squares[row][col].isbishop(piece.color) or self.squares[row][col].isqueen(piece.color):

                                    if not self.in_check(piece, move):
                                        piece.add_moves(move)
                                else:
                                    piece.add_moves(move)
                            break'''


                    else: break

                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr 
                
        def king_moves():
            adjs = [
                (row-1, col-1),
                (row-1, col),
                (row-1, col+1),
                (row, col+1),
                (row+1, col+1),
                (row+1,col),
                (row+1, col-1),
                (row, col-1)
            ]


            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                            else: break
                        else:
                            piece.add_moves(move)
            
             # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                #adds left rook to king
                                piece.left_rook = left_rook

                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                left_rook.add_moves(move)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                piece.add_moves(move)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_moves(moveR)
                                        # append new move to king
                                        piece.add_moves(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_moves(moveR)
                                    # append new move king
                                    piece.add_moves(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                                #rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                right_rook.add_moves(move)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                piece.add_moves(move)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_moves(moveR)
                                        # append new move to king
                                        piece.add_moves(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_moves(moveR)
                                    # append new move king
                                    piece.add_moves(moveK)




        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece, Knight): knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])

        elif isinstance(piece, King):
            king_moves()

        elif isinstance(piece, Bishop_Rook):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
        
        elif isinstance(piece, Bishop_Knight):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
            knight_moves()

        elif isinstance(piece, Rook_Knight):
            straightline_moves([
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
            knight_moves()

        elif isinstance(piece, Queen_Knight):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
            knight_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #king
        self.squares[row_other][4] = Square(row_other, 4, King(color))