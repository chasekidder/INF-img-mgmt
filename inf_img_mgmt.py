#!/usr/bin/env python3

# Chase Kidder 2019
#inf_img_mgmt - inf_img_mgmt.py
#Main program file

#Project Imports
import config as cfg
import exif
import crypt
import funclib as func

#Regular Imports
from PIL import Image, ImageOps
from Crypto.Cipher import AES
import os
import flickrapi


def Main(): 
     
    setup_complete = os.path.isfile(os.getcwd() + os.sep + "api.key")

    if (setup_complete == False):
        print("Running Flickr API Setup...")
        func.init_setup()



    #Check for any untagged photos that have a rating
    func.Tag_Untagged_Photos()

    #Resize, Crop, and Save to Field Display
    func.AV_Field_Display()

    #Resize, Crop, and Save to Temp Folder for Photon Wall
    func.Photon_Wall()

    #Upload to Flickr
    func.Upload_To_Flickr()


    #Process
    #encrypt secret


    print("SCRIPT END")

if __name__=="__main__": 
    Main() 