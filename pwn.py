#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 @danlopgom
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# DISCLAMER This tool was developed for educational goals. 
# The author is not responsible for using to others goals.

import requests
import json
import argparse
from argparse import RawTextHelpFormatter
import datetime

parser = argparse.ArgumentParser(description="Tool to check if the accounts given at accounts.dat have been pwned", formatter_class=RawTextHelpFormatter)
args = parser.parse_args()

#Colours
RED = '\033[91m'
ENDC = '\033[0m'
GREEN = '\033[1;32m'
WHITE = '\033[1m'
BOLD = '\033[01m'

# Get the accounts
with open('accounts.dat', 'r') as f:
	accounts = f.readlines()

# Remove whitespace characters like `\n` at the end of each line
accounts = [x.strip() for x in accounts]

headers = {
    'User-Agent': 'pwncheck 1.0'
    #'From': 'youremail@domain.com'  # This is another valid field
}

for a in accounts:
	url = ('https://haveibeenpwned.com/api/v2/breachedaccount/%s') % (str(a))
	r = requests.get(url, headers=headers)
	print(40*"=")
	try:
		r_2=json.loads(r.content)
	except:
		print("[+] %s -> " + GREEN + "NOT leaked" + ENDC) % (str(a))
		continue

	count = len(r_2)

	print("[!] %s -> " + RED + "LEAKED" + ENDC) % (str(a))
	print("[+] Leaks: %s") % (str(count))
	print("[+] Details")
	for c in r_2:
		# Date format change
		date = datetime.datetime.strptime(c['BreachDate'], '%Y-%m-%d').strftime('%d/%m/%y')
		arr = [str(r) for r in c['DataClasses']]

		print("\t- {: <30} {: <10} {: >20}".format(c['Domain'], date, arr))
			
print(40*"=")
