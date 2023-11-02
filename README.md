# automated_backup

Last update: 2023-11-02 23:24
<br><br>

## automated_backup

**Title**: automated_backup

**Date Started**: 2023-09-17

**Date Completed**: 2023-11-02

**Language**: Python

**Overview**: A bash script that can be run as a CRON job. The script allows you to define a source and target, and then copies the files over to the target.

**Result**: The python script is ready, and has 100% test coverage. There is also a Bash script ready and running on a cronjob to back up my main laptop to the server upon reboot.

## Running the Project

### Using Commandline

The easiest way to run Automated Backup is to run the Python script. Run the following commands:

```bash
python -m venv venv  # Create a virtual environment.
./venv/bin/activate OR .\venv\Scripts\activate  # Enter the virtual environment.

pip install .

python3 ./backend/backend.py /path/to/source /path/to/target
```

You can add specific parameters using ` --overwrite bool `, ` --condition string `, ` --ignored_ext [str] `, ` --ignored_files [str] `, ` --ignored_dir [str] `, ` --dry_run bool `.


### Using a Bash Script

Use the *auto_backup_bash.sh* script inside of "Frontend" directory as a reference. Adjust the ` source ` and ` target ` and set the other conditions in the Python script. Note that ` --ignored_ext [str] `, ` --ignored_files [str] `, ` --ignored_dir [str] ` are not currently working in the Bash script.
