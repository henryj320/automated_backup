from pathlib import Path
import os
import shutil
import logging
import sys
import glob
import time
from datetime import datetime
from alive_progress import alive_bar

from time import sleep

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='backend_cronjob.log', level=logging.INFO)
# logger = logging.getLogger('backup_logger')

class Backup:
    def __init__(
            self,
            source: Path,
            target: Path,
            overwrite: bool = False,
            overwrite_condition: str = "Target Empty",
            # "Target Empty":  Fails if target is not empty.
            # "Ignore": Do not copy over any files that already exist in target.
            # "Duplicate":  Keep both old and new file in target with a (1) at the end.
            # "Recently Modified"
            ignored_ext: list = [],
            ignored_files: list = [],
            ignored_directories: list = [],
            dry_run: bool = False
        ):
        """Initialise the Backup instance."""
        try:
            self.source = Path(os.path.expanduser(source))  # Replaces "~" with the full path.
            self.target = Path(os.path.expanduser(target))
        except TypeError as e:
            logging.error("Source or Target directory are not a string.")
            sys.exit("Source or Target directory are not a string.")

        self.overwrite = overwrite
        self.overwrite_condition = overwrite_condition
        self.ignored_ext = ignored_ext
        self.ignored_files = ignored_files
        self.ignored_directories = ignored_directories
        self.result = {}
        self.dry_run = dry_run
    

    def check_dir_exists(self) -> bool:
        """Checks that the source and target directories exist."""

        if self.source.is_dir() and self.target.is_dir():
            return True
        return False
        

    def check_target_ready(self) -> tuple:
        """Checks that the target empty if overwrite is set to false."""

        if not isinstance(self.overwrite, bool):
            return (False, "Overwrite is not set to a bool! Exiting.")
        

        # Skip because overwrite is allowed.
        if self.overwrite:
            return (True, "")
        
        # If target is empty
        if len(os.listdir(self.target)) == 0:
            return (True, "")
        # If overwrite_condition is "Ignore" or "Duplicate".
        elif self.overwrite_condition != "Target Empty":
            return (True, "")

        
        return (False, "Overwrite is set to 'False' but target directory is not empty.")


    def output(self, time_taken: float, count: int) -> dict:
        """Outputs the results to the user."""

        # Check the inputs are valid.
        try:
            if time_taken < 0 or count < 0:
                logging.error("The time taken or number of files cannot be less than 0.")
                raise ValueError
        except TypeError as e:
            logging.error(f"The time_taken or count are the incorrect type. {e}")
            sys.exit("The time_taken or count are the incorrect type.")

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return {
            "completed_at": now,
            "files_transferred": count,
            "time_taken": time_taken,
            "ignored_ext": self.ignored_ext,
            "ignored_files": self.ignored_files,
            "ignored_directories": self.ignored_directories
        }
    

    def check_ready(self):
        """Exits prematurely if any of the checks fail."""
        
        # Exit early if source or target directory does not exist.
        if not self.check_dir_exists():
            logging.error("Source or target directory does not exist.")
            sys.exit("Source or target directory does not exist.")

        # Exit early if !overwrite and target directory is not empty.
        check_target_ready_bool, check_target_ready_str = self.check_target_ready()
        if not check_target_ready_bool:
            logging.error(check_target_ready_str)
            print(check_target_ready_str)
            sys.exit(check_target_ready_str)

            # TODO: Make it return and then just print that in the transfer_files() section so it passes the tests.
        
    

    def list_files(self) -> list:
        """List all of the files in the source."""
        # Find all files in the source firectory.
        source_files = glob.glob(f"{self.source}/**", recursive=True)
        source_files.pop(0)  # Removes the root directory.

        return source_files
    

    def remove_start_path(self, file):
        """Gets rid of the beginning of the path."""

        # file_only = file
        # while "/" in file_only:
        source_split = str(self.source).split("/")
        source_end = source_split[len(source_split) - 1]
        split_point = file.split("/")
        # print(f"{source_end} is source end")
        # print(split_point)
        while split_point[0] != source_end:
            split_point.pop(0)  # Removes "Test_Source"
            # new_start = split_point[:-1]
            # file_only = file_only[split_point + 1:]
        split_point.pop(0)

        return split_point


    def check_file_last_modified(self, filepath: str, hours: int) -> bool:
        """Checks whether the file was modified within the last x hours.

        Args:
            filepath (str): Path to the file to check.
            hours (int): Number of hours .

        Returns:
            bool: True if file was modified within the last x hours.
        """

        # value is a floating point number giving the number of seconds since the epoch
        time_modified = os.path.getmtime(filepath)

        # time_modified_timestamp = time.ctime(time_modified)

        seconds_since_modified = time.time() - time_modified
        minutes_since_modified = seconds_since_modified / 60
        hours_since_modified = minutes_since_modified / 60

        if hours_since_modified > hours:
            return False
        
        return True


    def transfer_files(self):
        """Transfers the files from the source to the directory, respecting the user inputs."""

        logging.info(f"Transfer process started with the following settings: Overwrite: {self.overwrite}, Dry Run: {self.dry_run}.")
        start = time.perf_counter()

        self.check_target_ready()
        source_files = self.list_files()        

        count = 0  # Number of files replicated.
        time_taken = 0
        total_items = len(source_files)

        # Used for the progress bar/
        with alive_bar(total_items, bar="filling") as progress_bar:

            # ignored_patterns = []
            # for ext in self.ignored_ext:
                # ignored_patterns.append(f"*{ext}")  # Adds *.jpg

            # Create each directory and copy each file.
            for index, file in enumerate(source_files):
                # Removes all directories from the path so just the file is left.

                
                # print("here")
                split_point = self.remove_start_path(file)
                print(split_point)
                new_path = ""
                for dir in split_point:
                    new_path = new_path + "/" + dir
                new_path = f"{self.target}/{new_path}"
                # print(new_path)
                # new_path = f"{self.target}/{file_only}"

                # print("FILE:")
                # print(file)
                if Path(file).is_dir():
                    if file in self.ignored_directories:
                        progress_bar() 
                        logging.info(f"{file} not created as in ignored directories list.")
                        new_path = ""
                        continue
                    if self.dry_run:
                        logging.info(f"DRY RUN: New directory would be created: {new_path}.")
                        progress_bar()  # Add another notch to the progress bar
                        new_path = ""
                        continue
                    os.mkdir(new_path)
                    logging.info(f"New directory created: {new_path}.")

                # If it is a file, not directory.
                else:
                    file_location = os.path.dirname(file)
                    print(f"file_location - {file_location}")
                    print(f"new_path - {new_path}")
                    if self.dry_run:
                        logging.info(f"DRY RUN: File would be copied to: {new_path}.")
                        progress_bar()  # Add another notch to the progress bar
                        new_path = ""
                        continue
                    elif file_location in self.ignored_directories:
                        progress_bar() 
                        logging.info(f"{file} not created as in ignored directories list.")
                        new_path = ""
                        continue
                    elif file in self.ignored_files:
                        progress_bar() 
                        logging.info(f"{file} not created as in ignored files list.")
                        new_path = ""
                        continue
                    elif Path(source_files[index]).suffix not in self.ignored_ext:

                        # Check whether file was modified withint the last x hours.
                        if self.overwrite and self.overwrite_condition == "Recently Modified":

                            modified_witin = 7 * 24
                            modified_witin = 1 / 120  # 30 seconds

                            if self.check_file_last_modified(file, modified_witin):
                                shutil.copy(source_files[index], new_path)
                                count = count + 1
                            else: 
                                progress_bar() 
                                logging.info(f"{file} not overwritten because not updated in the last {modified_witin} hours.")
                                continue

                        else:

                            shutil.copy(source_files[index], new_path)
                            count = count + 1
                

                # sleep(0.5)
                progress_bar()  # Add another notch to the progress bar

                new_path = ""
            
            end = time.perf_counter()
            time_taken = end - start

        
        output = self.output(time_taken, count) 

        logging.info(f"Backup job completed in {time_taken:0.4f} seconds.")
        return output
    

    def empty_directory(self, directory: str) -> bool:
        """Remove all files in the given directory"""
        files = glob.glob(f"{directory}/**", recursive=True)
        files.pop(0)
        for file in files:
            # If a file, not a directory.
            if os.path.isfile(file) or os.path.islink(file):
                # Deletes the file.
                os.unlink(file)
            
            # If a directory
            elif os.path.isdir(file):
                # Deletes the directory and all its contents.
                shutil.rmtree(file)
        
        return True



if __name__ == "__main__":
    source = Path("./Test_Source")
    target = Path("./Test_Target")


    # backup = Backup(source, target, ignored_ext=[".txt"], ignored_directories=["Test_Source/Ignored_Dir"])
    # backup = Backup(source, target, ignored_ext=[".txt"], ignored_directories=["Test_Source/Ignored_Dir"])

    # backup = Backup(source, target, ignored_files=["Test_Source/Hey/Im_unwanted.txt"])


    # backup.empty_directory(target)

    good_source = "Test_Source"
    good_target = "Test_Target"

    # good_source = "/home/henry/Documents/Repositories/backup_cronjob/Test_Source"
    # good_target = "/home/henry/Documents/Repositories/backup_cronjob/Test_Target"
    # ignored_directory = f"{good_source}/IgnoredDirectory"
    # backup = Backup(good_source, good_target, ignored_directories=[ignored_directory])
    
    
    backup = Backup(good_source, good_target, overwrite=True, overwrite_condition= "Recently Modified")
    result = backup.transfer_files()

    # backup = Backup(1, target)
    # result = backup.check_dir_exists()

    # print(result)

    # last_mod = backup.check_file_last_modified("Test_Source/Test.md", 7)
    # print(datetime.now())
    # print(time.time())

    # seconds_since_modified = time.time() - last_mod

    # print(seconds_since_modified)

    # minutes_since_modified = seconds_since_modified / 60
    # hours_since_modified = minutes_since_modified / 60
    # print(minutes_since_modified)
    # print(hours_since_modified)



    # print(result)
