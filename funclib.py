# Chase Kidder 2019
# inf_img_mgmt - funclib.py
# Main Functions File

import crypt
import logging
import os
import time

import flickrapi
from PIL import Image, ImageOps

import config as cfg
import exif


def init_setup():

    logger = logging.getLogger(__name__)

    while True:
        try:

            # Check to see if the secret is a valid format
            crypt.encrypt(input("Please enter Flickr API secret: "))

            logger.warning("Running OAuth Authentication...")

            # Use OAuth to get a token from Flickr
            flickr = flickrapi.FlickrAPI(
                cfg.flickr_api_key, crypt.get_api_secret(), cache=True)

            flickr.authenticate_console(perms='write')

            break

        except ValueError:
            logger.exception(
                "That is an invalid API Secret format. Secrets are 16 characters.")

        except flickrapi.exceptions.FlickrError as err:
            logger.exception("You have not entered a valid API secret or have \
                            not provided a valid API Key in the config file.")
            os.remove("api.key")

    logger.info("Script Setup is Complete.")

    return 0


def Tag_Untagged_Photos():

    logger = logging.getLogger(__name__)

    file_found = False

    # Get a list of untagged files
    exif.check_tags(cfg.img_dir)

    # Open matches file and run the conversion on each match
    with open('untagged_files.txt', 'r') as tag_file:
        for file in tag_file:
            file = file.rstrip()
            if not file:
                continue

            logger.debug(time.time() - os.path.getmtime(cfg.img_dir + os.sep + file))
            # Verify that the file was last modified > 15 mins ago eg. 900 secs
            if time.time() - os.path.getmtime(cfg.img_dir + os.sep + file) > 900:
                file_found = True
                logger.info("Processing File: " + file)

                # Add the "Not Uploaded" tags to file
                exif.add_tag(cfg.img_dir + os.sep + file,
                             "NotUploadedToFlickr")

                exif.add_tag(cfg.img_dir + os.sep + file,
                             "NotUploadedToPhotonWall")

                exif.add_tag(cfg.img_dir + os.sep + file,
                             "NotUploadedToFieldDisplay")

    if file_found == True:
        return 0

    else:
        logger.warning("No New Files to Tag")
        return 0


def AV_Field_Display():

    logger = logging.getLogger(__name__)

    # Find files to work with
    exif.find_tag(cfg.img_dir, "NotUploadedToFieldDisplay")

    # Open matches file and run the conversion on each match
    with open('match_tag.txt', 'r') as tag_file:
        for line in tag_file:
            line = line.rstrip()
            if not line:
                continue

            logger.info("Processing File: " + line)

            # Config
            img_name = line
            img_path = cfg.img_dir + os.sep + img_name
            new_img_path = cfg.field_display_dir + os.sep \
                + cfg.fd_pre_txt + img_name

            logger.debug(img_path)

            # Open Image for Editing
            img = Image.open(img_path)

            # Resize and Crop Image to Config Dimensions
            resized_img = exif.resize_image(img, cfg.AV_scale_dims)
            cropped_img = exif.crop_image(resized_img, cfg.AV_scale_dims)

            # Save the Cropped and Scaled Image To Disk
            exif.save_image(cropped_img, new_img_path)

            # Add "ReadyToBeUploaded" Tag
            exif.add_tag(img_path, "FieldDisplay_UploadedTo")

            # Remove "NotUploaded" Tag
            exif.remove_tag(img_path, "NotUploadedToFieldDisplay")

    return 0


def Photon_Wall():

    logger = logging.getLogger(__name__)

    # Find files to work with
    exif.find_tag(cfg.img_dir, "NotUploadedToPhotonWall")

    # Open matches file and run the conversion on each match
    with open('match_tag.txt', 'r') as tag_file:
        for line in tag_file:
            line = line.rstrip()
            if not line:
                continue

            logger.info("Processing File: " + line)

            # Config
            img_name = line
            img_path = cfg.img_dir + os.sep + img_name
            new_img_path = cfg.photon_wall_dir + os.sep \
                + cfg.pw_pre_txt + img_name

            logger.debug(img_path)

            # Open Image for Editing
            img = Image.open(img_path)

            # Resize and Crop Image to Config Dimensions
            resized_img = exif.resize_image(img, cfg.PW_scale_dims)
            cropped_img = exif.crop_image(resized_img, cfg.PW_scale_dims)

            # Save the Cropped and Scaled Image To Disk
            exif.save_image(cropped_img, new_img_path)

            # Add "ReadyToUpload" Tag
            exif.add_tag(img_path, "PhotonWall_ReadyToUpload")

            # Remove "NotUploaded" Tag
            exif.remove_tag(img_path, "NotUploadedToPhotonWall")

            # TODO: Automatically upload the pictures to the Photon Wall
            # then update the tag
            logger.info("UPLOADING TO PHOTON WALL...")

            # Add "UploadedTo" Tag
            exif.add_tag(img_path, "PhotonWall_UploadedTo")

            # Remove "ReadyToUpload" Tag
            exif.remove_tag(img_path, "PhotonWall_ReadyToUpload")

    return 0


def Upload_To_Flickr():

    logger = logging.getLogger(__name__)

    try:

        flickr = flickrapi.FlickrAPI(
            cfg.flickr_api_key, crypt.get_api_secret(), cache=True)
        flickr.authenticate_console(perms='write')

    except flickrapi.exceptions.FlickrError as err:
        logger.exception("There was a Flickr authentication error: ", err)

    # Find files to work with
    exif.find_tag(cfg.img_dir, "NotUploadedToFlickr")

    # Open matches file and run the conversion on each match
    with open('match_tag.txt', 'r') as tag_file:
        for line in tag_file:
            line = line.rstrip()
            if not line:
                continue

            logger.info("Processing File: " + line)

            # Config
            img_name = line
            img_path = cfg.img_dir + os.sep + img_name

            logger.debug(img_path)

            # Add "ReadyToUpload" Tag
            exif.add_tag(img_path, "Flickr_ReadyToUpload")

            # Remove "NotUploaded" Tag
            exif.remove_tag(img_path, "NotUploadedToFlickr")

            logger.info("UPLOADING TO FLICKR...")

            # Might want to remove tags prior to upload

            try:

                flickr.upload(img_path)

            except flickrapi.exceptions.FlickrError as err:
                logger.exception("There was a Flickr upload error: ", err)
                logger.error("FILE_NOT_UPLOADED: " + img_path)

            # Add "UploadedTo" Tag
            exif.add_tag(img_path, "Flickr_UploadedTo")

            # Remove "ReadyToUpload" Tag
            exif.remove_tag(img_path, "Flickr_ReadyToUpload")

    return 0
