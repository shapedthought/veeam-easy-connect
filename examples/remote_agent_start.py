from veeam_easy_connect import VeeamEasyConnect
import urllib3
urllib3.disable_warnings()
from datetime import datetime
import time
from tqdm import tqdm
import json
from datetime import datetime, timedelta
import os
import sys

# This script requires a creds.json file with:
# username = username to log into the API
# password
# url = just the DNS or IP of the host
# job_name = name of job that you want to start
# see example creds file in examples directory

# install dependcies = pip install tqdm veeam-easy-connect

# set time offset if there is a time difference between the VBR server and local host
# 4 = local host is 4 min faster, -4 = local host is 4 min slower
TIME_OFFSET = 4

# timeout value for monitoring
TIMEOUT = 10

# sleep time between session progress checks
SLEEP_TIME = 30

def countdown(count: int) -> None:
    for x in tqdm(range(count), desc="count down"):
        time.sleep(1)

def clear_screen() -> None:
    os.system("clear")

def check_sessions(old_time: datetime, job_name: str, vec: VeeamEasyConnect) -> str:
    """
    function that takes the following params:
    old_time = time when the script was started in UTC
    job_name = the job name
    vec = the VeeamEasyConnect instance

    It sends a request to the sessions endpoint with the ?format=Entities parameter.
    It then filters out the jobs by the job name parameter.
    Next it sorts the jobs by their date and splits the name at the @ and converts it to a datetime object.
    It then compares that time with the old_time parameter to check that it was created after then start of the script.
    This is done because it can take some time for the session to be added.
    If the current session has been added then it will return the session URL, otherwise it will return "None"
    """
    agent_sessions = vec.get("agents/backupSessions?format=Entities", False)
    filter_sessions = []
    for i in agent_sessions['Refs']:
        if job_name in i['Name']:
            filter_sessions.append(i)
    # sorts the sessions but the name parameter
    sorted_sessions = sorted(filter_sessions, key= lambda x: x['Name'], reverse=True)
    # pulls the name parameter from all the sorted list of dictionaries
    names = [x['Name'] for x in sorted_sessions]
    print(f"Top session is currently {names[0]}")
    # performs the check between the supplied time and the time job on the session
    sess_time = datetime.strptime(names[0].split("@")[-1], '%Y-%m-%d %H:%M:%S')
    if (old_time - timedelta(minutes=TIME_OFFSET)) > sess_time:
        return "None"
    else:
        return sorted_sessions[0]['Links'][1]['Href']


def main():
    # gets the creds from the credentials file
    clear_screen()
    with open("creds.json", "r") as jd:
        creds = json.load(jd)
    
    # set up the VeeamEasyConnect object, False skips SSL verification
    vec = VeeamEasyConnect(creds['username'], creds['password'], False)
    print("Logging in")

    # Log into the API
    vec.ent_man().login(creds['url'])
    job_name = creds["job_name"]

    print("Getting jobs")
    # gets all the agent jobs
    jobs = vec.get("query?type=AgentBackupJob&format=Entities", False)

    # finds the job in question and grabs the UID by splitting the Name parameter
    for i in jobs['Entities']['AgentBackupJob']['AgentBackupJobs']:
        if job_name in i['Name']:
            uid = i['UID'].split(":")[-1]
    
    print(f"UID of job is: {uid}")

    # set the current time in UTC
    current_time = datetime.utcnow()
    
    # start the backup job
    print("Starting job")
    start_url = f"agents/jobs/{uid}?action=start"
    start_res = vec.post(start_url, {}, False)
    print(f"Task ID: {start_res['TaskId']}, State: {start_res['State']}")

    print("Waiting 10 seconds")
    countdown(10)

    clear_screen()
    # loop running the check_sessions function above
    print("Waiting for the session to start")
    count = 1
    while True:
        sess_url = check_sessions(current_time, job_name, vec)
        if sess_url == "None":
            print(f"Try: {count}. Still waiting for session")
        else:
            print("Found session, continuing")
            break
        time.sleep(10)
        count += 1

    error_count = 0
    clear_screen()
    # loop to monitor the progress of the job
    print("Monitoring job, waiting 30 seconds between checks")
    while True:
        
        sess_res = vec.get(f"{sess_url}?format=Entity")
        # if statement to check the length of the returned object as it may not have the session added yet
        if len(sess_res['BackupJobSessions']) > 0:
            sess_res = sess_res['BackupJobSessions'][0]
            print(f"State: {sess_res['State']}, Progress: {sess_res['Progress']}")
            if sess_res['State'] != "Working" and sess_res['Progress'] == 100:
                print("Job finished")
                break
            # check if the timeout has been met and quit if it has
            if datetime.utcnow() > current_time + timedelta(minutes=TIMEOUT):
                sys.exit("Timeout has been met, quitting")
        else:
            # added a get out clause so it doesn't get stuck in an infinite loop
            if error_count > 10:
                sys.exit("Sessions took too long, quitting")
            print("Sessions still warming up, waiting")
            error_count += 1
        time.sleep(SLEEP_TIME)
        clear_screen()

if __name__ == "__main__":
    main()