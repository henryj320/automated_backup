from pathlib import Path


class Backup:
    def __init__(
            self,
            source: Path,
            target: Path,
            overwrite: bool = False,
            ignored_ext: list = [],
            ignored_files: list = [],
            ignored_directories: list = [],
            result: dict = {}
        ):
        """Initialise the Backup instance."""
        pass

# Check that the directories exist

# Check that the target is empty (if !overwrite)

# Copy the files to target.

# Output the overview info as JSON.