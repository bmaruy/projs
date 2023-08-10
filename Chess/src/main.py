import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from board import *
from piece import *

class Main:

    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()


    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger


        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                #first click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mY // SQSIZE
                    clicked_col = dragger.mX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                    
                #mouse movemetn
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                #mouse release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mY // SQSIZE
                        released_col = dragger.mX // SQSIZE

                        initial = Square(dragger.first_row, dragger.first_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()

                    dragger.undrag_piece()
                
                elif event.type == pygame.KEYDOWN:
                    def pawn_promotion(self):
                        if event.key == pygame.K_q:
                            board.squares[final.row][final.col].piece = Queen(piece.color)
                
                        elif event.key == pygame.K_b:
                            board.squares[final.row][final.col].piece = Bishop(piece.color)
                            
                        elif event.key == pygame.K_r:
                            board.squares[final.row][final.col].piece = Rook(piece.color)
                            
                        elif event.key == pygame.K_k:
                            board.squares[final.row][final.col].piece = Knight(piece.color)

                    if isinstance(piece, Pawn):
                        if final.row == 7 or final.row == 0:
                            pawn_promotion(self)

                    if event.key == pygame.K_r:
                        game.reset()

                #quitgame
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()




            pygame.display.update()

main = Main()
main.mainloop()