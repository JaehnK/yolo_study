from collections import OrderedDict as od
import os
import json

from PIL import Image

def prop_open(path:str) -> dict:
    path = os.path.join(path, 'crop_area.properties')
    print(path)
    cropProp = dict()
    with open(path, mode = 'r', ) as f:
        content = f.readlines()
        for i, con in enumerate(content):
            element = con.split('=')
            crops = [int(e) for e in element[1].split(',')]
            cropProp[element[0]] = {'crop_raw' : crops, 'img_size' : None, 'crop_norm' : list()}
    return cropProp

def get_imgsize(paths:list, img_infos:dict):
    
    return


def main():
    path = './foodSample'
    dirs = os.listdir(path)
    img_infos = dict()
    for dir in dirs:
        dir_path = os.path.join(path, dir)
        img_infos.update(prop_open(dir_path))
        
        imgs_path = [os.path.join(dir_path, img) for img in os.listdir(dir_path) if img.endswith('jpg')]
        print(imgs_path)
        #print(img_infos)

if __name__ == '__main__':
    main()