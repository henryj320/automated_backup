# backup_cronjob

Last update: 2023-09-27 21:54
<br><br>

## Development Notes for backup_cronjob

1. Set up the repository.
2. Set up the basic "Backup" class.
3. Could use a progress bar in the terminal
    - https://builtin.com/software-engineering-perspectives/python-progress-bar
4. Set up each method.
5. Wrote the initial script.
6. Next steps:
    - Add logging. ✅
    - Output the final result using ` output(self) `. ✅
    - Add a progress bar. ✅
    - Add testing.
    - Add the other options (e.g. overwrite)
7. Setting up the progress 
    - https://github.com/rsalmei/alive-progress
    - ` pip install alive-progress `
    - Adding the code
8. Adding the tests.
    - ` pip install pytest `
    - Learning how to import Backup
    - Writing the tests
    - You can run it with ` pytest ` while in the project root directory.
    - Trying to see coverage
        - ` pip install pytest-cov `
        - Can now run ` pytest --cov ` or  ` coverage report ` or ` coverage report --fail-under=70 `
        - More info on ` pytest --cov ` here: https://pytest-cov.readthedocs.io/en/latest/config.html#reference
    - Writing lots more tests.
    - Adding a dry run capability.
    - Looks like it currently fails if a directory has the same name as a file
        - ` FileExistsError: [Errno 17] File exists: 'Test_Target/Hey' `
    - All tests are now complete.
9. Now that the tests are ready, I need multiple options for ` overwrite `. Here are the options that would be useful:
    - **Overwrite**
        - Update all files ✅ (Default)
        - Update file if modified within the last x days ("Recently Modified") ✅
    - **Not overwrite**
        - Fail if target is not empty ("Target Empty")
        - Ignore files that already exist ("Ignore")
        - Create a "(1)" duplicate of the file ("Duplicate")
    - Just making sure it works with full paths
        - Yep, seems fine
    - Separating the transfer_files() into separate functions
    - Testing "Overwrite ➡️ Update all files" works
        - Yep, it already works
