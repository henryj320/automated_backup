#!/bin/bash

source="/home/henry/Documents/GitHub/backup_cronjob/Tests/Test_Source"
target="/home/henry/Documents/GitHub/backup_cronjob/Tests/Test_Target/"


# Check that the server exists.
server=192.168.1.1
if ! ping -c 1 "$server"; then
    echo "No connection to server. Exiting."
    exit 1
fi

# Removes trailing "/" characters.
source=$(echo "$source" | sed 's/\/$//')
target=$(echo "$target" | sed 's/\/$//')

# Checks that the source and target exist.
if ! [[ -d "$source" ]]; then
    echo "Source does not exist. Exiting."
    exit 1
elif ! [[ -d "$target" ]]; then
    echo "Target does not exist. Exiting."
    exit 1
fi


overwrite="True"
condition="Recently Modified"
dry_run="False"

path_to_repo="/home/henry/Documents/GitHub/backup_cronjob/"



# Call the Python script with Click arguments
"$path_to_repo"backend/backend.py "$source" "$target" --overwrite "$overwrite" --condition "$condition" --dry_run "$dry_run"

notify-send "Automated Backup" "Backup to Rocky Server complete."
