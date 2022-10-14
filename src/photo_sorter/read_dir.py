import os
import re


def set_regexp(suffix_list):
	
	regexp = ""
	for suf in suffix_list:
		if regexp == "":
			regexp += f"({suf}"
		else:
			regexp += f"|{suf}"
	#finalize the string if not empty
	if regexp != "":
		regexp += f")"
		return re.compile(regexp)
	else:
		return None


def scan_folder(wd, regexp):
	
	files_list = []	
	
	# Scanning folder
	
	print(f"Scanning folder : {wd}")
	
	
	# scanning all the files
	for entry in os.scandir(wd):
		if entry.is_file():
			
			# recognize if videos
			if regexp.search(entry.name):
				#print(entry.name)
				files_list.append(entry)
		elif entry.is_dir():
			files_list += scan_folder(entry.path, regexp)
		else:
			#need to work on recursive folders structure
			pass
		
	
	
	return files_list
	