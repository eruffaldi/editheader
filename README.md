# Edit Header for C/C++
Bulk edit of the headers of C/C++ project files

Scan Files and Verify license for C/C++


 Usage:
 - select files using a combination of find/grep e.g.
   find . | grep -v buildosx | grep -v buildwin | grep -E ".*\.(cpp|hpp|h)$"
 - verify used headers or per-file
 	python editheader.py --filelist FILELIST --all --listlicenses
 	python editheader.py --filelist FILELIST --all --list
 - regenerate all
 	python editheader.py --filelist FILELIST --all --replace MYLICENSE
 - replace license