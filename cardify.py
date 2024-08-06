#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 
# ******************************************************************************
#
# @file			cardify.py
#
# @brief        Code file for 3x5 card generation tool 
#
# @copyright    Copyright (C) 2024 Barrett Edwards. All rights reserved.
#
# @date         Aug 2024
# @author       Barrett Edwards <thequakemech@gmail.com>
# 
# ******************************************************************************

import os
import sys
import argparse
import yaml

import nitrile

from nitrile import Package, Command, Tag, Content

class Card:

	def __init__(self, yaml=None):
		self.src = yaml
		self.dst = None
		self.tex_str = None

	def __str__(self):
		return self.tex_str

	def tex(self, yaml_dct=None, options={}):

		# STEPS:
		# 1. Set default options 
		# 2. Use new dictionary if provided 
		# 3. Merge options dictionaries
		# 4. Create Nitrile document
		# 5. Add pacakges 
		# 6. Add commands 
		# 7. Add content
		# 8: Generate tex

		# STEP 1. Set default options 
		opt = {}
		opt['basefontsize'] = 10
		opt['paperwidth'] = 5
		opt['paperheight'] = 3
		opt['vertical'] = False
		opt['top'] = 0.2
		opt['left'] = 0.2
		opt['right'] = 0.2
		opt['bottom'] = 0.2
		opt['footskip'] = 0
		opt['fontsize'] = 'normalsize'
		opt['center'] = True
		opt['vcenter'] = True
		opt['noindent'] = False
		opt['convert'] = True

		# STEP 2: Use new dictionary if provided 
		if yaml_dct:
			self.src = yaml_dct 
		src = self.src 

		# STEP 3: Merge options dictionaries
		if 'options' in src:
			for x in src['options'].keys():
				opt[x] = src['options'][x]

		for x in options.keys():
			opt[x] = options[x]

		# STEP 4: Create Nitrile Document 
		doc = nitrile.Document(classname='extreport', options=[str(opt['basefontsize'])+"pt"])

		# STEP 5: Add packages

		# For formatting enumerations
		doc.add(Package('enumitem'))

		# For itemized checkbox formatting enumerations
		doc.add(Package('amssymb'))

		# The fancyhdr pacage allows us to set the formatting of the footer
		doc.add(Package('fancyhdr'))

		# Flip orientation 
		if opt['vertical']:
			tmp = opt['paperwidth']
			opt['paperwidth'] = opt['paperheight']
			opt['paperheight'] = tmp

		# Add space for author and date if present
		num = 0
		if 'author' in src and src['author'] is not None:
			num += 1
		if 'date' in src and src['date'] is not None:
			num += 1 
		opt['bottom'] = round(opt['bottom'] + (0.2 * num), 2)

		# Specify page dimensions using the geometry package 
		doc.add(Package('geometry', options=["paperwidth="+str(opt['paperwidth'])+"in","paperheight="+str(opt['paperheight'])+"in","top="+str(opt['top'])+"in","left="+str(opt['left'])+"in","right="+str(opt['right'])+"in","bottom="+str(opt['bottom'])+"in","footskip="+str(opt['footskip'])+"in"]))

		# STEP 6: Add commands 

		# Set page style to fancy so we can specify the footer 
		doc.add(Command('pagestyle', options=['fancy']))

		# Set the Left footer entry to the title
		if "title" in src and src['title'] is not None:
			s = "\small " + src["title"]
			doc.add(Command('fancyfoot', parameters=['L'], options=[s]))
		else:
			doc.add(Command('fancyfoot', parameters=['L'], options=[""]))

		# Set the center footer entry to empty 
		doc.add(Command('fancyfoot', parameters=['C'], options=[""]))

		# Set the right footer entry to the Author & Date 
		s = "" 
		rightfooter = False
		if "author" in src and src['author'] is not None:
			rightfooter = True
			s += src["author"]
			if 'date' in src:
				s += "\n\n"
		if "date" in src and src['date'] is not None:
			rightfooter = True
			s += src["date"].replace("#","\#")
		if rightfooter:
			doc.add(Command('fancyfoot', parameters=['R'], options=["\small " + s]))
		else:
			doc.add(Command('fancyfoot', parameters=['R'], options=[""]))

		# STEP 7: Add content 

		doc.add(Tag('topskip0pt', postnewlines=1))

		if opt['vcenter']:
			doc.add(Tag('vspace*', options=['\\fill'], postnewlines=1))

		indent = "\\indent "
		if opt['noindent']:
			indent = "\\noindent "

		if src['text'].startswith(" "):
			src['text'] = src['text'].replace(" ", "", 1)

		if opt['center']:
			doc.add(Tag('center', postnewlines=1))
			src['text'] = src['text'].replace("\n\n", "\a\a\\mbox{}\\newline ").replace("\n","\n\n").replace("\a","\n")
		else:
			src['text'] = indent + src['text'].replace("\n\n", "\a\\newline\\newline" + indent).replace("\n", "\n\\newline" + indent).replace("\a","\n" )

		s = "\\" + opt['fontsize'] + "\n" + src['text']
		doc.add(Content(s, convert=opt['convert'], postnewlines=1))

		doc.add(Tag('vspace*', options=['\\fill'], postnewlines=0))
		
		self.dst = doc 

		# STEP 8: Generate tex
		self.tex_str = doc.tex()

		return self.tex_str

	def pdf(self, filename, force=True):
		self.dst.pdf(filename=filename, force=force)

		return	

def load(filename):
	# STEPS 
	# 3. Open file
	# 4. Read in file
	# 5. Parse file to dictionary

	# STEP 3: Open file 
	fp = open(filename, "r")
		
	# STEP 4: Read in File 
	file = fp.read()

	# STEP 5: Parse File
	y = yaml.safe_load(file)

	return y

def save(s, filename):
	# STEP 3: Open file 
	fp = open(filename, "w")
	fp.write(s)

	return

def parse_arguments():

	# Parse arguments
	parser = argparse.ArgumentParser(description='Quote card creator')
	
	parser.add_argument('filename',             nargs='?',                              help='YMAL source filename', default='?')
	parser.add_argument('-o','--output',        required=False, action='store',         help='Output filename')
	
	#input formats
	#parser.add_argument('-i','--stdin',         required=False, action='store_true',    help='Use STDIN for input')
	
	#output formats
	parser.add_argument('-t','--tex',           required=False, action='store_true',    help='Build doc into Latex format')
	parser.add_argument('-p','--pdf',           required=False, action='store_true',    help='Build doc into PDF format')
	parser.add_argument('-P','--print',         required=False, action='store_true',    help='Print tex')
	
	# options
	parser.add_argument('-V','--vertical',      required=False, action='store_true',	help='Vertical orientation', default=False)
	parser.add_argument('-s','--fontsize',      required=False, action='store', 	 	help='Font Size: tiny, scriptsize, footnotesize, small, normalsize, large, Large, LARGE, huge, Huge')

	# operational actions
	parser.add_argument('-F','--force', 	  	required=False, action='store_true',    help='Force action to overwrite existing file')
	parser.add_argument('-v','--verbose',   	required=False, action='store_true',    help='Verbose Output')
	
	return parser.parse_args()

def run():

	# STEPS: 
	# 1. Parse arguments
	# 2. Find default file if needed
	# 3. Load and parse the yaml file
	# 4: Create Card object and load the yaml file
	# 5: Set options

	# STEP 1: Parse arguments
	args = parse_arguments()

	if args.verbose:
		print(args)

	# STEP 2: Find default file if needed 
	# if filename isn't specified find first yaml file in directory and try to compile that
	filename = args.filename
	if filename == '?':
		for file in os.listdir(os.getcwd()):
			if file.endswith(".yaml"):
				filename = file
				break

	# If no filename is provided / found then exit
	if filename == '?':
	    print("Error: No file found. Quitting.", file=sys.stderr)
	    exit(-1)

	filepath = os.path.expanduser(filename)

	# STEP 3: Load and parse the yaml file
	d = None
	try: 
		d = load(filepath)
	except FileNotFoundError:
		print("Error: File not found: " + args.filename, file=sys.stderr)
		exit(-1)
	except BaseException as e:
		print("Error: Unable to read in and parse yaml file: " + e.msg, file=sys.stderr)
		exit(-1)

	# STEP 4: Create Card object and load the yaml file
	card = Card(d)

	# STEP 5: Set options 
	options = {}

	if args.vertical:
		options['vertical'] = True

	if args.fontsize:
		options['fontsize'] = args.fontsize

	# STEP 6: Build the tex
	card.tex(options=options)

	if args.print:
		print(card)	

	if args.tex:
		output = args.output 

		if output is None:
			output = os.path.splitext(filename)[0] + ".tex"
		else:
			# If an output filepath was provided, check if it is a directory
			# If it is a directory, then flush out full file path with path + basename + .tex
			if os.path.isdir(os.path.expanduser(output)):
				output = output + os.path.splitext(filename)[0] + ".tex"

		save(card.tex_str, output)

		exit(0)

	if not args.tex or args.pdf:
		output = args.output 
		
		# If no output filepath is provided, use the source file path + .pdf
		if output is None:
			output = os.path.splitext(filename)[0] + ".pdf"
		else:
			# If an output filepath was provided, check if it is a directory
			# If it is a directory, then flush out full file path with path + basename + .pdf 
			if os.path.isdir(os.path.expanduser(output)):
				output = output + os.path.splitext(filename)[0] + ".pdf"

		card.pdf(output, force=True)

	return

if __name__ == '__main__':
    run()







#def clean():
#	dirpath = os.path.dirname(filename)
#	return 
#	if dirpath == '':
#		dirpath = os.getcwd()
#	
#	for file in os.listdir(dirpath):
#		if file.endswith((".tex", ".toc", ".log", ".aux", ".out", "synctex.gz", ".lot", ".lof", ".epub", ".mobi", ".pdf", )):
#			os.remove(os.path.join(dirpath, file))
