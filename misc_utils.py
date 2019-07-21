
#import piexif
#import sys
#from PIL import Image
#from PIL.ExifTags import TAGS
#import pyexiv2
#import exiftool

#import subprocess
from subprocess import Popen, PIPE
#import exiftoolsub
#import sys






	#exif_dict = piexif.load("/home/chase/repos/INF-img-mgmt/images/" + file_name)
	#print(exif_dict)


	#print(get_exif("/home/chase/repos/INF-img-mgmt/images/exif.jpg"))


	#data = pyexiv2.Image.read_all("/home/chase/repos/INF-img-mgmt/images/exif.jpg")

	#data.read()
	#for key in data.exif_keys:
	#	tag = data[key]
	#	print(' %-40s%s' %(key, tag.value))

#sys.stdout.write("Hello")

#files = "/home/chase/repos/INF-img-mgmt/images/tag.jpg"


#os.system("exiftool " + files);
#print("a")
#subprocess.run('foo=bar; echo "$foo"', shell=True)




# Run "cat", which is a simple Linux program that prints it's input.
process = Popen(['exiftool', '-keywords=new_test_tag', '/home/chase/repos/INF-img-mgmt/images/exif.jpg'], stdin=PIPE, stdout=PIPE)
#process.stdin.write(b'Hello\n')
#process.stdin.flush()
 
result = repr(process.stdout.readline())

process.stdin.write(b'exiftool')
process.stdin.flush()
print(repr(process.stdout.readline()))


#exiftool -keywords=EXIF -keywords=editor dst.jpg
#Replace existing keyword list with two new keywords (EXIF and editor).

#exiftool -Keywords+=word -o newfile.jpg src.jpg
#Copy a source image to a new file, and add a keyword (word) to the current list of keywords.




#process.stdin.write(b'World\n')
#process.stdin.flush()  
#print(repr(process.stdout.readline())) # Should print 'World\n'

# "cat" will exit when you close stdin.  (Not all programs do this!)
process.stdin.close()
print('Waiting for exiftool to exit')
process.wait()
print('exiftool finished with return code %d' % process.returncode)

