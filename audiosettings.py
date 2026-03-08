import pygame
from os.path import join, dirname, abspath
def draw_text(text,font,color,x,y,surface):
   img = font.render(text,True,color)
   surface.blit(img,(x,y))

class AudioSettings:
    def __init__(self):
        #Setup
        self.screen = pygame.display.get_surface()
        self.base_path = dirname(dirname(abspath(__file__)))
        self.draw_text = draw_text

        #Graphics
        self.image = pygame.image.load(join(self.base_path, 'graphics', 'Setting menu.png' )).convert_alpha()
        self.exitimage = pygame.image.load(join(self.base_path, 'graphics', 'cross.png' )).convert_alpha()
        self.exitrect = self.exitimage.get_rect(center=(450,600))
        self.settings_rect = self.image.get_rect(center=(650,350))
        self.font = pygame.font.Font(join(self.base_path, 'font', 'settingpixels.ttf'), 20)
        
        
        
        #volume
        self.black_bar = pygame.image.load(join(self.base_path, 'graphics', 'black bar.png' )).convert_alpha()
        self.green_bar = pygame.image.load(join(self.base_path, 'graphics', 'green bar.png' )).convert_alpha()
        #Volume plus
        self.plus_img = pygame.image.load(join(self.base_path, 'graphics', 'Plus.png' )).convert_alpha()
        self.plus_img_pressed = pygame.image.load(join(self.base_path, 'graphics', 'plus_pressed.png' )).convert_alpha()
        #Volume minus
        self.minus_img = pygame.image.load(join(self.base_path, 'graphics', 'minus.png' )).convert_alpha()
        self.minus_img_pressed = pygame.image.load(join(self.base_path, 'graphics', 'minus_pressed.png' )).convert_alpha()
        
        #Volume plus/minus rectangles
        self.plus_rect = self.plus_img.get_rect(center=(720,270))
        self.minus_rect = self.minus_img.get_rect(center=(760,270))
        
        #Effect volume plus/minus rects
        self.effect_plus_rect = self.plus_img.get_rect(center=(720,470))
        self.effect_minus_rect = self.minus_img.get_rect(center=(760,470))
        
        #Volume setup
        self.start_x, self.start_y = 500, 230
        self.gap_size = 5
        self.segment_width = self.black_bar.get_width()
        self.segments = 10
        self.num_of_greens = 5
        self.volume = self.num_of_greens/self.segments


        #Effects setup
        self.effect_start_y =  430
        self.effect_num_of_greens = 5
        self.effect_segments = 10
        self.effect_volume = self.effect_num_of_greens/self.effect_segments
        
    #Effects functions
    def effect_change_volume(self):
        self.effect_volume = (self.effect_num_of_greens/self.effect_segments)

    def addeffectvolume(self):
        self.effect_num_of_greens = min(self.effect_segments, self.effect_num_of_greens +1)
        self.effect_change_volume()

    def minuseffectvolume(self):
        self.effect_num_of_greens = max(0, self.effect_num_of_greens -1)
        self.effect_change_volume()
    
    
    #Volume functions
    #Changes volume
    def change_volume(self):
        self.volume = (self.num_of_greens/self.segments)
    #Adds volume
    def addvolume(self):
        self.num_of_greens = min(self.segments, self.num_of_greens +1)
        self.change_volume()
    #Subtracts volume
    def minusvolume(self):
        self.num_of_greens = max(0, self.num_of_greens -1)
        self.change_volume()







        
         


    def run(self):
        #Drawing Icons 
        self.screen.fill('beige')
        self.screen.blit(self.image,self.settings_rect)
        #Buttons
        self.screen.blit(self.exitimage,self.exitrect)
        #plus/minus
        self.screen.blit(self.plus_img,self.plus_rect)
        self.screen.blit(self.minus_img, self.minus_rect)
        #effect plus/minus
        self.screen.blit(self.plus_img,self.effect_plus_rect)
        self.screen.blit(self.minus_img, self.effect_minus_rect)

        #Drawing Texts
        self.draw_text('music',self.font,'white',500,200,self.screen)
        self.draw_text('effects',self.font,'white',500,400,self.screen)

        
        #bar drawing logic
        for i in range(self.segments):
            x = self.start_x + i *(self.segment_width +self.gap_size)
            if i < self.num_of_greens :
                img = self.green_bar
            else:
                img = self.black_bar
            self.screen.blit(img, (x,self.start_y))
        #bar drawing logic for effects.
        for i in range(self.segments):
            x = self.start_x + i *(self.segment_width +self.gap_size)
            if i < self.effect_num_of_greens :
                img = self.green_bar
            else:
                img = self.black_bar
            self.screen.blit(img, (x,self.effect_start_y))
            
        pygame.display.update()
      
        

        
