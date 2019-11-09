#!/usr/bin/env python3

# Chase Kidder 2019
# pynf_media_manager - image.py
# Image Class File

import subprocess as sp
from PIL import Image, ImageOps
import flickrapi
import time
import os

import crypt

class images():
    def __init__(self, config):
        self.image_dir = config.image_dir
        self.av_dir = config.av_dir
        self.photon_temp_dir = config.photon_temp_dir
        self.flickr_temp_dir = config.flickr_temp_dir

        self.tagger = img_tagger()
        self.editor = img_editor()

        self.fd_prefix = "FD_"
        self.pw_prefix = "PW_"

        self.av_dimensions = config.av_dimensions
        self.pw_dimensions = config.pw_dimensions

        self.flickr_api_key = config.flickr_api_key
        self.flickr_api_secret = crypt.get_api_secret()


    def tag_images(self):
        pass
            

    def av_field_display(self):
        pass

    def flickr(self):
        pass


class img_tagger():
    def __init__(self):
        pass

    def find_tag(self, tag, path):
        sp.call("exiftool -m -q -q -T -r -filename -if '$FileModifyDate ' -if '$keywords =~ /" +
            tag + "/' " + path + " > match_tag.txt", shell=True)

    def check_tags(self, path):
        sp.call("exiftool -m -q -q -T -r -filename -if 'not $keywords' -if '$rating eq 3' " +
            path + " > untagged_files.txt", shell=True)

    def add_tag(self, tag, file_path):
        process = sp.Popen(['exiftool', '-m', '-q', '-q', '-keywords+=' +
            tag, file_path, "-overwrite_original"], stdin=sp.PIPE, stdout=sp.PIPE)

    def remove_tag(self, tag, file_path):
        process = sp.Popen(['exiftool', '-m', '-q', '-q', '-keywords-=' +
                     tag, file_path, "-overwrite_original"], stdin=sp.PIPE, stdout=sp.PIPE)

    def copy_rating(self, src_file, dest_file):
        process = sp.Popen(['exiftool', '-m', '-q', '-q', "−tagsFromFile", src_file,
            '-rating>rating', "-overwrite_original", dest_file], stdin=sp.PIPE, stdout=sp.PIPE)



class img_editor():
    def __init__(self):
        pass

    def resize_image(self, img, new_dimensions):
        return img.thumbnail(new_dimensions)

    def crop_image(self, img, new_dimensions):
        img = ImageOps.fit(img, new_dimensions, centering=(0.5, 0.5))
        return img

    def save_image(self, img, path):
        img.save(path)
