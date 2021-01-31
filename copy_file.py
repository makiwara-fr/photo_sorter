import os
import re
from datetime import datetime
from PIL import Image
import shutil
import hachoir
import sys


from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core.tools import makeUnicode

# Get metadata for video file
def metadata_videos(filename):

	try:
		parser = createParser(filename)
		with parser:
			try:
			
				metadata = extractMetadata(parser)
		
				date_exif = datetime.fromisoformat(makeUnicode(metadata.getItems("creation_date").values[0].value))
				#print(date_exif)
				return date_exif
			# "date_time_original"
			except Exception as err:
				print("Metadata extraction error: ")
				print(err)
			
			
	except Exception as e:
		print("Unable to parse file " + str(filename))
		print(e)
		
	
	
			

	

split_date = re.compile(":")

def get_month_taken_photos(path):
	""" return date of creation base on exif """
	try :
		date_exif = Image.open(path)._getexif()[36867]
		split = split_date.split(date_exif)
		return split[0]+ "-"+ split[1]
	except Exception as e:
		print(f"Problem with photo's EXIF : {path.path} - Defaulting date")
		return "1970-01"
		
def get_month_taken_videos(path):
	""" return date of creation base on exif for videos """
	try :
		date_exif = metadata_videos(path.path)
		if date_exif.month < 10:
			return str(date_exif.year)+"-0"+str(date_exif.month)
		else:
			return str(date_exif.year)+"-"+str(date_exif.month)
		
	except Exception as e:
		print(f"Problem with video's EXIF : {path.path} - Defaulting date")
		print(e)
		return "1970-01"


	
def copy(items, dir, text, get_date_taken):
	
	print("--------------")
	print("Copying " + text)
	print("--------------")
	
	copied = 0
	skipped = 0
	
	for p in items:
		# find when picture has been taken
		#print(p.name)
		# get year and month from item
		year_month = get_date_taken(p)
		#print(year_month)
		
		# Check if photo already exists
		target = os.path.join(dir,year_month, p.name)
		if os.path.exists(target):
			print(f"File {p.name} already exists. Skipping")
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
		
		
		
	print(f"{len(items)} {text}s provided : {copied} have been copied, {skipped} were skipped")
	
	
def copy_videos(videos, dir):
	copy(videos, dir, "video", get_month_taken_videos)
	
def copy_photos(photos, dir):
	copy(videos, dir, "photo", get_month_taken_photos)