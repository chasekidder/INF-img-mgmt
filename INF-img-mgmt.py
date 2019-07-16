#!/usr/bin/env python3
from PIL import Image, ImageOps
import os
import config as cfg
from PIL.ExifTags import TAGS
import piexif

def find_image_files():

    return 1

def resize_image(thumb_img, new_dimensions): 
    thumb_img.thumbnail(new_dimensions)
    #new_img = img.resize(AV_dimensions)

    #print("resized")
    return thumb_img


def crop_image(img_toBeCropped, new_dimensions):
    #crop image

    #centering is percentage taken from each side that is being cropped ie. 50% from top and bottom
    #if the height is being cropped
    img_toBeCropped = ImageOps.fit(img_toBeCropped, new_dimensions, centering=(0.5, 0.5))

    #print("cropped")
    return img_toBeCropped


def save_image(img_toBeSaved, new_path):
    #save under new file name
    img_toBeSaved.save(new_path)

    #print("img saved: " + new_path)
    return 1



def test_change_exif(exif_data):

    print(exif_data)
    add_data = {40094: (116, 0, 101, 0, 115, 0, 116, 0, 95, 0, 116, 0, 97, 0, 103, 0, 0, 0)}
    #, 40094: (116, 0, 101, 0, 115, 0, 116, 0, 95, 0, 116, 0, 97, 0, 103, 0, 0, 0)

    #exif_data['GPS'][piexif.GPSIFD.GPSAltitude] = (140, 1)
    exif_data['0th'] = add_data

    print(exif_data)

    return exif_data



def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret














def Main(): 
    #print("Started")



    #Config
    #img_dir = os.getcwd()
    img_name = "test.jpg"
    img_path = cfg.img_dir + os.sep + img_name
    new_img_path = cfg.temp_img_dir + os.sep + "new_" + img_name

    AV_dimensions = (1920, 1080)


    #for loop here


    #open the image
    img = Image.open(img_path)

    #print(img_path)


    



    #exif_data = img._getexif()
    #print(TAGS[256])

    #exif_dict = piexif.load(img.info['exif'])
    #altitude = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude]
    #print(altitude)

    exif_dict = piexif.load(img_path)
    new_exif = test_change_exif(exif_dict)
    exif_bytes = piexif.dump(new_exif)
    piexif.insert(exif_bytes, cfg.img_dir + "/exif.jpg")

    print(get_exif(cfg.img_dir + "/exif.jpg"))



    resized_img = resize_image(img, AV_dimensions)
    cropped_img = crop_image(resized_img, AV_dimensions)

    save_image(cropped_img, new_img_path)

  

if __name__=="__main__": 
    Main() 