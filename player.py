import pygame
from settings import *
from support import *
from os.path import join, dirname, abspath
from ttimer import Timer
from watering_can import WateringCan


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop):
        super().__init__(group)

        self.watering_can = WateringCan(capacity=20 )
        
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        
        
        #setup
        self.image = self.animations[self.status][self.frame_index]      
        self.rect = self.image.get_rect(center = pos)
        
        self.z = LAYERS['main'] #creates a 3rd dimension
        
        #movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 500
        
        #tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.seeds = ['corn', 'tomato','Eggplant', 'Pumpkin', 'Starfruit']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
        
        #collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate(-126,-70)

        #inventory
        self.item_inventory = {
            'wood':   10,
            'apple':  10,
            'corn':   10,
            'tomato': 10,
            'Eggplant': 5,
            'Pumpkin': 5,
            'Starfruit': 5,
        }

        self.seed_inventory = {
            'corn': 5,
            'tomato': 5,
            'Eggplant': 5,
            'Pumpkin': 5,
            'Starfruit': 5,
        }
        self.money = 200

        #interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

        #sound
        self.base_path = base_path = dirname(dirname(abspath(__file__)))
        self.watering = pygame.mixer.Sound(join(self.base_path, 'audio', 'water.mp3')) #pl
        self.watering.set_volume(0.2)

        #timer     
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }       
    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        
        if self.selected_tool == 'water':
            if self.watering_can.can_water():
                watered = self.soil_layer.water(self.target_pos)
                if watered:
                    self.watering_can.use() 
                    self.watering.play()      

                else:
                    if self.watering_can.near_water(self.hitbox): # not yet made
                        self.watering_can.refill()
  
    def get_target_pos(self):
        
        self.target_pos = self.rect.center +  PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
       
    
        pass

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)    #if less than 1 seed you cant plant
            self.seed_inventory[self.selected_seed] -= 1


    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                           'right_idle': [],'left_idle': [],'up_idle': [],'down_idle': [],
                           'right_hoe': [],'left_hoe': [],'up_hoe': [],'down_hoe': [],
                           'right_axe': [],'left_axe': [],'up_axe': [],'down_axe': [],
                           'right_water': [],'left_water': [],'up_water': [],'down_water': [],}
        base_path = dirname(dirname(abspath(__file__)))
        graphics_path = join(base_path, "graphics", "character")
        for animation in self.animations.keys():

            full_path = join(graphics_path, animation)
            self.animations[animation] = import_folder(full_path)

       

    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >=  len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]  

    def input(self):
        keys = pygame.key.get_pressed()
        #list of all keys potentially being pressed

        if not self.timers['tool use'].active and not self.sleep:

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status =  'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1  
                self.status =  'down'
            else:
                self.direction.y = 0 
        
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status =  'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1 
                self.status =  'right'
            else:
                self.direction.x = 0


        #tool inputs
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()   
                self.direction = pygame.math.Vector2()
                self.fame_index = 0

            #changing tools
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1         
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0  
                #ensures it doesnt go out of range                
                self.selected_tool = self.tools[self.tool_index]
                #to us pressing q might be pressing q  onec but to pguame it look slike were pressing q for a certain period og time and it keeps adding this plus 1 to the tool index continously. and running out of index values 

            #seed use
            
            if keys[pygame.K_r]:
                    
               

                    self.timers['seed use'].activate()   
                    self.direction = pygame.math.Vector2()
                    self.fame_index = 0

                #elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                        #self.timers['seed use'].activate()   
                        #self.direction = pygame.math.Vector2()
                        #self.fame_index = 0

                

            #change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1         
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0  
                #ensures it doesnt go out of range 
                self.selected_seed = self.seeds[self.seed_index]

            if keys[pygame.K_RETURN]:
               
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()
                   

                    else:
                        self.status = 'left_idle'
                        self.sleep = True
                elif self.watering_can.near_water(self.hitbox):
                    self.watering_can.refill() 
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + "_idle"

        if self.timers['tool use'].active:
           self.status = self.status.split('_')[0] + "_" + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.udpdate()

    def collision(self,direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: #moving to the right
                            self.hitbox.right =sprite.hitbox.left
                        if self.direction.x < 0: #moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0: #moving to down
                            self.hitbox.bottom =sprite.hitbox.top
                        if self.direction.y < 0: #moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery



    def move(self,dt):
        
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        self.pos.x += self.direction.x * self.speed * dt 
        self.hitbox.centerx = round(self.pos.x)                 #to avoid truncating and get glitches, also other stuff is to make sure hitbox moves along with the player
        self.rect.centerx = self.hitbox.centerx 
        self.collision('horizontal')
        

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)

