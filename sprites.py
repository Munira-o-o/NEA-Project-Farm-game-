import pygame
from settings import *
from os.path import join, dirname, abspath
from random import randint, choice
from ttimer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super(). __init__(groups)
        #Setup
        self.z = z
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        #Hitbox for object
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75) #if it is too large player might not be able to go behind it.
#Interaction objects
class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos,surf,groups)
        self.name = name

#Water objects
class Water(Generic):
    def __init__(self, pos, frames, groups):

        #water animation
        self.frames = frames
        self.frame_index = 0

        super().__init__( pos = pos, surf = self.frames[self.frame_index], groups = groups, z = LAYERS['water'])

    #Animates water tiles
    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >=  len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]  
    #Calls changes in FPS indpendant way.
    def update(self, dt):
        self.animate(dt)
#could call all the code in update this is more organised recusrion .

#Wildflower objects
class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super() .__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9) #Different hitbox

#Creates outline for disappearing objects
class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super(). __init__(pos, surf, groups ,z)
        self.start_time = pygame.time.get_ticks()                  #start_time is only take once,current time is repeatedly updated
        self.duration = duration

        #white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf


    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration: #Updates for a short period of time
            self.kill() #Destroys white otuline

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add, all_sprites):        #name =small/large
        super().__init__(pos,surf,groups)                    #tree inherits hitbox from generic
        base_path = dirname(dirname(abspath(__file__)))
        #tree attributes
        self.health = 5
        self.alive = True
        self.stump_surf = pygame.image.load(join(base_path, 'graphics', 'stumps', 'small.png' if name == 'Small' else 'large.png')).convert_alpha()
       
        self.all_sprites = all_sprites #pygame doesnt keep the groups in the same order everytime you start the game. This ensures that the apples are in the all_sprites group everytime
        
        #apples
   
        self.apples_surf = pygame.image.load(join(base_path,'graphics','fruit','apple.png' ))
        self.apple_pos =  APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        #Adds to player inventory
        self.player_add = player_add

        #sounds
        self.axe_sound = pygame.mixer.Sound(join(base_path, 'audio', 'axe.mp3'))

    def damage(self):

        #damaging the tree
        self.health -= 1

        #play sound
        self.axe_sound.play()

        #remove an apple
        if len(self.apple_sprites.sprites()) > 0:                         #ensures its not empty
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft, random_apple.image, self.all_sprites, LAYERS['fruit'])
            self.player_add('apple')
            random_apple.kill()                                          #kill is pygame function that removes the sprite from all groups.

    #Handles tree death
    def check_death (self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.all_sprites, LAYERS['fruit'], 300 )
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom) #loads in image of stump after death
            self.hitbox = self.rect.copy().inflate(-10,-self.rect.height *0.6)  #reduces hitbox
            self.alive = False
            self.player_add('wood')

    #Updates death changes
    def update(self, dt):
        if self.alive:
            self.check_death()

    #Redraws fruit
    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0,10) < 2:    #pos[0 tells me how far to the left of the tree i wanna go + the distance from edge of screen
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x,y), self.apples_surf, [self.apple_sprites, self.all_sprites], LAYERS['fruit'])
               