#Copyright - Chase Kidder 2019
#INF-img-mgmt - exif.py
#Function file to keep EXIF tag functionality separate of the rest of the program functions

import subprocess
from PIL import Image, ImageOps
from subprocess import Popen, PIPE

def find_tag(folder_path, tag):
	
	#Write all matching images to file
	#process = Popen(["exiftool", "−T", "-if","$keywords =~ test_tag", "-filename", folder_path], stdin=PIPE, stdout=PIPE)
	subprocess.call("exiftool -T -r -filename -if '$keywords eq \"" + tag + "\"' " + folder_path + " > match_tag.txt", shell=True)

	#exiftool -filename -if '$keywords eq "test_tag"' .

	return 0

def check_tags(folder_path):
	
	#Check for all files in the folder that have a rating of 3 stars and no tags
		#Command: exiftool -T -r -filename -if 'not $keywords' -if '$rating eq 3' [PATH GOES HERE]
	subprocess.call("exiftool -T -r -filename -if 'not $keywords' -if '$rating eq 3' " + folder_path + " > untagged_files.txt", shell=True)


	#TODO: See if I can change over to popen instead of subprocess.call
		#7.18.19 - Can't seem to get the conditional to work right with the seperate argument format

	#test_file = open('test_file.txt','w')
	#process = Popen(["exiftool","-v1", "-filename", "-if","\'not $keywords\' ", folder_path], stdin=PIPE, stdout=test_file)
		

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