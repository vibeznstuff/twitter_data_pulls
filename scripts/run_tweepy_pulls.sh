# Extract run path from JSON config file
# Requires jq command to be installed
run_path=`jq '.run_path' tweepy_pull_config.json`
run_path="${run_path%\"}"
run_path="${run_path#\"}"

log_path=`jq '.log_path' tweepy_pull_config.json`
log_path="${log_path%\"}"
log_path="${log_path#\"}"

python3 $run_path/tweepy_pulls.py > $log_path/tweepy_log.txt 2>&1
