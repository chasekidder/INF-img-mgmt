#!/usr/bin/env python3

# Chase Kidder 2019
# pynf_media_manager - config.py
# Configuration Parser File

import configparser
import os

class config():
    def __init__(self, config_path):
        self.config_file = configparser.RawConfigParser()
        self.path = config_path

        if not os.path.exists(self.path):
            self.generate_config()

        self.read_config()

    def generate_config(self):
        pass

    def read_config(self):
        self.config_file.read(self.path)

        self.image_dir = self.config_file['GLOBAL']['image_dir']

        self.av_dir = self.config_file['AV FIELD DISPLAY']['export_dir']
        self.fd_prefix = self.config_file['AV FIELD DISPLAY']['prefix']
        self.av_dimensions = self.config_file['AV FIELD DISPLAY']['dimensions']

        self.photon_temp_dir = self.config_file['PHOTON WALL']['export_dir']
        self.pw_prefix = self.config_file['PHOTON WALL']['prefix']
        self.pw_dimensions = self.config_file['PHOTON WALL']['dimensions']

        self.flickr_temp_dir = self.config_file['FLICKR API']['temp_dir']
        self.flickr_api_key = self.config_file['FLICKR API']['api_key']

        
