#!/usr/bin/env python3
from PIL import Image, ImageOps
import config as cfg
from subprocess import Popen, PIPE
import os

def find_image_files():

	return 0


def resize_image(thumb_img, new_dimensions): 

	thumb_img.thumbnail(new_dimensions)
	
	return thumb_img


def crop_image(img_toBeCropped, new_dimensions):

	#centering is percentage taken from each side that is being cropped ie. 50% from top and bottom
	#if the height is being cropped
	img_toBeCropped = ImageOps.fit(img_toBeCropped, new_dimensions, centering=(0.5, 0.5))

	return img_toBeCropped


def save_image(img_toBeSaved, new_path):

	#save under new file name
	img_toBeSaved.save(new_path)

	return 0



def add_tag(file_path, tag):

	#Add keyword to file using exiftool
	process = Popen(['exiftool', '-keywords+=' + tag, file_path, "-overwrite_original"], stdin=PIPE, stdout=PIPE)
	
	#Read exiftool output
	print(repr(process.stdout.readline()))

	#close exiftool
	process.stdin.close()
	process.wait()
	print('exiftool finished with return code %d' % process.returncode)	

	return 0



def Main(): 

	#Config
	img_name = "test.jpg"
	img_path = cfg.img_dir + os.sep + img_name
	new_img_path = cfg.temp_img_dir + os.sep + cfg.pre_txt + img_name

	
	#Open Image for Editing
	img = Image.open(img_path)


	#process = Popen(['exiftool', '-stay_open=1', "-@=exiftoolargs.args"], stdin=PIPE, stdout=PIPE)
	#exiftool -make -model -csv -@ file_list.args > out.csv
	#exiftool -stay_open True -@ ARGFILE


	#Resize and Crop Image to Config Dimensions
	resized_img = resize_image(img, cfg.scale_dims)
	cropped_img = crop_image(resized_img, cfg.scale_dims)

	#Save the Cropped and Scaled Image To Disk
	save_image(cropped_img, new_img_path)

	#Add Metadata to New File
	add_tag(new_img_path, "auto_test_tag")
	add_tag(new_img_path, "2nd_test_tag")

	

  

if __name__=="__main__": 
	Main() 