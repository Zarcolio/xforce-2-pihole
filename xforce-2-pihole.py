#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import re
import socket
import requests
import time
from requests.auth import HTTPBasicAuth

# <Configure me>
strApiKey = 'FILL_ME'
strApiPass = 'FILL_ME'
# </Configure me>


text1 = ': forwarded '
text2 = ' to'

for strInput in sys.stdin:
	strInput = strInput.rstrip()
	
	reFound = re.search(text1+'(.+?)'+text2, strInput)
	if reFound:
		strHost = reFound.group(1)
		if not strHost.endswith(".in-addr.arpa"):
			try:
				strIp = socket.gethostbyname(strHost)
				reqXforceIpr = requests.get('https://api.xforce.ibmcloud.com/ipr/'+strIp, auth=HTTPBasicAuth(strApiKey, strApiPass))
				if bool(re.search('"cats":\{"Malware":57\}', reqXforceIpr.text)):
					print("! "+strHost)
					subprocess_start = subprocess.Popen("pihole -b " + strHost +" --comment \"By xforce-2-pihole\"", shell=True, stdout=subprocess.PIPE)
					subprocess_return = subprocess_start.stdout.read()
					
					if bool(re.search('already exists in whitelist, it has been moved to blacklist!', subprocess_return.decode('utf-8'))):
						print("whitelist again")
						strResult = os.system("pihole -w " + strHost +" --comment \"By xforce-2-pihole\"")
			except socket.gaierror:
				wait(1)
				pass

