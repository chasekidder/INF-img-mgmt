#!/usr/bin/env python3
from PIL import Image, ImageOps
import config as cfg
import subprocess
from subprocess import Popen, PIPE
import os

def find_tag(folder_path, tag):
	
	#Write all matching images to file
	#process = Popen(["exiftool", "−T", "-if","$keywords =~ test_tag", "-filename", folder_path], stdin=PIPE, stdout=PIPE)
	subprocess.call("exiftool -T -r -filename -if '$keywords eq \"" + tag + "\"' " + folder_path + " > match_tag.txt", shell=True)

	#exiftool -filename -if '$keywords eq "test_tag"' .

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

def copy_rating(file_path, new_file_path):
	#exiftool [ OPTIONS ] −tagsFromFile SRCFILE [− SRCTAG [> DSTTAG ]...] FILE ...
	#exiftool -TagsFromFile file.jpg '-Keywords>Description' file.jpg

	#Add keyword to file using exiftool
	process = Popen(['exiftool', "−tagsFromFile", file_path,'-rating>rating',"-overwrite_original", new_file_path], stdin=PIPE, stdout=PIPE)
	
	#Read exiftool output
	print(repr(process.stdout.readline()))

	#close exiftool
	process.stdin.close()
	process.wait()
	print('exiftool finished with return code %d' % process.returncode)	

	return 0



def Main(): 
	
	#Find files to work with
	find_tag(cfg.img_dir, "test_tag")
	print("found tags")


	with open('match_tag.txt','r') as tag_file:
		for line in tag_file:
			line = line.rstrip()
			if not line: continue

			print(line)
			
			#Config
			img_name = line
			img_path = cfg.img_dir + os.sep + img_name
			new_img_path = cfg.temp_img_dir + os.sep + cfg.pre_txt + img_name

			#Open Image for Editing
			img = Image.open(img_path)

			#Resize and Crop Image to Config Dimensions
			resized_img = resize_image(img, cfg.scale_dims)
			cropped_img = crop_image(resized_img, cfg.scale_dims)

			#Save the Cropped and Scaled Image To Disk
			save_image(cropped_img, new_img_path)

			#Add Metadata to New File
			add_tag(new_img_path, "auto_test_tag")
			add_tag(new_img_path, "2nd_test_tag")

			#copy rating
			copy_rating(img_path, new_img_path)

	


	#process = Popen(['exiftool', '-stay_open=1', "-@=exiftoolargs.args"], stdin=PIPE, stdout=PIPE)
	#exiftool -make -model -csv -@ file_list.args > out.csv
	#exiftool -stay_open True -@ ARGFILE


	

	


  

if __name__=="__main__": 
	Main() 