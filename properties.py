from collections import OrderedDict as od
import os
import json

from PIL import Image

def prop_open(path: str) -> dict:
    path = os.path.join(path, 'crop_area.properties')
    print(f"Reading file: {path}")
    crop_prop = dict()
    with open(path, mode='r') as f:
        content = f.readlines()
    for con in content:
        element = con.strip().split('=')
        if len(element) == 2:
            key, value = element
            try:
                crops = [int(e) for e in value.split(',')]
                if len(crops) == 4:  # Ensure we have 4 values for x, y, width, height
                    crop_prop[key] = {'crop_raw': crops, 'img_size': None, 'crop_norm': list()}
                else:
                    print(f"Warning: Skipping invalid data for {key}: {value}")
            except ValueError:
                print(f"Warning: Could not parse values for {key}: {value}")
    return crop_prop

def get_imgsize(paths:list, img_infos:dict):
    for img in paths:
        im = Image.open(img)
        filename = os.path.basename(img)
        key = filename[:-4]  

        if filename not in img_infos.keys():
            img_infos[key] =  {'crop_raw' : None, 'img_size' : None, 'crop_norm' : list()}

        img_infos[key]['img_size'] = list(im.size)
        img_size = list(im.size)
        img_infos[key]['img_size'] = img_size
            
        if img_infos[key]['crop_raw'] is None:
            img_infos[key]['crop_raw'] = [0, 0, img_size[0], img_size[1]]
        
        raw_crop = img_infos[key]['crop_raw']
        width, height = img_size
        x_center = (raw_crop[0] + raw_crop[2]) / 2 / width
        y_center = (raw_crop[1] + raw_crop[3]) / 2 / height
        crop_width = (raw_crop[2] - raw_crop[0]) / width
        crop_height = (raw_crop[3] - raw_crop[1]) / height
        
        img_infos[key]['crop_norm'] = [x_center, y_center, crop_width, crop_height]
    return

def main():
    path = '../convnext/food_image/kfood/food'
    dirs = os.listdir(path)
    img_infos = dict()
    for dir in dirs:
        dir_path = os.path.join(path, dir)
        print(dir_path)
        for d in os.listdir(dir_path):
            dir_subdir = os.path.join(dir_path, d)
            img_infos.update(prop_open(dir_subdir))
        #imgs_path = [os.path.join(dir_path, img) for img in os.listdir(dir_path) if img.endswith('jpg')]
        #get_imgsize(imgs_path, img_infos)
    with open("./properties.json", mode = 'w') as f:
        json.dump(img_infos, f)

if __name__ == '__main__':
    main()