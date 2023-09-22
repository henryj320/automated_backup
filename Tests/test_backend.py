import sys
import pathlib
import os
import pytest
from datetime import datetime
from time import sleep

# Adds "backend" to be a location that the interpretter searches for modules.
sys.path.append("./backend") 

from backend import Backup



def fill_source(number_of_files: int, source: pathlib.PosixPath) -> None:
    """Take the source and fill it with some example files"""

    for x in range(0, number_of_files):
        # Creates a new file
        file = open(f"{source}/file{x}.txt", "w")


def test_files(tmp_path):
    fill_source(10, tmp_path)
    print(os.listdir(tmp_path))



def test_check_dir_exists(tmp_path):
    """Test the check_dir_exists() function in backend.py."""
    fill_source(10, tmp_path)  # Fill the tmp_path with 10 files.

    # Good example.
    backend_instance = Backup(tmp_path, "./Tests/Test_Target")
    assert backend_instance.check_dir_exists()

    # Fails with no source.
    backend_instance_no_source = Backup("/does_not_exist", "./Tests/Test_Target")
    assert not backend_instance_no_source.check_dir_exists()

    # Fails with no target.
    backend_instance_no_target = Backup(tmp_path, "/does_not_exist")
    assert not backend_instance_no_target.check_dir_exists()

    # Non-string source.
    with pytest.raises(SystemExit) as e:
        backend_instance_no_target = Backup(123, "./Tests/Test_Target")

    # Non-string target.
    with pytest.raises(SystemExit) as e:
        backend_instance_no_target = Backup(tmp_path, 123)


def test_check_target_ready(tmp_path):
    """Test the check_target_ready() function in backend.py."""

    # Good example.
    backend_empty_target = Backup("./Test_Source", tmp_path)
    assert backend_empty_target.check_target_ready()

    # Overwrite with empty target.
    backend_empty_target_overwrite = Backup("./Test_Source", tmp_path, overwrite=True)
    assert backend_empty_target_overwrite.check_target_ready()

    # Overwrite with non-empty target.
    backend_empty_target_overwrite = Backup("./Test_Source", tmp_path, overwrite=True)
    fill_source(10, tmp_path)  # Fill the tmp_path with 10 files.
    assert backend_empty_target_overwrite.check_target_ready()

    # Not overwrite with non-empty target.
    assert not backend_empty_target.check_target_ready()
    
    # Non-bool  overwrite.
    backend_empty_target_int_overwrite = Backup("./Test_Source", tmp_path, overwrite=1)
    with pytest.raises(TypeError) as e:
        backend_empty_target_int_overwrite.check_target_ready()


def test_output():

    backend = Backup("./Test_Source", "./Test_Target")

    # Good example.
    good_time_taken = 4.0
    good_count = 10
    good_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    result = backend.output(good_time_taken, good_count)
    assert result["completed_at"] == good_now
    assert result["files_transferred"] == good_count
    assert result["time_taken"] == good_time_taken
    assert result["ignored_directories"] == []

    # Negative time_taken.
    negative_time_taken = -1
    with pytest.raises(ValueError) as e:
        backend.output(negative_time_taken, good_count)

    # Negative count.
    negative_count = -10
    with pytest.raises(ValueError) as e:
        backend.output(good_time_taken, negative_count)

    # Non string/int.
    with pytest.raises(SystemExit) as e:
        backend.output("ABC", good_count) 
    assert "The time_taken or count are the incorrect type." in str(e.value)



def test_transfer_files():
    good_source = "./Tests/Test_Source"
    good_target = "./Tests/Test_Target"

    backend = Backup(good_source, good_target)

    # Good example.
    backend.empty_directory(good_source)  # Empty the Target.
    fill_source(10, good_source)
    backend.empty_directory(good_target)  # Empty the Target.
    backend.transfer_files()
    assert len(os.listdir(good_target)) == 10

    # Not overwrite with non-empty target.
    with pytest.raises(SystemExit) as e:
        backend.transfer_files()
    assert "Overwrite is set to 'False' but target directory is not empty." in str(e.value)
    
    # Fails with no source.
    with pytest.raises(SystemExit) as e:
        backend_no_source = Backup(None, good_target)
        backend_no_source.transfer_files()
    assert "Source or Target directory are not a string." in str(e.value)

    # Fails with no target.
    with pytest.raises(SystemExit) as e:
        backend_no_source = Backup(good_source, None)
        backend_no_source.transfer_files()
    assert "Source or Target directory are not a string." in str(e.value)

    # Overwrite with empty target.
    backend_overwrite = Backup(good_source, good_target, overwrite=True)
    backend_overwrite.empty_directory(good_source)
    fill_source(10, good_source)
    backend_overwrite.empty_directory(good_target)
    result = backend_overwrite.transfer_files()
    assert result["completed_at"] == datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    assert result["files_transferred"] == 10
    assert result["time_taken"] < 10
    assert result["ignored_directories"] == []

    # Overwrite with non-empty target.
    backend_overwrite.empty_directory(good_source)
    fill_source(10, good_source)
    result = backend_overwrite.transfer_files()
    assert result["completed_at"] == datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    assert result["files_transferred"] == 10
    assert result["time_taken"] < 10
    assert result["ignored_directories"] == []

    # With ignored directories.
    ignored_directory = f"{good_source}/IgnoredDirectory"
    backend = Backup(good_source, good_target, ignored_directories=[ignored_directory])
    backend.empty_directory(good_source)
    backend.empty_directory(good_target)
    os.mkdir(ignored_directory)
    fill_source(10, good_source)
    fill_source(10, ignored_directory)
    result = backend_overwrite.transfer_files()
    assert result["completed_at"] == datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    assert result["files_transferred"] == 10
    assert result["time_taken"] < 10
    assert result["ignored_directories"] == [ignored_directory]

    # TODO: Check it works when ignored directories is implemented.





    # With ignored files.

    # With ignored extensions.

    # Dry run.

    backend.empty_directory(good_source)
    backend.empty_directory(good_target)
