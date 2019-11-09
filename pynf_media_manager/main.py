#!/usr/bin/env python3

# Chase Kidder 2019
# pynf_media_manager - main.py
# Main program file

import os

import image, config

class application():
    def __init__(self):
        self.cwd = os.getcwd() + os.sep 

        setup_complete = os.path.isfile(self.cwd + "api.key")

        if (setup_complete == False):
            #logger.warning("Running Setup...")
            self.setup()
        
        self.config = config.config(self.cwd + "config.conf")
        self.images = image.images(self.config)


    def setup(self):
        pass

    def run(self):
        keep_running = True

        while keep_running:
            self.images.tag_images()
            self.images.av_field_display()
            self.images.photon_wall()
            self.images.flickr()

    def close(self):
        pass



def main():
    main_app = application()

    main_app.run()

    main_app.close()



if __name__ == "__main__":
    main()
