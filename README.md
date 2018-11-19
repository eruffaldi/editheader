# Edit Header for C/C++
Bulk edit of the headers of C/C++ project files

Scan Files and Verify license for C/C++

# Usage

	usage: editheader.py [-h] [--filelist FILELIST] [--list] [--listlicenses]
	                     [--listnames] [--marker MARKER] [--all] [--remove]
	                     [--test] [--replace REPLACE] [--special] [--new]
	                     [--regen]
	                     [paths [paths ...]]

	List and modify licenses

	positional arguments:
	  paths                list of files

	optional arguments:
	  -h, --help           show this help message and exit
	  --filelist FILELIST  takes files from this list instead from path
	  --list               list file found with details
	  --listlicenses       list licenses with related files
	  --listnames          list filenames only
	  --marker MARKER      marker used at the end of the first block comment
	  --all                select all files, otherwise only ones with marker
	                       present or empty license
	  --remove             Removes All licenses
	  --dry-run            Test Mode, no file changed
	  --replace REPLACE    Replace all licenses with new file
	  --special            eat everything
	  --new                Instead of replacing files produce a file with appended
	                       .new
	  --regen              Extract and Regenerate the Licence