#!/usr/bin/env bash

if [ -n "$1" ]
then 
	echo "Uploading to pi@${1}..."
#	printf "HINT: The password should be 'raspberry'.\n\n"
	# shellcheck disable=SC2035
	sshpass -p raspberry scp -r * pi@"$1":~/vision2022
	printf "\n\nHINT: If it said 'read-only file system' then restart the RPI and try again.\n"
else 
	echo "No IP passed to first parameter."
fi 
