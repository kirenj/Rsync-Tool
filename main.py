import time
import sys
import ipaddress
import os
import subprocess
import shlex


def ping_server(ip):
    ip_addr = ipaddress.ip_address(ip)
    result = os.system(f"ping -c 1 {ip_addr} > /dev/null 2>&1") # /dev/null = redirects the standard output (stdout) to /dev/null, essentially discarding it.
    # 2>&1 = Redirects the standard error (stderr) to the same location as stdout, so error messages are also supressed.
    if result == 0:
        return "Remote IP is active"
    else:
        return "Remote IP is Unreachable"


# ping check placeholder
def time_delay(time_displayed = 3, interval = 0.5):
    print("Please wait", end="", flush=True)
    for j in range (time_displayed):
        time.sleep(interval)
        print(".", end="", flush=True)
    print("Done!")


# MAIN Rsync Function
def rsync_func(remote_username, remote_server_ip, dest_path, source_path, options=""):
    rsync_command = f"rsync -avz {options} {source_path} {remote_username}@{remote_server_ip}:{dest_path}"
    print(f"Running command: {rsync_command}")
    try:
        task_run = subprocess.run(shlex.split(rsync_command), check=True, capture_output=True, text=True)
        # subprocess.run to execute the rsync command
        # shlex.split will split the rsync command to individal components (eg: 'rsync' '-avz' 'remote_username'...)
        # check=True: This tells subprocess.run() to raise a CalledProcessError if the command returns a non-zero exit status (indicating an error)
        # capture_output=True: This tells subprocess.run() to capture the standard output (stdout) and standard error (stderr) from the command. This allows us to process the commands output in Python.
        # text=True: This ensures that the output captured (stdout and stderr) will be in the form of strings (rather than bytes). This is useful because it allows you to directly manipulate and check the output.
        print("Rsync completed successfully!")
    except subprocess.CalledProcessError as e:
        print("Error during Rsync operation!!")
        print(e.stderr) # prints the rsync error message


# Rsync Back-up check
def rsync_backup_check(remote_username, remote_server_ip, dest_path, source_path, options=""):
    #constructing a Rsync dry run command
    rsync_command = f"rsync -avzn {options} {source_path} {remote_username}@{remote_server_ip}:{dest_path}"
    try:
        task_run = subprocess.run(shlex.split(rsync_command), check=True, capture_output=True, text=True)
        # If the output is empty, no files have been changed
        if task_run.stdout.strip() == "":
            print("No changes detected. Back-up is not required")
            return False
        else:
            print("Changes detected. Back-up required")
            print(task_run.stdout) #Display what items are to be transferred
            return True
    except subprocess.CalledProcessError as e:
        print("Error during rsync dry run")
        print(e.stderr) #prints the rsync error messages
        return False


print("*********************************Rync Tool!*******************************")

remote_server_ip = input("Enter the IP of the remote server: ")
try_ping = input(f"Do you wish to ping the remote server at {remote_server_ip}? (Yes/No): ").lower()

if try_ping == "yes":
    time_delay()
    response = ping_server(remote_server_ip)
    print(response)
elif try_ping == "no":
    pass
else:
    print("You didn't enter a valid input......exiting")
    sys.exit()

remote_username = input("Enter the remote server username: ")
dest_path = input("Enter the destination file path of the remote server: ")
source_path = input("Enter the file path of the files you want to back-up: ")
options = input("Rsync options by default are 'a', 'v' & 'n'. Enter any additional options if needed: ")
back_up_check = input("Do you wish to check if your files have already been backed up? (Yes/No): ").lower()

if back_up_check == "yes":
    check_result = rsync_backup_check(remote_username, remote_server_ip, dest_path, source_path, options)
    if check_result == True:
        start_rsync = input("Do you wish to start the Rsync process? (Yes/No): ").lower()
        if start_rsync == "yes":
            rsync_func(remote_username, remote_server_ip, dest_path, source_path, options)
        else:
            print("Quitting script!")
            sys.exit()
else:
    start_rsync = input("Do you wish to start the Rsync process? (Yes/No): ").lower()
    if start_rsync == "yes":
        rsync_func(remote_username, remote_server_ip, dest_path, source_path, options)
    else:
        print("Quitting script!")
        sys.exit()
