#!/usr/bin/env python3

# Chase Kidder 2019
#inf_img_mgmt - inf_img_mgmt.py
# Main program file

import crypt
import logging
import logging.config
import os
import sys

import flickrapi
from Crypto.Cipher import AES
from PIL import Image, ImageOps

import config as cfg
import exif
import funclib as func


def Main():
    try:
        logging.config.fileConfig(fname = cfg.LOGGER_CONFIG_FILE)
        logger = logging.getLogger(__name__)
    except KeyError:
        print("CRITICAL ERROR: could not initialize logger")
        sys.exit()

    #logging.basicConfig(filename='output.log', level=logging.DEBUG,
                       # format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


    setup_complete = os.path.isfile(os.getcwd() + os.sep + "api.key")

    if (setup_complete == False):
        logger.warning("Running Setup...")
        func.init_setup()

    # Check for any untagged photos that have a rating
    func.Tag_Untagged_Photos()

    # Resize, Crop, and Save to Field Display
    func.AV_Field_Display()

    # Resize, Crop, and Save to Temp Folder for Photon Wall
    func.Photon_Wall()

    # Upload to Flickr
    func.Upload_To_Flickr()

    logger.warning("SCRIPT END")


if __name__ == "__main__":
    Main()
