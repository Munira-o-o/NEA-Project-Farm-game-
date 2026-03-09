import pygame
from settings import *
from os.path import join, dirname, abspath
from pytmx.util_pygame import load_pygame
from support import *
from random import choice

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos,surf,groups):
        super(). __init__(groups)
        #Setup
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        #Setup
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water'] #Different layer to SoilTile

class Plant(pygame.sprite.Sprite):
    def __init__(self,plant_type, groups,soil,check_watered):
        super().__init__(groups)
        
        #setup
        self.plant_type = plant_type
        self.base_path = dirname(dirname(abspath(__file__))) 
        self.frames = import_folder(join(self.base_path, 'graphics', 'fruit', plant_type))
        self.soil = soil
        self.check_watered = check_watered
        
        #plant growing
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        #sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -6 if plant_type == 'corn' else -8                 #depending on height of the plant it will go up by y amount 
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
        self.z = LAYERS['ground plant']

    #Plant growth  
    def grow(self):
        #Checks if it is watered
        if self.check_watered(self.rect.center):
            #Growth depends on speed
            self.age += self.grow_speed #(In settings)

            #Less than max age
            if int(self.age) >= self.max_age:
                self.z = LAYERS['main']   #makes plant collidable wheen it is greather than 0. self.age might be 0.7
                self.hitbox = self.rect.copy().inflate(-26,self.rect.height * -0.4)
            #Greater than max age.
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True #When fully grown becomes harvestable

            self.image = self.frames[int(self.age)]   #age could be floating point
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))


class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):

        #sprite groups
        self.collision_sprites = collision_sprites
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        #graphics
        self.base_path = dirname(dirname(abspath(__file__)))
        self.soil_surf = pygame.image.load(join(self.base_path, 'graphics', 'soil','o.png' )).convert_alpha()
        self.soil_surfs = import_folder_dict(join(self.base_path, 'graphics', 'soil'))
        self.water_surfs = import_folder(join(self.base_path, 'graphics', 'soil_water') )

        #List of rectangle/soil.
        self.create_soil_grid()
        self.create_hit_rects()

        #Rain
        self.raining = False #Defaults rain as False

        #sounds

        #Hoe
        self.hoe_sound = pygame.mixer.Sound(join(self.base_path, 'audio', 'hoe.wav')) #sl
        self.hoe_sound.set_volume(0.4)

        #Planting
        self.plant_sound = pygame.mixer.Sound(join(self.base_path, 'audio', 'plant.wav')) #sl
        self.plant_sound.set_volume(0.2)

    #Grid storing soil info.
    def create_soil_grid(self):
        #Load bg image
        ground = pygame.image.load(join(self.base_path, 'data', 'map.png'))   
        h_tiles = ground.get_width()// TILE_SIZE                                                    #return the number of squres in the horzontal and vertical by using the ctual ground imae height
        v_tiles = ground.get_height() // TILE_SIZE

        self.grid =[[[] for col in range(h_tiles)] for row in range(v_tiles)]   #returns an empty list with the same number of elemnts as tiles       
      
        for x , y, __ in load_pygame(join(self.base_path, 'data', 'map.tmx')).get_layer_by_name('Farmable').tiles():    #takes all the tiles coloured green in the farmable layer and gets their x, y coordinates and adds an F in its place the rest is empty.
            self.grid[y][x].append('F')

    #creates a list of rectangles that the player can collide with
    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):  #retrieve both index of position in grid and the item inside it enumerate()
            for  index_col, cell in enumerate(row):
                #Checks if it is farmable
                if 'F' in cell: 
                    #Returns it back to a position
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect =  pygame.Rect(x,y, TILE_SIZE,TILE_SIZE)   #POSITION AND SIZE
                    self.hit_rects.append(rect)

    #Checks player has hit a valid grass tile
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                #Plays sound for hoe
                self.hoe_sound.play()

                x = rect.x // TILE_SIZE   #retrieves the row and column of the tile that got hit
                y = rect.y // TILE_SIZE
                #Checks if it is Farmable land
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')     #when player hits tile it replaces F with X to indicate a soil patch.
                    self.create_soil_tiles()
                    #If it is raining waters all the soil tiles at once.
                    if self.raining:
                        self.water_all()

    #Waters specific tiles
    def water(self,target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                #Retrieves x,y pos
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                
                #Checks whether its been watered already
                if 'W' in self.grid[y][x]:
                    return False #returns false when its already been watered

                #Adds capital W otherwise
                self.grid[y][x].append('W')
                #Draws water on top of tile.
                WaterTile( soil_sprite.rect.topleft ,choice(self.water_surfs),[self.all_sprites, self.water_sprites])
                return True

        return False #for when no soil gets watered
    
    #Waters all tile  (Raining)
    def water_all(self):
        for index_row, row in enumerate(self.grid): 
            for  index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:  #First checks if it is a soil tile
                    self.grid[index_row][index_col].append('W') #Adds capital W to signify Water tile.
                    #Retrieves x,y pos
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    #Draws water tile on the x,y pos.
                    WaterTile( (x,y) ,choice(self.water_surfs),[self.all_sprites, self.water_sprites])
    
    def remove_water(self):
        #Remove water sprite
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        #clean up grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    #Checks 'W' is in grid
    def check_watered(self,pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell =  self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered #Returns True/False

    #Seed planting
    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos): #Checks player has collided with a soil tile
                self.plant_sound.play() #Plays sound

                #Retrieves position of the soil.
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                #Checks if there is already a plant there and if it is a Soil tile
                if 'P' not in self.grid[y][x] and 'X' in self.grid[y][x]:
                    self.grid[y][x].append('P') #Adds capital P to show it has been planted
                    Plant(seed, [self.all_sprites,self.collision_sprites,  self.plant_sprites], soil_sprite, self.check_watered ) #Creates an instance of a plant
                   

    #Grows all plants at once.
    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()


    def create_soil_tiles(self):
        self.soil_sprites.empty()                 #gets rid of soil sprite
        for index_row, row in enumerate(self.grid):
            for  index_col, cell in enumerate(row):   
                if 'X' in cell:
                    
                    #tile options   #tells me what is in the neighbouring tiles
                    t = 'X' in self.grid[index_row -1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]
                    
                    tile_type = 'o'

                    #all side
                    if all((t,r,b,l)):
                        tile_type = 'x'
                   
                    #horizontal:
                    if l and not any((t,r,b)): tile_type = 'r'
                    if r and not any((t,l,b)): tile_type = 'l'                
                    if l and r and not any((t,b)): tile_type = 'lr'

                    #vertical
                    if t and not any((l,r,b)): tile_type = 'b'
                    if b and not any((r,l,t)): tile_type = 't'                
                    if t and b and not any((r,l)): tile_type = 'tb'

                    #corners
                    if l and b and not any((t,r)): tile_type = 'tr' 
                    if l and t and not any((r,b)): tile_type = 'br'
                    if r and b and not any((t,l)): tile_type = 'tl' 
                    if r and t and not any((l,b)): tile_type = 'bl'

                    # T SHAPES
                    if all((t,b,r)) and not l: tile_type = 'tbr'
                    if all((t,b,l)) and not r: tile_type = 'tbl'
                    if all((t,l,r)) and not b: tile_type = 'lrb'
                    if all((l,b,r)) and not t: tile_type = 'lrt'
                    


                    #Draws soil tile
                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE),     #initialises the SoilTile class when a tile is hit.
                    self.soil_surfs[tile_type], 
                    [self.all_sprites, self.soil_sprites]) 

        
        
        #requirements
        #if the area is farmable
        #if the soil has been watered 
        #if the soil has a plant already