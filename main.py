import pygame, sys
from settings import *
from level import Level
from os.path import join, dirname, abspath
from audiosettings import AudioSettings
from menu import Menu
import os

def draw_text(text,font,color,x,y,surface):
   img = font.render(text,True,color)
   surface.blit(img,(x,y))




class Game:
    def __init__(self):
        pygame.init()
        #setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Grow a Farm")
        self.clock = pygame.time.Clock()
        self.mouse_pos = pygame.mouse.get_pos()
        
       #functions & classes
        self.audiosettings = AudioSettings()
        self.level = Level(self.audiosettings,self.mouse_pos)
        self.menu = Menu(self.level.player, self.level.toggle_shop)
        self.draw_text = draw_text
       
        self.base_path = dirname(dirname(abspath(__file__)))
        
        #-----------------graphics------------------------|  
        #bg
        self.image = pygame.image.load(join(self.base_path, 'graphics', 'background.png' )).convert_alpha()
        #exit
        self.exitimage = pygame.image.load(join(self.base_path, 'graphics', 'exit.png')).convert_alpha()
        self.hoverexitimage = pygame.image.load(join(self.base_path, 'graphics', 'hoverexit.png')).convert_alpha()
        self.exitrect = self.exitimage.get_rect(center=(60,660))
        #menu       
        self.menuimage = pygame.image.load(join(self.base_path, 'graphics', 'menu.png')).convert_alpha()
        self.hovermenuimage = pygame.image.load(join(self.base_path, 'graphics', 'hovermenu.png')).convert_alpha()
        self.menurect = self.menuimage.get_rect(center=(1232,47))   
        #exit
        self.returnimage = pygame.image.load(join(self.base_path, 'graphics', 'return.png')).convert_alpha()
        self.returnrect = self.returnimage.get_rect(center=(60,60))

        #Tutorial screen
        self.tutrect = pygame.Rect(170,70,1000,600)
        self.bordertutrect = pygame.Rect(0, 0, 1100, 670)
        self.bordertutrect.center = self.tutrect.center


        
        
        #Importing text
        self.font = pygame.font.Font(join(self.base_path, 'font', 'pixel.ttf'), 20)
        self.tutfont =  pygame.font.SysFont(join(self.base_path, 'font', 'arial'), 30)
        self.display_surface = pygame.display.get_surface()
        
        #buttons graphics and rectangels
        self.Button = pygame.image.load(join(self.base_path, 'graphics', 'button.png')).convert_alpha() 
        self.Buttonhover = pygame.image.load(join(self.base_path, 'graphics', 'hoverbuttonb.png')).convert_alpha()         
        self.playrect = self.Button.get_rect(center=(640,300))
        self.playrecthover = self.Buttonhover.get_rect(center=(640,300))        
        self.aboutrect = self.Button.get_rect(center=(640,375))  
        self.tutorialrect = self.Button.get_rect(center=(640,450))

        self.state = 'menu' #tracks game state 
       
        
            


     

        

        

    def where_is_mouse(self):
       
            
            self.previous_state = None
            #tracks pygame events.
            for event in pygame.event.get():
                #x button is clicked.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #handles all the game state changes in one function
                    if self.state == 'menu':
                        if self.exitrect.collidepoint(event.pos):
                            self.quit()
                        if self.playrect.collidepoint(event.pos):
                            self.state = "game"
                        elif self.aboutrect.collidepoint(event.pos):
                            self.state = "about"
                        elif self.tutorialrect.collidepoint(event.pos):
                            self.state = "tutorial"
                        elif self.menurect.collidepoint(event.pos):
                            self.previous_state = self.state
                            self.state = "settings"
                        
                    #return button in about and tutorial collision check.
                    elif self.state == 'about' or self.state == 'tutorial':
                        if self.returnrect.collidepoint(event.pos):
                            self.state = 'menu'
                    elif self.state == 'settings':
                        #exit button

                        if self.audiosettings.exitrect.collidepoint(event.pos):
                            self.state = 'game'
                            
                        #volume functions    
                        elif self.audiosettings.plus_rect.collidepoint(event.pos):
                            self.audiosettings.addvolume()
                        elif self.audiosettings.minus_rect.collidepoint(event.pos):
                            self.audiosettings.minusvolume()
                        #effect volume functions
                        elif self.audiosettings.effect_plus_rect.collidepoint(event.pos):
                            self.audiosettings.addeffectvolume()
                        elif self.audiosettings.effect_minus_rect.collidepoint(event.pos):
                            self.audiosettings.minuseffectvolume()
                        

                    elif self.state == 'game':
                        if self.menurect.collidepoint(event.pos):
                            self.previous_state = self.state
                            self.state = 'settings'
                        
            return self.mouse_pos        

    def run(self):
        while True:          
            self.mouse_pos = pygame.mouse.get_pos()
            mouse_pos = self.where_is_mouse()
            
            
            

            if self.state == 'menu':
                self.screen.blit(self.image, (0, 0))
                
                #play button
                self.screen.blit(self.hoverexitimage if self.exitrect.collidepoint(self.mouse_pos) else self.exitimage, self.exitrect)
                
                #menu button
                self.screen.blit(self.hovermenuimage if self.menurect.collidepoint(self.mouse_pos) else self.menuimage, self.menurect)

                # play button
                play_img = self.Buttonhover if self.playrect.collidepoint(self.mouse_pos) else self.Button
                self.screen.blit(play_img, self.playrect)
                self.draw_text('play', self.font, 'black', self.playrect.x + 60, self.playrect.y + 10, self.screen)

                # about button
                about_img = self.Buttonhover if self.aboutrect.collidepoint(self.mouse_pos) else self.Button
                self.screen.blit(about_img, self.aboutrect)
                self.draw_text('about', self.font, 'black', self.aboutrect.x + 49, self.aboutrect.y + 11, self.screen)

                # tutorial button
                tut_img = self.Buttonhover if self.tutorialrect.collidepoint(self.mouse_pos) else self.Button
                self.screen.blit(tut_img, self.tutorialrect)
                self.draw_text('tutorial', self.font, 'black', self.tutorialrect.x + 24, self.tutorialrect.y + 11, self.screen)

            
                self.clock.tick(60)
                pygame.display.flip()

            elif self.state == 'about':
                self.display_surface.fill('darkolivegreen3')
                #return button          
                self.screen.blit(self.returnimage, self.returnrect)
                #borders
                pygame.draw.rect(self.screen,'brown', self.bordertutrect)
                pygame.draw.rect(self.screen,'wheat1', self.tutrect)
                            
                           

                #text about game           
                self.draw_text('Welcome to Grow a Farm!',self.tutfont,'darkgreen',560,80,self.screen)
                self.draw_text('a relaxing farming adventure where your goal is to rebuild a forgotten piece of land into a thriving ',self.tutfont,'forestgreen',180,150,self.screen)
                self.draw_text('farm. you stumbled on a forgotten land which containd remants of a once thriving owner.',self.tutfont,'forestgreen',180,220,self.screen)
                self.draw_text('Over time, the land was abandoned and slowly fell into ruin. Now, it’s up to you to bring it back to ',self.tutfont,'forestgreen',180,290,self.screen)
                self.draw_text('life. Start with just a small plot of soil and a few seeds.',self.tutfont,'forestgreen',180,360,self.screen)
                self.draw_text('Plant crops, water them, harvest your produce, and sell what you grow to earn money.',self.tutfont,'forestgreen',180,430,self.screen)
                            
                           
                self.clock.tick(60)
                pygame.display.update()

            elif self.state == 'tutorial':
                self.display_surface.fill('darkolivegreen3')
                #return button       
                self.screen.blit(self.returnimage, self.returnrect)
                #borders
                pygame.draw.rect(self.screen,'brown', self.bordertutrect)
                pygame.draw.rect(self.screen,'wheat1', self.tutrect)
                            
                            
                #Tutorial text            
                self.draw_text('How to play',self.tutfont,'darkgreen',560,80,self.screen)
                self.draw_text('1.Two plant seeds have a tile dirrectly facing you and press R',self.tutfont,'forestgreen',180,150,self.screen)
                self.draw_text('2.To switch between tools press Q (tools should be displayed at the bottom left)',self.tutfont,'forestgreen',180,220,self.screen)
                self.draw_text('3.To switch between seeds press E',self.tutfont,'forestgreen',180,290,self.screen)
                self.draw_text('4. To access shop/new day press ENTER near the trader top left or near bed.',self.tutfont,'forestgreen',180,360,self.screen)
                self.draw_text('To chop trees or till soil press SPACEBAR',self.tutfont,'forestgreen',180,430,self.screen)
                            
                self.clock.tick(60)          
                pygame.display.update()
                #main game loop
            elif self.state == "game":
                dt =  self.clock.tick() / 1000
                
                #Calling run
                self.level.run(dt)
                #drawing menu icon
                self.screen.blit(self.hovermenuimage if self.menurect.collidepoint(self.mouse_pos) else self.menuimage, self.menurect)
                #displaying players money
                self.menu.display_money()
                #audiosettings 
            elif self.state == 'settings':
                #Draws audiosettings
                self.audiosettings.run()
                #Sets volume in settings
                pygame.mixer.music.set_volume(self.audiosettings.volume)
                
                
        
                
         
            
            
            pygame.display.update()
            
            

if __name__ == '__main__':
    game = Game()
    game.run()
    
 