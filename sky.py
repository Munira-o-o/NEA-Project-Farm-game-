import pygame
from settings import *
from os.path import join, dirname, abspath
from sprites import Generic
from support import import_folder
from random import randint, choice


class Sky:
    def __init__(self):
        #setup
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255,255,255]
        self.end_color = (38,101,189)

    #Draws black screen
    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:               #makes it so that color gradually get darker
                self.start_color[index] -= 2 *dt

        #Drawing
        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0,0), special_flags = pygame.BLEND_RGBA_MULT)


class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):
        
        #general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        #moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2,4)
            self.speed = randint(600,900)
    
    def update(self, dt):
        #movement
        if self.moving:
            self.pos += self.directionect * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        #timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        


class Rain:
    def __init__(self, all_sprites):
        #File path
        self.base_path = dirname(dirname(abspath(__file__)))
        self.all_sprites = all_sprites
        #Graphics
        self.rain_drops = import_folder(join(self.base_path, 'graphics', 'rain', 'drops'))
        self.rain_floor = import_folder(join(self.base_path, 'graphics', 'rain', 'floor') )
        self.floor_w, self.floor_h = pygame.image.load(join(self.base_path, 'graphics', 'world', 'ground.png')).get_size()
    
    #Randomly draws drops on the floor
    def create_floor(self):
        Drop(
            surf = choice(self.rain_floor),
            pos = (randint(0,self.floor_w),randint(0,self.floor_h)),                 #pos is a random position on the map in the intervals of o --> map wifht.height
            moving = False,
            groups = self.all_sprites, 
            z = LAYERS['rain floor']      
            )
    #Randomly draws drops in the sky.
    def create_drops(self):
        Drop(
            surf = choice(self.rain_drops),
            pos = (randint(0,self.floor_w),randint(0,self.floor_h)),                 #pos is a random position on the map in the intervals of o --> map wifht.height
            moving = False,
            groups = self.all_sprites, 
            z = LAYERS['rain drops']      
            )
    
    #Runs functions
    def update(self):
        self.create_floor()
        self.create_drops()