Apache Error Log Cleaner (Python)
========================

A Python script that returns a list of Apache errors without repeated errors. 

This helps you see trough important errors among thousands of repeated errors.

It can also show you errors grouped by frequency, with the most frequent errors on the top, or the least frequent errors at the top.

This script should work on any platform.

## Usage

Allow this script to be executed by running
```
chmod +x logcleaner.py
```

To run use:
```
./logcleaner.py logFileName
```
or 
```
python logcleaner.py logFileName
```

### Example Usage

	Showing the log file grouped by frequency
	```
	./logcleaner.py  -f logFileName 
	```
	
	Sorts the log file by descending frequency
	```
	./logcleaner.py  -f -o DESC logFileName    
	```
	
	Showing the first 20 errors grouped log lines 
	```
	./logcleaner.py  -s 20 logFileName       
	```

## Options:
```
 -h , --help                    Displays the help file.
 -f , --freq                    Display the frequency that each error line haves.
 -o STR , --order=STR           Allows the user to choose the sorting order by frequency,
                                STR possible values are ASC or DESC.
 -s NUM , --show=NUM            Shows the first NUM rows from the list.
```

## Warning:
- Using this program on very large files might cause your CPU usage to skyrocket.



