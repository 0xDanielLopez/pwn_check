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
# V2

import requests
import json
import argparse
from argparse import RawTextHelpFormatter
import datetime
from time import sleep
from key import *

parser = argparse.ArgumentParser(description="Tool to check if the emails given at emails.dat have been pwned", formatter_class=RawTextHelpFormatter)
args = parser.parse_args()

#Colours
RED = '\033[91m'
ENDC = '\033[0m'
GREEN = '\033[1;32m'
WHITE = '\033[1m'
BOLD = '\033[01m'

# Get the emails
with open('emails.dat', 'r') as f:
	emails = f.readlines()

# Remove whitespace characters like `\n` at the end of each line
emails = [x.strip() for x in emails]

headers = {
	'User-Agent': 'pwncheck 2.0',
	'hibp-api-key': API_key
	#'From': 'youremail@domain.com'  # This is another valid field
}

file_pwned_urls="pwned_pastes_urls.txt"
file_pwned_emails="pwned_pastes_emails.txt"

# Create the file
with open(file_pwned_urls, 'w'): pass
with open(file_pwned_emails, 'w'): pass

# Total number of emails
t_emails = len(emails)
c_emails = 0
pwned_emails = 0

for a in emails:
	sleep(3)
	url = ('https://haveibeenpwned.com/api/v3/pasteaccount/%s') % (str(a))
	r = requests.get(url, headers=headers)
	print(40*"=")
	c_emails += 1	
	print("[+] Count: %s/%s (%s%%)") % (str(c_emails),str(t_emails),str(round(100 * float(c_emails)/float(t_emails),2)))
	
	try:
		r_json=json.loads(r.content)
	except:
		print("[+] Emails leaked for now: %s/%s (%s%%)") % (str(pwned_emails),str(t_emails),str(round(100 * float(pwned_emails)/float(t_emails),2)))
		print("[+] Checking:")
		print("\t - " + BOLD + "%s -> " + GREEN + "NOT leaked" + ENDC) % (str(a))
		continue

	count = len(r_json)
	pwned_emails += 1
	print("[+] Emails leaked for now: %s/%s (%s%%)") % (str(pwned_emails),str(t_emails),str(round(100 * float(pwned_emails)/float(t_emails),2)))
	print("[+] Checking:")
	print("\t - " + BOLD + "%s -> " + RED + "LEAKED" + ENDC) % (str(a))	
	# Include the email on the external file
	with open(file_pwned_emails, 'a') as f:
		f.write("%s\n" % a)
	print("[+] Leaks: %s") % (str(count))
	print("[+] Details")

	try:
		if r_json['statusCode'] == 429:
			print(r_json)
			print("Esperamos")
			sleep(5)
			raw_input()
	except:
		#print("We are OK")
		for c in r_json:
			print("\t- {: <30} {: <10}".format(c['Source'], c['Id']))

			with open(file_pwned_urls, 'a') as f:
				if c['Source'] == "Pastebin":
					f.write("https://pastebin.com/%s\n" % c['Id'])
				elif c['Id'].startswith("http"):
					f.write("%s\n" % c['Id'])
print(40*"=")
