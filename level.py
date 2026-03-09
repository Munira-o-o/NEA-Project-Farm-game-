import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from os.path import join, dirname, abspath
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu
from audiosettings import AudioSettings
import os

#Drawing text function
def draw_text(text,font,color,x,y,surface):
   img = font.render(text,True,color)
   surface.blit(img,(x,y))

class Level:
    def __init__(self,audiosettings,mouse_pos):
      #Setup
      self.display_surface = pygame.display.get_surface()
      self.mouse_pos = mouse_pos
      self.base_path = dirname(dirname(abspath(__file__)))
      self.screen = pygame.display.get_surface()
      
      #Sprites
      self.all_sprites = CameraGroup()
      self.water_sprites = pygame.sprite.Group() 
      self.collision_sprites = pygame.sprite.Group()
      self.tree_sprites = pygame.sprite.Group()
      self.interaction_sprites = pygame.sprite.Group()
      
      #Importing Text
      self.font = pygame.font.SysFont('Helvetica', 60)
      self.draw_text = draw_text
      self.audiosettings = audiosettings
      
     
      #Menu graphics
      self.menuimage = pygame.image.load(join(self.base_path, 'graphics', 'menu.png')).convert_alpha()
      self.hovermenuimage = pygame.image.load(join(self.base_path, 'graphics', 'hovermenu.png')).convert_alpha()
      self.menurect = self.menuimage.get_rect(center=(1232,47))

     
      #Outside classes
      self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
      self.setup()
      self.overlay = Overlay(self.player)
      self.transition = Transition(self.reset, self.player)
      

      # sky & rain
      self.rain = Rain(self.all_sprites)
      self.raining = randint(0,10) > 7
      self.soil_layer.raining = self.raining
      self.sky = Sky()
      self.raining = False
      

      #shop
      self.shop_active = False
      self.menu = Menu(self.player, self.toggle_shop)
      

      #music
      self.base_path = base_path = dirname(dirname(abspath(__file__)))
      self.success = pygame.mixer.Sound(join(self.base_path, 'audio', 'success.wav'))
      
      #Loading music
      pygame.mixer.music.load(join(self.base_path, 'audio', 'music.mp3'))
      pygame.mixer.music.play(loops=-1)
      
      
     
     

      

    def setup(self):
      #File paths
      base_path = dirname(dirname(abspath(__file__)))
      overlay_path = join(base_path, "data", "map")

      #|----------------Tiled software imports------------------|
      
      #Main ground image (bg)
      Generic(
      pos = (0,0), 
      surf = pygame.image.load(f'{join(overlay_path)}.png').convert_alpha(),
      groups = self.all_sprites,
      z = LAYERS['ground'])
     
      tmx_data = load_pygame(join(base_path,'data','map.tmx' ))
      

      #houseFloor & Furniture
      for layer in ['HouseFloor', 'HouseFurnitureBottom']:   #order matters
        for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
          Generic((x * TILE_SIZE ,y * TILE_SIZE),surf,self.all_sprites,LAYERS['house bottom'])                       #in tiled pos is 1, 0 we use tile size to get positon by pizels
      #House walls & furniture  
      for layer in ['HouseWalls', 'HouseFurnitureTop']:   #order matters
        for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
          Generic((x * TILE_SIZE ,y * TILE_SIZE),surf,self.all_sprites) 
      #path
      for x,y, surf in tmx_data.get_layer_by_name('path').tiles():
          Generic((x * TILE_SIZE ,y * TILE_SIZE),surf,self.all_sprites,LAYERS['ground plant']) 
      #fence
      for x,y, surf in tmx_data.get_layer_by_name('Fence').tiles():
          Generic((x * TILE_SIZE ,y * TILE_SIZE),surf,[self.all_sprites, self.collision_sprites])  #already in the main parameter

      #water
      water_frames = import_folder(join(base_path, 'graphics', 'water'))
      for x,y, surf in tmx_data.get_layer_by_name('Water').tiles():
          Water((x * TILE_SIZE ,y * TILE_SIZE), water_frames, [self.all_sprites,self.water_sprites])
      
      #wildflower
      for obj in tmx_data.get_layer_by_name('Decoration'):
          WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

       #trees
      for obj in tmx_data.get_layer_by_name('Trees'):
          Tree(
          pos = (obj.x, obj.y), 
          surf = obj.image, 
          groups = [self.all_sprites, self.collision_sprites,self.tree_sprites], 
          all_sprites = self.all_sprites,
          name = obj.name,
          player_add = self.player_add)
    
      #collision tiles
      for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():                                     
        Generic((x * TILE_SIZE ,y * TILE_SIZE),pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

      


      #player
      for obj in tmx_data.get_layer_by_name('Player'): #loads player in the start position
        if obj.name == 'Start':
          self.player = Player((obj.x, obj.y), 
          self.all_sprites,
          self.collision_sprites,
          self.tree_sprites, self.interaction_sprites,
          self.soil_layer, self.toggle_shop)
          #player is created after Generic cus otherwise player would dissapear into the ground
          
          #Sets the water sprites in the wateringCan sprite
          self.player.watering_can.water_sprites = self.water_sprites
         
        #Draws bed & trader as interaction sprites
          interaction = self.interaction_sprites
        if obj.name == 'Bed':
          Interaction((obj.x,obj.y),(obj.width, obj.height),self.interaction_sprites, 'Bed' )

        if obj.name == 'Trader':
          Interaction((obj.x,obj.y),(obj.width, obj.height),self.interaction_sprites, 'Trader')   #when enter is pressed it interacts with trader   #instance of player    
      
      #Drawing menu
      self.screen.blit(self.hovermenuimage if self.menurect.collidepoint(self.mouse_pos) else self.menuimage, self.menurect)   
      
      
      
      
    #Adds item & plays sound
    def player_add(self,item):
      self.player.item_inventory[item] += 1
      self.success.play()

    #determines shop is open
    def toggle_shop(self):
      self.shop_active = not self.shop_active   #toggles between true and false

    def reset(self):
      #plants
      self.soil_layer.update_plants()    #should be called before the other ones as when  it strts raining might water and then rain
      
      #soil
      #Removes water
      self.soil_layer.remove_water()
      #Randomises rain
      self.raining = randint(0,10) > 7
      self.soil_layer.raining = self.raining

      if self.raining:
        self.soil_layer.water_all()                      #makes it so that when new day is started it waters all teh existing soils.

      #day
      self.sky.start_color = [255, 255, 255]


      #apples
      for tree in self.tree_sprites.sprites():
        for apple in tree.apple_sprites.sprites():
          #Destroys apples
          apple.kill()
        tree.create_fruit()
    #Harvesting logic
    def plant_collision(self):
      if self.soil_layer.plant_sprites:
        for plant in self.soil_layer.plant_sprites.sprites():
          if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
            self.player_add(plant.plant_type)
            #Removes plant image
            plant.kill()
            Particle(    #Draws white outline after
              pos = plant.rect.topleft,
              surf = plant.image,
              groups = self.all_sprites,
              z = LAYERS['main']
            )
            self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')      #removes it so that player can harvest once
        

    def run(self, dt):
      #drawing logic
      self.display_surface.fill('blue')
      #Sets volume to audiosettings volume
      pygame.mixer.music.set_volume(self.audiosettings.volume)
      self.apply_effect_volume() 
      #Calls camera 
      self.all_sprites.custom_draw(self.player) 
      #Checks player has collided with sprite
      collided_interaction_sprite = pygame.sprite.spritecollide(self.player, self.interaction_sprites, False)  #spritecollide() expects the first argument to be a pygame.sprite.Sprite with a .rect. But you passed self (the Level object), and Level is not a Sprite, so it has no .rect
      if collided_interaction_sprite:
          if collided_interaction_sprite[0].name == 'Trader': 
            #Displays text
            self.draw_text('press ENTER to talk to shop keeper.',self.font,'white',0, 0,self.display_surface)                  #Inside Level.run() you currently call pygame.display.update() inside that collision block. Don’t do that inside Level—your main loop should update the display once per frame. 
            
          else:
            #Displays text for bed
            self.draw_text('press ENTER to SLEEP.',self.font,'white',0, 0,self.display_surface)                   
            


      #updates
      if self.shop_active:
        self.menu.update()  
      else: 
          self.all_sprites.update(dt)
          self.plant_collision()
      #Draws tool & seed icon
      self.overlay.display()

      #rain
      if self.raining and not self.shop_active:
        self.rain.update()
        self.soil_layer.raining = self.raining
        
        

      #day
      self.sky.display(dt) 
      
      

      #transition overlayed
      if self.player.sleep:  
        self.transition.play()
      

    #Changes volume of effect sounds
    def apply_effect_volume(self):
      vol = self.audiosettings.effect_volume
      #Action volume
      self.success.set_volume(vol)

      

      # player effect volume
      self.player.watering.set_volume(vol)

      # soil effect volume
      self.soil_layer.hoe_sound.set_volume(vol)
      self.soil_layer.plant_sound.set_volume(vol)

      # tree effect volume
      for tree in self.tree_sprites.sprites():
        tree.axe_sound.set_volume(vol)
      
class CameraGroup(pygame.sprite.Group):
  def __init__(self):
    super().__init__() # so the group works by itself
    self.display_surface = pygame.display.get_surface () # camera group can draw on the display directly
    self.offset = pygame.math.Vector2()

  def custom_draw(self, player):
    self.offset.x = player.rect.centerx - SCREEN_WIDTH/2
    self.offset.y = player.rect.centery - SCREEN_HEIGHT/2 #ensures player is always i the middle
    #Redraws srpites &layers
    for layer in LAYERS.values():
      for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #makes the object further down position y get drawn last dk what lambda key is though
        if sprite.z == layer:
          offset_rect = sprite.rect.copy()
          offset_rect.center -= self.offset
          self.display_surface.blit(sprite.image, offset_rect) # wouldnt be bale to draw sprite without # if layers wasnt here the order of code would mean items would disappear and get more confuisng/overwhelming at times.



          #|--------------Checking target & hitbox position--------------------|
          #if sprite == player:
           # pygame.draw.rect(self.display_surface, 'red', offset_rect, 5) # too look at hitbox and target position of tool
            #hitbox_rect = player.hitbox.copy()
            #hitbox_rect.center = offset_rect.center
            #pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
            #target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
            #pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)




#instead of putting all the sprites in anormal pygame group we are going to create a special kinda group via this group we are going to get the camera

