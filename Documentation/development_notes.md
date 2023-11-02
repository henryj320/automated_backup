# automated_backup

Last update: 2023-11-02 18:02
<br><br>

## Development Notes for automated_backup

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
        - Fail if target is not empty ("Target Empty") ✅
        - Ignore files that already exist ("Ignore") ✅
        - Create a "(1)" duplicate of the file ("Duplicate") ✅
    - Just making sure it works with full paths
        - Yep, seems fine
    - Separating the transfer_files() into separate functions
    - Testing "Overwrite ➡️ Update all files" works
        - Yep, it already works
10. Fixing the tests
    - All working
    - TODO: Linting, bash script, frontend?
11. Code cleanup
    - Removing commented code
    - Making a *requirements.txt*
    - Making the *ton.ini* file
    - Now working with ` tox -e lint `, ` tox ` or ` tox -e tests `.
    - Slowly linting
    - Need to incorporate Black into it.
12. Moved over to the new Kubuntu 23.10 distro
    - Having issues with  ` × This environment is externally managed ` whenever I try to pip install
    - ` pip install pip==22.3.1 --break-system-packages `
        - Downgrading pip slightly from 23.3.1 to 22.3.1
    - Now I can ` pip install alive_progress `
    - ` pip install -r requirements.txt `
13. Testing genuinely using it
    - Mounting the SharedFolder
        -  Created "/mnt/SharedFolder/Henry/"
        - Setting up mount on boot
            - ` sudo vi /etc/fstab `
            - Added ` //192.168.1.20/sharedFolder/Henry /mnt/sharedFolder/Henry cifs credentials=/etc/samba/credentials,uid=1000,gid=1000 0 0 `
        - Setting up samba credentials
            - ` sudo vi /etc/samba/credentials `
            - ` sudo chmod 600 /etc/samba/credentials `
        - Seeing if it works
            - ` systemctl daemon-reload `
            - ` sudo mount -a `
            - ` sudo apt install cifs-utils `
14. Creating click options
    - So that I can run it from a Bash script.
    - Trying to run ` python3 backend/backend.py ./Tests/Test_Source ./Tests/Test_Target `
        - That works!
    - ` python3 backend/backend.py ./Tests/Test_Source ./Tests/Test_Target --overwrite True `
        - Looks good
15. Writing a bash script to run it
    - Made *auto_backup_bash.sh* in "Frontend".
    - ` chmod +x ` on the Bash script and Python script.
    - I had to add a "Shebang" line to the Python script
    - It works!
    - Making it so that the user can input the parameters when running the script.
    - Struggling to pass the arrays as parameters.
16. Fixing Errors
    - Getting an Error "FileExistsError: [Errno 17] File exists: '/mnt/SharedFolder/Henry/Backups/Documents/Automated Backups/DnD//The Bank Job (May 2023)' "
        - Looks like it cannot recreate files if they already exist.
    - All good, except "Ignored Dir" is not at all working at the moment.
    - For some reason, have to run it once with "Target Empty" and then you can use recently modified
17. Setting up a cronjob
    - ` export EDITOR=vim && export VISUAL=vim `
    - ` crontab - e`
    - ` @reboot sleep 600 && /home/henry/Documents/GitHub/backup_cronjob/Frontend/auto_backup_bash.sh >> /home/henry/Documents/GitHub/backup_cronjob/Frontend/Ideapad-Cronjob.log 2>&1 
    - It logs a lot`
18. Added a notification on completion
    - ` sudo apt update `
    - ` sudo apt upgrade `
    - ` sudo apt install libnotify-bin `
    - ` notify-send "this is the summary" `
19. Moving the Rocky automated backup script to its own place - "/home/henry/Documents/Software/Automated_Backup/"
    - Also genericised the *auto_backup_bash.sh* script.
    - It all works. Looks good!
        - Backs up 1 minute after reboot if it can connect to the server.
    - ` @reboot sleep 60 && /home/henry/Software/Automated_Backup/auto_backup_bash.sh >> /home/henry/Software/Automated_Backup/Ideapad-Cronjob.log 2>&1 `
20. Future to do:
    - Sync all files
        - If removed, also remove
        - If updated at all, update
    - Frontend
    - Decrease how much it logged.
    - Make it so that "files_transferred" does not increase if the file is skipped.
