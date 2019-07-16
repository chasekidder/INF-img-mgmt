#!/usr/bin/env python3
#import piexif
#import sys
#from PIL import Image
#from PIL.ExifTags import TAGS
#import pyexiv2
#import exiftool

import subprocess
#import exiftoolsub
import sys


def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	info = i._getexif()
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value
	return ret


def main(file_name):
	#exif_dict = piexif.load("/home/chase/repos/INF-img-mgmt/images/" + file_name)
	#print(exif_dict)


	#print(get_exif("/home/chase/repos/INF-img-mgmt/images/exif.jpg"))


	#data = pyexiv2.Image.read_all("/home/chase/repos/INF-img-mgmt/images/exif.jpg")

	#data.read()
	#for key in data.exif_keys:
	#	tag = data[key]
	#	print(' %-40s%s' %(key, tag.value))

	sys.stdout.write("Hello")

	files = "/home/chase/repos/INF-img-mgmt/images/tag.jpg"

	asdf
	#os.system("exiftool " + files);
	print("a")
	subprocess.run('foo=bar; echo "$foo"', shell=True)
	


	if __name__=="__main__": 
		main(sys.argv[1]) 
