# Apache Log Anaylzer
Work in progress mrjob apachelog anaylzer for large data sets.

## Local run
To test locally on one apache file.
* python apache_analyzer.py apache_log_file --output-dir=./output/

or for multiple files
* python apache_analyzer.py apache_log_file_dir/* --output-dir=./output/

After this run has finished run the following.
* python show_graphs  -o ./output/ -S

This will run a simple HTTP server on localhost:8000, To review results you can see localhost:8000/graphs.html

## Information
This script will provide a number of raw counts for the following information:
* Request_URL
* Referrer_URL
* Monthly_hits
* Daily_hits
* Ten_minute_hits
* one_minute_hits(This can be configurable to show all hits or just top x hits)
* Response_Time_in_seconds
* Return_code
* Referrer



## TODO
* Update docs to run on EC2/cloud for large scale operations.
* Make a apache log format to python regex function.
* Create output for all sections of the apache log line.
* Allow request URL regexs.
* Update the counted parts of the log line.
* Create the ability to keep history and add it to the current run.
* Create a conf file to track what to keep counts of and how to display graphs.
* Add an example

## Issues:
* The regex is setup for a specific apache log line at the moment.

