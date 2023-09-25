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


    def transfer_files(self):
        """Transfers the files from the source to the directory, respecting the user inputs."""

        logging.info(f"Transfer process started with the following settings: Overwrite: {self.overwrite}, Dry Run: {self.dry_run}.")
        start = time.perf_counter()
        
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
        
        # Find all files in the source firectory.
        source_files = glob.glob(f"{self.source}/**", recursive=True)
        source_files.pop(0)  # Removes the root directory.
        print("Here")
        print(source_files)

        count = 0  # Number of files replicated.
        directories_ignored = []
        files_ignored = []
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
                # print("here")
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

    good_source = "Tests/Test_Source"
    good_target = "Tests/Test_Target"
    ignored_directory = f"{good_source}/IgnoredDirectory"
    backup = Backup(good_source, good_target, ignored_directories=[ignored_directory])

    
    result = backup.transfer_files()

    # backup = Backup(1, target)
    # result = backup.check_dir_exists()

    # print(result)




    # print(result)
