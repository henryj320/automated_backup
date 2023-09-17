from pathlib import Path
import os
import shutil
import logging
import sys
import glob

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='backend_cronjob.log')
# logger = logging.getLogger('example')


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


    def output(self):
        """Outputs the results to the user."""
        pass


    def transfer_files(self):
        """Transfers the files from the source to the directory, respecting the user inputs."""
        
        # Exit early if source or target directory does not exist.
        if not self.check_dir_exists():
            logging.error("Source or target directory does not exist.")
            sys.exit()

        # Exit early if !overwrite and target directory is not empty.
        if not self.check_target_ready():
            logging.error("Overwrite is set to 'False' but target directory is not empty.")
            sys.exit()
        
        # for dir in os.listdir(self.source):

        #     dir = Path(dir)
        #     print(dir)

        #     full_path = Path(os.path.join(self.source, dir))
        #     print(full_path.is_dir())

        #     # If is a directory
        #     if full_path.is_dir():
        #         new_dir = Path(os.path.join(self.target, dir))
        #         os.mkdir(new_dir)
            
        #     # If it is a file
        #     else:
        #         shutil.copy(full_path, target)
        
        # pass

        # source_files = glob.glob(f"{self.source}/*")
        # source_files = []
        source_files = glob.glob(f"{self.source}/**", recursive=True)
        source_files.pop(0)  # Removes the root directory.
        print(source_files)

        for index, file in enumerate(source_files):

            split_point = file.find("/")
            new_path = f"{self.target}/{file[split_point + 1:]}"
            if Path(file).is_dir():
                # print(file[split + 1:])
                print(new_path)
                os.mkdir(new_path)

            else:
                # filename = file.split("/")
                # filename = filename[len(filename) - 1]
                # new_path = f"{new_path}/{filename}"
                shutil.copy(source_files[index], new_path)

        # for dirpath, dirname, file in os.walk(self.source):
        #     print(dirpath)
        #     print(dirname)
        #     print(file)
        #     print("")




if __name__ == "__main__":
    source = Path("./Test_Source")
    target = Path("./Test_Target")

    backup = Backup(source, target, False, [], [], [], False)
    backup.transfer_files()

