domain=$1
now=$(date +"%Y-%m-%d_%H-%M-%S")

dig @8.8.8.8 $domain A +auth +trace +stats +multiline > dig_results_$domain\_$now.txt