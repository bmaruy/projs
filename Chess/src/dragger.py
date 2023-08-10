import pygame
from const import *


class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mX = 0
        self.mY = 0
        self.first_row = 0
        self.first_col = 0

    def update_blit(self, surface):
        self.piece.set_texture(size = 128)
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = (self.mX, self.mY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, pos):
        self.mX, self.mY = pos

    def save_initial(self, pos):
        self.first_row = pos[1] // SQSIZE
        self.first_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    
