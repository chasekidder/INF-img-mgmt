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
        file_found = False

        # Get a list of untagged files
        self.tagger.check_tags(self.image_dir)

        # Open matches file and run the conversion on each match
        with open('untagged_files.txt', 'r') as tag_file:
            for file in tag_file:
                file = file.rstrip()
                if not file:
                    continue

                # Verify that the file was last modified > 15 mins ago eg. 900 secs
                if time.time() - os.path.getmtime(self.image_dir + os.sep + file) > 900:
                    file_found = True
                    #logger.info("Processing File: " + file)

                    # Add the "Not Uploaded" tags to file
                    self.tagger.add_tag(self.image_dir + os.sep + file, "NotUploadedToFlickr")

                    self.tagger.add_tag(self.image_dir + os.sep + file, "NotUploadedToPhotonWall")

                    self.tagger.add_tag(self.image_dir + os.sep + file, "NotUploadedToFieldDisplay")

        if not file_found:
            #logger.warning("No New Files to Tag")
            pass
            

    def av_field_display(self):
        # Find files to work with
        self.tagger.find_tag("NotUploadedToFieldDisplay")

        # Open matches file and run the conversion on each match
        with open('match_tag.txt', 'r') as tag_file:
            for img in tag_file:
                img = img.rstrip()
                if not img:
                    continue

                #logger.info("Processing File: " + line)

                # Config
                img_path = self.image_dir + os.sep + img
                new_img_path = self.av_dir + os.sep + self.fd_prefix + img

                #logger.debug(img_path)

                # Open Image for Editing
                img = Image.open(img_path)

                # Resize and Crop Image to Config Dimensions
                resized_img = self.editor.resize_image(img, self.av_dimensions)
                cropped_img = self.editor.crop_image(resized_img, self.av_dimensions)

                # Save the Cropped and Scaled Image To Disk
                self.editor.save_image(cropped_img, new_img_path)

                # Add "UploadedTo" Tag
                self.tagger.add_tag(img, "FieldDisplay_UploadedTo")

                # Remove "NotUploaded" Tag
                self.tagger.remove_tag(img, "NotUploadedToFieldDisplay")


    def photon_wall(self):
        #logger = logging.getLogger(__name__)

        # Find files to work with
        self.tagger.find_tag(self.image_dir, "NotUploadedToPhotonWall")

        # Open matches file and run the conversion on each match
        with open('match_tag.txt', 'r') as tag_file:
            for img in tag_file:
                img = img.rstrip()
                if not img:
                    continue

                #logger.info("Processing File: " + line)

                img_path = self.image_dir + os.sep + img
                new_img_path = self.photon_temp_dir + os.sep \
                    + self.pw_prefix + img

                #logger.debug(img_path)

                # Open Image for Editing
                img = Image.open(img_path)

                # Resize and Crop Image to Config Dimensions
                resized_img = self.tagger.resize_image(img, self.pw_dimensions)
                cropped_img = self.editor.crop_image(resized_img, self.pw_dimensions)

                # Save the Cropped and Scaled Image To Disk
                self.editor.save_image(cropped_img, new_img_path)

                # Add "ReadyToUpload" Tag
                self.tagger.add_tag(img_path, "PhotonWall_ReadyToUpload")

                # Remove "NotUploaded" Tag
                self.tagger.remove_tag(img_path, "NotUploadedToPhotonWall")

                # TODO: Automatically upload the pictures to the Photon Wall
                # then update the tag
                #logger.info("UPLOADING TO PHOTON WALL...")

                # Add "UploadedTo" Tag
                self.tagger.add_tag(img_path, "PhotonWall_UploadedTo")

                # Remove "ReadyToUpload" Tag
                self.tagger.remove_tag(img_path, "PhotonWall_ReadyToUpload")

    def flickr(self):
        try:
            flickr = flickrapi.FlickrAPI(self.flickr_api_key, crypt.get_api_secret(), cache=True)
            flickr.authenticate_console(perms='write')

        except flickrapi.exceptions.FlickrError as err:
            #logger.exception("There was a Flickr authentication error: ", err)
            pass

        # Find files to work with
        self.tagger.find_tag("NotUploadedToFlickr")

        # Open matches file and run the conversion on each match
        with open('match_tag.txt', 'r') as tag_file:
            for line in tag_file:
                line = line.rstrip()
                if not line:
                    continue

                #logger.info("Processing File: " + line)

                # Config
                img_name = line
                img_path = self.image_dir + os.sep + img_name

                #logger.debug(img_path)

                # Add "ReadyToUpload" Tag
                self.tagger.add_tag(img_path, "Flickr_ReadyToUpload")

                # Remove "NotUploaded" Tag
                self.tagger.remove_tag(img_path, "NotUploadedToFlickr")

                #logger.info("UPLOADING TO FLICKR...")

                # Might want to remove tags prior to upload

                try:
                    flickr.upload(img_path)

                except flickrapi.exceptions.FlickrError as err:
                    #logger.exception("There was a Flickr upload error: ", err)
                    #logger.error("FILE_NOT_UPLOADED: " + img_path)
                    pass

                # Add "UploadedTo" Tag
                self.tagger.add_tag(img_path, "Flickr_UploadedTo")

                # Remove "ReadyToUpload" Tag
                self.tagger.remove_tag(img_path, "Flickr_ReadyToUpload")

        return 0


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
