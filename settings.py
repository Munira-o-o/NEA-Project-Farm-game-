from pygame.math import Vector2

#Main window screen width & Height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#Tile size from Tiled software
TILE_SIZE = 64

#Where tool/seed icons should be drawn
OVERLAY_POSITIONS = {
    "tool" : (40, SCREEN_HEIGHT - 15),
    "seed" : (100, SCREEN_HEIGHT - 15)
}
#Where tools should be drawn.
PLAYER_TOOL_OFFSET = {
    "left" : Vector2(-50, 40),
    "right": Vector2(50,40),
    "up": Vector2(0,-10),
    "down": Vector2(0,50)
}
#decides the order of creation and what will go above what
LAYERS = {
    "water": 0,
    "ground": 1,
    "soil": 2,
    "soil water": 3,
    "rain floor": 4,
    "house bottom": 5,
    "ground plant": 6,
    "main": 7,
    "house top": 8,
    "fruit": 9,
    "rain drops": 10,
}

#Randomised positions of apples
APPLE_POS = {
    'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
    'Large': [(30, 24), (60,65), (50,50), (16,40), (45,50), (42,70)]
}
#Grow rates of plants
GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7,
    'Eggplant': 1,
    'Pumpkin': 0.7,
    'Starfruit':  0.5,
}
#How much money should be returned to player, when item is sold.
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 5,
    'tomato': 10,
    'Eggplant': 5,
    'Pumpkin': 10,
    'Starfruit':  25,

}
#Prices for seeds
PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5,
    'Eggplant': 4,
    'Pumpkin': 5,
    'Starfruit':  10,

}