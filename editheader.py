from __future__ import print_function
# Edit Header for C/C++
# Scan Files and Verify license for C/C++
#
# Emanuele Ruffaldi 2015-2016
#
# Usage:
# - select files using a combination of find/grep e.g.
#   find . | grep -v buildosx | grep -v buildwin | grep -E ".*\.(cpp|hpp|h|hxx|c)$"
# - verify used headers or per-file
# 	python editheader.py --filelist FILELIST --all --listlicenses
# 	python editheader.py --filelist FILELIST --all --list
# - regenerate all with the MYLICENSE file
# 	python editheader.py --filelist FILELIST --all --replace MYLICENSE
# - replace license
import argparse
import os,re
import sys
from collections import defaultdict
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def findfiles(args):
	rem = re.compile(".*\.(cpp|hpp|c|h)$")
	files = []
	#build expression for the exclusion of paths and files

	for x in args.paths:
		if os.path.isfile(x):
			files.append(x)
		else:
			matches = []
			for root, dirnames, filenames in os.walk(x):

				# TODO check path exclusion
				for filename in filenames:
					if rem.match(filename):
						# TODO check file exclusion
						files.append(os.path.join(root, filename))
	return files

def extractlicense(filename,args):
	lines = []
	doublemode = False
	hasmarker = False
	for e,l in enumerate(open(filename,"r")):
		l = l.strip()
		if e == 0:
			# first line
			if not l.startswith("/*"):
				if l.startswith("//"):
					doublemode = True
				elif l.startswith("#"):
					return (False,False,e,[])
				else:
					return (False,False,e,"OTHER")
			l = l[2:].strip()
			if l != "" and l != "*":
				lines.append(l)
		else:
			# stop on preprocessor
			if l.startswith("#"):
				break
			elif doublemode:
				if l.startswith("//"):
					l = l[2:].strip()					
					if l == args.marker:
						break
					else:
						lines.append(l)
			else:
				if l.startswith("*/"):
					if not args.special:
						break
				else:
					if l.startswith("*"):
						l = l[1:].strip()					
					if l == args.marker:
						hasmarker = True
						if not args.special:
							break
					else:
						lines.append(l)
	return (doublemode,hasmarker,e,lines)

def main():
	parser = argparse.ArgumentParser(description='List and modify licenses')
	parser.add_argument('paths', metavar='paths', type=str, nargs='*',
	                   help='list of files')
	parser.add_argument('--filelist', help="takes files from this list instead from path")
	parser.add_argument('--list', action='store_true',help="list file found with details")
	parser.add_argument('--listlicenses', action='store_true',help="list licenses with related files")
	parser.add_argument('--listnames', action='store_true',help="list filenames only")
	#parser.add_argument('--exclude',type=str,nargs='*',help="relative paths to be excluded")
	parser.add_argument('--marker', help="marker used at the end of the first block comment",default="--")	
	parser.add_argument('--all', help="select all files, otherwise only ones with marker present or empty license",action="store_true")
	#parser.add_argument('--selecttopragma', help="removes license froms elected files",action="store_true")
	parser.add_argument('--remove', help="Removes All licenses",action="store_true")
	parser.add_argument('--dry-run', help="Test Mode, does nothing",action="store_true")
	parser.add_argument('--replace', help="Replace all licenses with new file")
	parser.add_argument('--special', help="eat everything",action="store_true")
	parser.add_argument('--new', help="Instead of replacing files produce a file with appended .new",action="store_true")
	parser.add_argument('--regen', help="Extract and Regenerate the Licence",action="store_true")

	args = parser.parse_args()

	newlicense = None
	if args.remove:
		newlicense = []
	elif args.replace:
		newlicense = open(args.replace,"r").read().split("\n")
	elif args.regen:
		newlicense = []

	files = []
	if args.filelist:
		files = [x.strip() for x in open(args.filelist,"r") if x.strip() != ""]
	else:
		files = findfiles(args)
	wfiles = [(x,extractlicense(x,args)) for x in files]
	if not args.all:
		# pick only marker or empty
		wfiles = [x for x in wfiles if x[1][1] or len(x[1][3]) == 0]

	if args.listnames:
		for f,l in wfiles:
			print (f)
	elif args.list:
		for f,l in wfiles:
			(doublemode,hasmarker,e,lines) = l
			print (bcolors.OKGREEN,f,bcolors.ENDC)
			print ("\tdoublemode",doublemode)
			print ("\thasmarker",hasmarker)
			print ("\tendline",e)
			print ("\tlines",lines)
	elif args.listlicenses:
		ll = defaultdict(list)
		for f,l in wfiles:
			(doublemode,hasmarker,e,lines) = l
			ll[tuple(lines)].append(f)
		for k,v in ll.iteritems():
			print (k)
			for y in v:
				print ("\t",y)
	elif newlicense is not None:
		if len(newlicense) != 0:
			a = ["/**"]
			for x in newlicense:
				a.append(" * " + x)
			a.append(" * " +args.marker)
			a.append(" */")
			newlicenseblock = a
		else:
			newlicenseblock = []
		for f,l in wfiles:
			doublemode,hasmarker,e,existing = l
			ff = open(f,"r")
			w = ff.read().split("\n")
			ff.close()
			pre = w[0:e]
			post = w[e:]
			if not args.regen and newlicense == existing:
				print ("same",f)
			else:
				if args.regen:
					newlicenseblock = existing
				tf = (args.new and f+".new" or f)
				if not args.dry_run:
					print ("updating",f,len(newlicenseblock),"post",len(post))
					open(tf,"w").write("\n".join(newlicenseblock + post))
				else:
					print ("test updating",tf,"newlicenselines",len(newlicenseblock),"from",e,"bodylines",len(post))
	else:
		print ("no action")
if __name__ == '__main__':
	main()