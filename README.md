## Twitter Data Pulls
This is a simple facility for pulling batch data extracts from twitter feeds based on configured twitter topics which you can subscribe to.

The parameters for the data pull scripts are managed in a JSON file which will need to be modified by the individual.

This script utilizes the Tweepy Python package and is designed to be run continuously throughout the day on a scheduler. Personally, I have set this up using crontab on a Linux AWS Lightsail instance. 

The scheduled executable is a shell script to be run within unix, however the same could be done on Windows.

Example JSON Config File:

{
	"consumer_key": "XXXXXXXXXXXXXX",
	"consumer_secret" : "XXXXXXXXXXXXXX",
	"access_token" : "XXXXXXXXXXXXXX",
	"access_token_secret" : "XXXXXXXXXXXXXX",
	"out_path" : "/path/to/out_files",
	"log_path" : "/path/to/log_files",
	"run_path" : "/path/to/scripts",
	"limit_buffer" : 10,
	"topics" : [
		"Donald Trump", 
		"Barak Obama", 
		"Global Warming", 
		"Black Lives Matter"
		]
}

Consumer Key, Consumer Secret, Access Token and Access Token Secret are all API security parameters provided when you obtain access to the Twitter API as a developer.

out_path: The location you'll want to store the output CSV files with the twitter data

log_path: The location to store log output of each run

run_path: The location where the scripts directory will be stored (e.g. tweepy_pulls.py and run_tweepy_pulls.sh)

limit_buffer: This is a parameter used to throttle the data pulls depending on how close you are getting to your API search call limit. Currently the limit is 180 calls within 15 minutes. The script is programmed to stop making calls when the remaining calls in your 15 minute window is < (limit_buffer) * rand() + (Count of Topics). In the above JSON config example, assuming rand() resolved to 1, this would equal 14 (i.e. stop when you have 14 calls remaining).

topics: These are the topics your script will subscribe to. For each topic, the script will pull 100 recent tweets and store them into a CSV file. If one does not already exist, the script creates a directory to store output for each topic along with CSV files within those sub-directories. The data accumulates into the CSV file until the day ends (the files are time-stamped) and a new file is started.

