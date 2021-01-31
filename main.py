# -*- coding: utf-8 -*-
# ###################################################################################
#
# 			Your text
#
#	License:
#	Author: 
#
#	                __   .__                              
#	  _____ _____  |  | _|__|_  _  _______ ____________   
#	 /     \\__  \ |  |/ /  \ \/ \/ /\__  \\_  __ \__  \  
#	|  Y Y  \/ __ \|    <|  |\     /  / __ \|  | \// __ \_
#	|__|_|  (____  /__|_ \__| \/\_/  (____  /__|  (____  /
#	      \/     \/     \/                \/           \/ 
#
#	Program walks through a directory (and subs), watch for photos and then put them 
#	into a directory based on the month of creation (e.g ./2020-07)
# ###################################################################################


import sys
import getopt
import os
import re
import json

import read_dir
import copy_file



def usage():
	pass
	

def read_parameters():
	try:
		with open('settings.json') as json_file:
		    return json.load(json_file)
			
	except json.JSONDecodeError as j_error:
		print(f"{j_error.msg}, {j_error.pos} line: {j_error.lineno}, column : {j_error.colno}")
	except Exception as e:
		print(f"Unkownn error {e}. Can't continue")
		return None
		
		
def get_app_args(arg_list):
	""" get the arguments from the command line """
	try:
		opts, args = getopt.getopt(arg_list, "hi:o:", ["help","input=","output="])
	except getopt.GetoptError as err:
		print("Error in the arguments")
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()

		elif opt in ("-o, --output"):
			export_dir = arg

		elif opt in ("-i", "--input"):
			input_dir = arg
		

	try:
		if input_dir != None and export_dir != None:
			return input_dir, export_dir
	except:
		usage()
		print("Please provide input and output directories")
		sys.exit(2)


		
def main(arg_list):
	# Welcome messages
	print("")
	print("")
	print("")
	print("".join((
	"                 __   .__                              \n",
	"   _____ _____  |  | _|__|_  _  _______ ____________   \n",
	"  /     \\\\__  \ |  |/ /  \ \/ \/ /\__  \\\\_  __ \\__  \\  \n",
	" |  Y Y  \/ __ \|    <|  |\     /  / __ \|  | \// __ \_\n",
	" |__|_|  (____  /__|_ \__| \/\_/  (____  /__|  (____  /\n",
	"      \/     \/     \/                \/           \/ \n")))
	print("")
	print("")
	print("")
	print("-------------")
	print("Photos sorter")
	print("-------------")
	
	# reading arguments from command line
	input_dir, export_dir = get_app_args(arg_list)
	
	# reading parameters
	params = read_parameters()
	
	if params == None:
		print("No parameters. Exiting")
		sys.exit(1)
	
	# debug info
	else:
		if params["DEBUG"] == "Y":
			print("Parameters are : ")
			print("-----------------")
			for k,v in params.items():
				print(f"{k} : {v}")
				pass
	
	# clear a line
	print("")			
				
	# Reading directory to be sorted
	# ==============================
	
	
	# scanning for photos
	#photos = scanning(params["PHOTOS_EXTENSIONS"], "photo", input_dir )
	
	#scanning for videos
	videos = scanning(params["VIDEOS_EXTENSIONS"], "video", input_dir )
	
	# Copying files needed to be saved
	# ================================
	#if len(photos)>0 :
	#	copy_file.copy_photos(photos, export_dir)
	if len(videos)>0:
		copy_file.copy_videos(videos, export_dir)
		#pass

	sys.exit(0)


def scanning(params, text, input_dir):
	# regexp to find all items
	regexp = read_dir.set_regexp(params)
	
	# Look for items
	print("-------------------------")
	items = read_dir.scan_folder(input_dir, regexp)
	
	if len(items) == 0:
		print(f"No {text} found.")
	else:
		print(f"{len(items)} {text}s found")
	print("-------------------------")
	print("")

	return items


if __name__ == "__main__":
	main(sys.argv[1:])