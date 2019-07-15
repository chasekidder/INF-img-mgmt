from PIL import Image
import os

#Config
img_path = os.getcwd()
AV_dimensions = (1920, 1080)

#open the image
img = Image.open(img_path)


#img_width = img.width
#img_height = img.height




#copy to a thumbnail image
thumb_img = img.copy()

#resize image to new dimensions



thumb_img.thumbnail(AV_dimensions)
#new_img = img.resize(AV_dimensions)



#create new file name
img_path = img_path + 3

newimg.save(img_path)