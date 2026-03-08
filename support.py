from os import walk
from os.path import join
import pygame

def import_folder(path):
    surface_list = []
    for dirpath,b, img_files in walk(path):
        for image in img_files:
            full_path = join(dirpath, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_folder_dict(path):           #used when we want to know what image we are working with.abs
    surface_dict = {}

    for dirpath,b, img_files in walk(path):
        for image in img_files:
            full_path = join(dirpath, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf 

    return surface_dict
