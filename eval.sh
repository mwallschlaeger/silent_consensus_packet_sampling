#!/bin/bash

EXEC="python3 seq_collector_file_based"

# PARAMETERS
# interval history_len history_steps_in_interval
parms[0]="1 10 10"
parms[1]="1 5 1"
parms[2]="1 5 2"
parms[3]="1 2 1"
parms[4]="2"
parms[5]="2"
parms[6]="5"

for i in {1..5} ; do
	for i in `ls pcap_files` ; do 
		echo $i 
	 done
done
