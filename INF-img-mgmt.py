#!/usr/bin/env python3

#Copyright - Chase Kidder 2019
#INF-img-mgmt - INF-img-mgmt.py
#Main program file

#Project Imports
import config as cfg
import exif as exif

#Regular Imports
from PIL import Image, ImageOps
import os

def Tag_Untagged_Photos():

	file_found = False

	#Get a list of untagged files
	exif.check_tags(cfg.img_dir)


	#Open matches file and run the conversion on each match
	with open('untagged_files.txt','r') as tag_file:
		for file in tag_file:
			file = file.rstrip()
			if not file: continue

			file_found = True
			print("Processing File: " + file)

			#Add the "Not Uploaded" tags to file
			exif.add_tag(cfg.img_dir + os.sep + file, "NotUploadedToFlickr")
			exif.add_tag(cfg.img_dir + os.sep + file, "NotUploadedToPhotonWall")
			exif.add_tag(cfg.img_dir + os.sep + file, "NotUploadedToFieldDisplay")


	if file_found == True:
		return 0

	else:
		print("No New Files to Tag")
		return 0


def AV_Field_Display():

	#Find files to work with
	exif.find_tag(cfg.img_dir, "NotUploadedToFieldDisplay")

	#Open matches file and run the conversion on each match
	with open('match_tag.txt','r') as tag_file:
		for line in tag_file:
			line = line.rstrip()
			if not line: continue

			print("Processing File: " + line)
			
			#Config
			img_name = line
			img_path = cfg.img_dir + os.sep + img_name
			new_img_path = cfg.field_display_dir + os.sep + cfg.fd_pre_txt + img_name

			print(img_path)

			#Open Image for Editing
			img = Image.open(img_path)

			#Resize and Crop Image to Config Dimensions
			resized_img = exif.resize_image(img, cfg.AV_scale_dims)
			cropped_img = exif.crop_image(resized_img, cfg.AV_scale_dims)

			#Save the Cropped and Scaled Image To Disk
			exif.save_image(cropped_img, new_img_path)

			#Add "ReadyToBeUploaded" Tag
			exif.add_tag(img_path, "FieldDisplay_UploadedTo")

			#Remove "NotUploaded" Tag
			exif.remove_tag(img_path, "NotUploadedToFieldDisplay")


	return 0

def Photon_Wall():

	#Find files to work with
	exif.find_tag(cfg.img_dir, "NotUploadedToPhotonWall")

	#Open matches file and run the conversion on each match
	with open('match_tag.txt','r') as tag_file:
		for line in tag_file:
			line = line.rstrip()
			if not line: continue

			print("Processing File: " + line)
			
			#Config
			img_name = line
			img_path = cfg.img_dir + os.sep + img_name
			new_img_path = cfg.photon_wall_dir + os.sep + cfg.pw_pre_txt + img_name

			print(img_path)

			#Open Image for Editing
			img = Image.open(img_path)

			#Resize and Crop Image to Config Dimensions
			resized_img = exif.resize_image(img, cfg.PW_scale_dims)
			cropped_img = exif.crop_image(resized_img, cfg.PW_scale_dims)

			#Save the Cropped and Scaled Image To Disk
			exif.save_image(cropped_img, new_img_path)

			#Add "ReadyToUpload" Tag
			exif.add_tag(img_path, "PhotonWall_ReadyToUpload")

			#Remove "NotUploaded" Tag
			exif.remove_tag(img_path, "NotUploadedToPhotonWall")



			#TODO: Automatically upload the pictures to the Photon Wall then update the tag
			print("UPLOADING TO PHOTON WALL...")



			#Add "UploadedTo" Tag
			exif.add_tag(img_path, "PhotonWall_UploadedTo")

			#Remove "ReadyToUpload" Tag
			exif.remove_tag(img_path, "PhotonWall_ReadyToUpload")


	return 0

def Main(): 
	
	#Check for any untagged photos that have a rating
	Tag_Untagged_Photos()

	#Resize, Crop, and Save to Field Display
	AV_Field_Display()

	#Resize, Crop, and Save to Temp Folder for Photon Wall
	Photon_Wall()

	#Upload to Flickr
	#Upload_To_Flickr()
  

if __name__=="__main__": 
	Main() 