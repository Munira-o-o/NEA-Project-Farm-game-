import pygame
from settings import *

class Transition:
    def __init__(self, reset, player):
        #Setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        #overlay image  # take a black imgae and change its transparacy
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2 #How fast colour changes

    def play(self):

        #1 class reset: line 26
        #2 wake up player line 29
        #3 set the speed to -2 at the end of the transition
    
        #checs if colour is not black
        self.color +=self.speed
        if self.color <= 0:
            self.speed *= -2
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2  #allows it to reapeat #Resets speed
        self.image.fill((self.color, self.color,self.color))  #turning it white, but get darker
        self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT) # getting a white image  SPECIAL FLAGS blends the brighter the value it is the less visible it seems, so pure white is not seen makes it smoother