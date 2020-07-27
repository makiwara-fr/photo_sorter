import os
import re
from datetime import datetime
from PIL import Image
import shutil

split_date = re.compile(":")

def get_date_taken(path):
	""" return date of creation base on exif """
	# need to find something else if exif is missing
	return Image.open(path)._getexif()[36867]

def copy_photos(photos, dir):
	
	print("--------------")
	print("Copying photos")
	print("--------------")
	
	copied = 0
	skipped = 0
	
	for p in photos:
		# find when picture has been taken
		#print(p.name)
		# split exif info to get dates
		split = split_date.split(get_date_taken(p.path))
		year_month = split[0]+ "-"+ split[1]
		
		
		
		# Check if photo already exists
		target = os.path.join(dir,year_month, p.name)
		if os.path.exists(target):
			#print(f"File {p.name} already exists. Skipping")
			skipped += 1
		else:
			# new photo so copy from source
			# check if target path exists
			target_dir = os.path.split(target)[0]
			if not os.path.exists(target_dir):
				os.mkdir(target_dir)
			# copy photo
			shutil.copyfile(p.path, target)
			copied += 1
		
		
		
	print(f"{len(photos)} photos provided : {copied} have been copied, {skipped} were skipped")