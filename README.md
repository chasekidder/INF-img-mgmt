## INF-img-mgmt
This is a little Python script that was put together to automate the tagging and upload of pictures to the IndianaFIRST Flickr,
Photon Wall, and Field Display. It is designed to be run on a Linux system with Python 3.

## Motivation
With hundreds of photos coming in per event, it became troublesome to continue to manually tag and upload batches of 100+ pictures for each event. The process was rife with opportunity for human error and the idea of a regularly run script to 
upload automatically was developed.

## Code style
This project adheres to the Python PEP-8 standard. Mostly.

[![Python-PEP8](https://img.shields.io/badge/code%20style-standard-brightgreen.svg?style=flat)](https://www.python.org/dev/peps/pep-0008/)

## Tech/framework used
- [Pillow](https://github.com/python-pillow/Pillow)
- [flickrapi](https://github.com/sybrenstuvel/flickrapi)
- [pycrypto](https://github.com/dlitz/pycrypto)
- [exiftool](https://github.com/exiftool/exiftool)

## Features
- Automatic tagging of photos with rating of 3 stars
- Automatic retagging of photos after completed operations
- Automatic resizing and cropping to desired photo size
- Automatic Upload to Flickr
- Easily editable configuration file
- Fully configurable search and output directories
- AES Encrypted API secret storage
- OAuth 1.0a Compatible
- All processes independently configurable

## Configuration
config.py

```#Photo Input Search Directory
img_dir = "[SEARCH DIRECTORY HERE]"

#Flickr API Key
flickr_api_key = ""

#Field Display Output Directory
field_display_dir = "/.../field_display"

#Photon Wall Output Directory
photon_wall_dir = "/.../photon_wall"

#Text to Prepend to Field Display Images
fd_pre_txt = "fd_"

#Text to Prepend to Photon Wall Images
pw_pre_txt = "pw_"

#AV Goal Dimensions
AV_scale_dims = (1920, 1080)

#Photon Wall Goal Dimensions
PW_scale_dims = (1360, 786)
```


## How to use?

Download .zip that includes the following files:
- inf_img_mgmt.py
- exif.py
- crypt.py
- funclib.py
- config.py

Edit the config.py file to adjust to your file paths and scaling preferences.

```gedit config.py```

Run the main Python file to start initial API setup.

```python3 INF-img-mgmt.py```

Directory scan and auto-tagging will begin.


## Credits
IndianaFIRST


Hugh Meyer

Chase Kidder - Author


##License

GPL-3.0