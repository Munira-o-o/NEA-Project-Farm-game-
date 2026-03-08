import pygame
from os.path import join, dirname, abspath
class WateringCan:
    def __init__(self, capacity =1):
        #Setup
        self.capacity = capacity
        self.amount = capacity
        self.water_sprites = None #this was set in level
        #File path
        self.base_path = dirname(dirname(abspath(__file__)))
        self.display_surface = pygame.display.get_surface()

        #Graphics
        self.bar_full = pygame.image.load(join(self.base_path,'graphics', 'waterbarfull.png')).convert_alpha()
        self.bar_empty = pygame.image.load(join(self.base_path,'graphics', 'waterbarempty.png')).convert_alpha()
        
        #Water surfaces 
        self.water_surf = None
        


    #Checks water bar is full
    def is_full(self):
        return self.amount == self.capacity
    
    #Checks water bar is empty
    def is_empty(self):
        return self.amount == 0
    #Checks if if they can water
    def can_water(self):
        return self.amount > 0 #return true or false

    #Reduces amount when they use it.
    def use(self):
        if self.amount > 0:
            self.amount -= 1
            return True
        return False   #can use this later to verify if the player can use it

    #Resets amount to capacity
    def refill(self):
        self.amount = self.capacity

    def draw(self):   

    
        #Sets position
        x, y = 1220, 560

        #Draws empty bar
        self.water_rect = self.bar_empty.get_rect(topleft=(x, y))
        self.display_surface.blit(self.bar_empty, self.water_rect)

        
        ratio =  self.amount / self.capacity
        #Resetting height
        full_width = self.bar_full.get_width()
        full_height = self.bar_full.get_height()
        fill_height = int(full_height * ratio)
        #makes it remove from the top instead
        offset_y = full_height - fill_height
        
        #Drawing full bar on top
        if fill_height > 0:
            fill_area = pygame.Rect(0, offset_y, full_width, fill_height)  
            self.display_surface.blit(self.bar_full, (x, y +offset_y), area=fill_area)



    def near_water(self,player_hitbox):
         #checks if their is no watersprites near the players hitbox
        if not self.water_sprites: 
            return False  
        #expands the players hitbox when enter is pressed
        test_rect = player_hitbox.inflate(12,12)

        #checks if the surronding objects are water sprites
        for water in self.water_sprites:
            if water.rect.colliderect(test_rect):
                return True
        return False