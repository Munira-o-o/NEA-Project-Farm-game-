import pygame

class Timer:
    def __init__(self,duration,func = None):
        #duration how long timer will be, function if we want to execute some code if the timer has ran out.
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    #Turns timer on
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
        #relative start time

    #Turns timer off  
    def deactivate(self):
        #Resets
        self.active = False
        self.start_time = 0
    
    #Checks timer has run out.
    def udpdate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
           
           if self.func and self.start_time != 0:
               self.func()
           self.deactivate()
           
           
           
            #checks if timer should have ran out
             #update will get updated conintously so current_time will always get our current time