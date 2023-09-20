from pathlib import Path
import os
import shutil
import logging
import sys
import glob
import time
from datetime import datetime

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
        self.source = Path(os.path.expanduser(source))  # Replaces "~" with the full path.
        self.target = Path(os.path.expanduser(target))
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
        # Skip because overwrite is allowed.
        if self.overwrite:
            return True
        
        # If target is empty
        if len(os.listdir(self.target)) == 0:
            return True
        
        return False


    def output(self, time_taken: float, count: int) -> dict:
        """Outputs the results to the user."""

        # Time taken
        # Files transferred
        # Directories Ignored

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
            sys.exit()

        # Exit early if !overwrite and target directory is not empty.
        if not self.check_target_ready():
            logging.error("Overwrite is set to 'False' but target directory is not empty.")
            sys.exit()
        
        # Find all files in the source firectory.
        source_files = glob.glob(f"{self.source}/**", recursive=True)
        source_files.pop(0)  # Removes the root directory.

        count = 0  # Number of files replicated.
        directories_ignored = []
        files_ignored = []
        time_taken = 0

        # Create each directory and copy each file.
        for index, file in enumerate(source_files):
            split_point = file.find("/")
            new_path = f"{self.target}/{file[split_point + 1:]}"

            if Path(file).is_dir():
                os.mkdir(new_path)
                logging.info(f"New directory created: {new_path}")
            else:
                shutil.copy(source_files[index], new_path)
                count = count + 1
        
        end = time.perf_counter()
        time_taken = end - start
        
        output = self.output(time_taken, count) 

        logging.info(f"Backup job completed in {time_taken:0.4f} seconds.")
        return output



if __name__ == "__main__":
    source = Path("./Test_Source")
    target = Path("./Test_Target")

    backup = Backup(source, target)
    result = backup.transfer_files()

    print(result)
