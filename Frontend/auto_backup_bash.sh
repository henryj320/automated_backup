#!/bin/bash

# Prompt the user for the source and target directories.
# read -e -i "/home/" -p "Enter the source directory: " source
# read -e -i "$source" -p "Enter the target directory: " target
# read -e -i "False" -p "Overwrite existing files? (True/False) " overwrite
# if [ "${overwrite,,}" = "True" ]; then
    # read -e -i "Target Empty" -p "Under what condition should files be overwritten? (Default/Recently Modified) " condition
# else
    # read -e -i "Target Empty" -p "Under what condition should files be overwritten? (Target Empty/Ignore/Duplicate) " condition
# fi
# read -e -i "False" -p "Is this a dry run? (True/False) " dry_run


source="/home/henry/Documents/GitHub/backup_cronjob/Tests/Test_Source"
target="/home/henry/Documents/GitHub/backup_cronjob/Tests/Test_Target/"

source=$(echo "$source" | sed 's/\/$//')  # Removes trailing "/" characters.
target=$(echo "$target" | sed 's/\/$//')

# source="/home/henry/Documents/Pets"
# target="/mnt/SharedFolder/Henry/Backups/Documents/Automated Backups/Pets"

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
# "$path_to_repo"backend/backend.py "$source" "$target" --overwrite "$overwrite" --condition "$condition" --dry_run "$dry_run"
"$path_to_repo"backend/backend.py "$source" "$target" --overwrite "$overwrite" --condition "$condition" --dry_run "$dry_run"

