#!/usr/bin/python
import sys
import re
import getopt

"""
The idea is to create shell program that can be able to remove unwanted lines from a log file.
It requires python 2.4 or higher.
"""

package = 'hashlib'
bHashlib = True

try:
	import hashlib
except ImportError:
	import md5
	bHashlib = False

try:
	opts, args = getopt.getopt(sys.argv[1:], "fo:hs:", ['freq','order=','help','show='])
except getopt.GetoptError, err:
	print str(err) # Error if no parameter was recognized
	sys.exit(2)

if len(args) == 0:
	print "No file selected"
	sys.exit(2)

bFreq = False
bSortDesc = False
bShow = False
nShow = 0

strHelp = """
This program is for removing repeated Apache error log lines.

To run try using:
./logcleaner.py logFileName

NOTE:
Remember to allow this script to be executed by running
chmod +x logcleaner.py

WARNING:
Using this program on very large files might cause your CPU
usage to skyrocket.

OPTIONS:
 -h , --help                    Displays the help file.
 -f , --freq                    Display the frequency that each error line haves.
 -o STR , --order=STR           Allows the user to choose the sorting order by frequency,
                                STR possible values are ASC or DESC.
 -s NUM , --show=NUM            Shows the first NUM rows from the list.

EXAMPLES:
./logcleaner.py  -f logFileName             # Shows the log file grouped by frequency
./logcleaner.py  -f -o DESC logFileName     # Sorts the log file by descending frequency
./logcleaner.py  -s 20 logFileName          # Shows the first 20 grouped log lines 


"""

for strOption, strArg in opts:
	if strOption in ("-f" , "--freq"):
		bFreq = True
	elif strOption in ("-o", "--order"):
		if strArg.lower() == 'desc':
			bSortDesc = True
		elif strArg.lower() == 'asc':
			bSortDesc = False
		else:
			assert False, "Wrong order option. Only  'asc' or 'desc' available"
	elif strOption in ("-s", "--show"):
		bShow = True
		nShow = int(strArg)
	elif strOption in ("-h", "--help"):
		print strHelp
		sys.exit(0)
	else :
		assert False, strOption + " option was not found. Please run this script with -h parameter for showing help"
		sys.exit(2)

strFileName = args[0]

compiled = re.compile('\[.*?\] \[.*?\] \[.*?\] (.*)')

fh = open(strFileName, 'r')

dictRows = {}
dictFreq = {}
nLargest = 0

nTotalOriginal = 0

for strLine in fh:
	nTotalOriginal += 1
	strLine = strLine[:-1]

	if strLine.strip() == '':
		continue
	strResult = re.findall(compiled, strLine)[0]
	
	if bHashlib:
		m = hashlib.md5()
		m.update(strResult)
		strHash = m.hexdigest()
	else :
		strHash = md5.new(strResult).hexdigest()
	dictRows[strHash] = strResult
	if dictFreq.has_key(strHash):
		dictFreq[strHash] += 1
	else:
		dictFreq[strHash] = 1
	if dictFreq[strHash] > nLargest:
		nLargest = dictFreq[strHash] 

fh.close()

listSorted = sorted(dictFreq, key = lambda x: dictFreq[x])

nDigits = len(str(nLargest))

if bSortDesc:
	listSorted.reverse()

if bShow:
	try:
		listSorted = listSorted[:nShow]
	except Error:
		pass

for strHash in listSorted:
	if bFreq:
		strFormat = "[%" + str(nDigits) + "d]  %s"
		print (strFormat) % ( dictFreq[strHash], dictRows[strHash])
	else :
		print "%s" % (dictRows[strHash])

raw_input("Press enter to exit")
