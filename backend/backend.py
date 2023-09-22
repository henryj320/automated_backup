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
        

    def check_target_ready(self) -> bool:
        """Checks that the target empty if overwrite is set to false."""

        if not isinstance(self.overwrite, bool):
            logging.error("Overwrite is not set to a bool! Exiting.")
            raise TypeError

        # Skip because overwrite is allowed.
        if self.overwrite:
            return True
        
        # If target is empty
        if len(os.listdir(self.target)) == 0:
            return True
        
        return False


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
        if not self.check_target_ready():
            logging.error("Overwrite is set to 'False' but target directory is not empty.")
            print("Overwrite is set to 'False' but target directory is not empty.")
            sys.exit("Overwrite is set to 'False' but target directory is not empty.")
        
        # Find all files in the source firectory.
        source_files = glob.glob(f"{self.source}/**", recursive=True)
        source_files.pop(0)  # Removes the root directory.

        count = 0  # Number of files replicated.
        directories_ignored = []
        files_ignored = []
        time_taken = 0
        total_items = len(source_files)

        # Used for the progress bar/
        with alive_bar(total_items, bar="filling") as progress_bar:

            # Create each directory and copy each file.
            for index, file in enumerate(source_files):
                # Removes all directories from the path so just the file is left.

                file_only = file
                while "/" in file_only:
                    split_point = file_only.find("/")
                    file_only = file_only[split_point + 1:]
                new_path = f"{self.target}/{file_only}"

                if Path(file).is_dir():
                    os.mkdir(new_path)
                    logging.info(f"New directory created: {new_path}")
                else:
                    shutil.copy(source_files[index], new_path)
                    count = count + 1
                

                # sleep(0.5)
                progress_bar()  # Add another notch to the progress bar
            
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


    backup = Backup(source, target)

    backup.empty_directory(target)
    
    result = backup.transfer_files()

    # backup = Backup(1, target)
    # result = backup.check_dir_exists()

    # print(result)




    # print(result)
