import splunk.Intersplunk 
from multiprocessing import Process
from signal import signal, SIGTERM
from time import sleep
import atexit
import requests
import os
import urllib
import urllib2
import time
import splunk.clilib.cli_common
import json
import sys
import splunk.rest
import datetime
import re
import logging
import logging.handlers
import sys
import json
import splunklib.client as client


def setup_logger(level):
    logger = logging.getLogger('my_search_command')
    logger.propagate = False  # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(level)

    file_handler = logging.handlers.RotatingFileHandler(
        os.environ['SPLUNK_HOME'] + '/var/log/splunk/googledrive.log', maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def RefreshToken(refresh_token, user, sessionKey):
    try:
        #Refresh Token 
        req = urllib2.Request('https://eop2idyodk.execute-api.us-west-2.amazonaws.com/prod/refreshgoogledrivekey?refresh_token='+refresh_token)
        response = urllib2.urlopen(req)
        codes = response.read()
        DeleteToken(sessionKey, user)
	codes=codes.replace("}", ", \"RefreshToken\": \""+refresh_token+"\"}")
        CreateToken(sessionKey, codes, user, user)
        return codes
    except Exception as e:
        logger.info(str(e))

def ListTokens(sessionKey):
    splunkService = client.connect(token=sessionKey,app='GoogleDriveAddonforSplunk')
    for storage_password in splunkService.storage_passwords:
        logger.info(storage_password.name)

def CreateToken(sessionKey, password, user, realm):
    splunkService = client.connect(token=sessionKey,app='GoogleDriveAddonforSplunk')
    splunkService.storage_passwords.create(password, user, realm)

def DeleteToken(sessionKey, user):
    splunkService = client.connect(token=sessionKey,app='GoogleDriveAddonforSplunk')
    try:
        splunkService.storage_passwords.delete(user,user)
    except Exception as e:
        logger.info(str(e))

def GetTokens(sesssionKey):
    splunkService = client.connect(token=sessionKey,app='GoogleDriveAddonforSplunk')   
    return splunkService.storage_passwords

def GetCourses(api_key, page_token, results, logger):
	try:
		r=requests.get('https://classroom.googleapis.com/v1/courses?pageSize=1000&pageToken'+page_token+'&access_token='+api_key+'&teacherId=me')
		r = json.loads(r.text)

		for course in r["courses"]:
			result={}
		if "name" in course:
			result["name"] = course["name"]
		else:
			result["name"] = "(None)"
                 
		if "courseState" in course:
			result["courseState"] = course["courseState"]
		else:
			result["courseState"] = "(None)"		


		if "id" in course:
			result["id"] = course["id"]
		else:
			result["id"] = "(None)"
		
		if "creationTime" in course:
			result["creationTime"] = course["creationTime"]
		else:
			result["mimeType"] = "(None)"
			results.append(result)
	
		if 'nextPageToken' in r:
			page_token=r["nextPageToken"]
			GetCourses(api_key, page_token, results, logger)	
		else:
			return results
	except Exception as e:
		logger.info(str(e))
		return results

now = datetime.datetime.now()

logger = setup_logger(logging.INFO)


results,dummy,settings = splunk.Intersplunk.getOrganizedResults()
sessionKey = settings.get("sessionKey")

for result in results:
	try:
		#Get Google Drive Name and API Creds from Password Store
		username=result['username']
		password=result['clear_password']

		#Parse JSON API Creds
		tokens = json.loads(password)
	
		#Get Refresh Token
		refreshtoken = tokens["RefreshToken"]

		#Get the API Key and Refresh Token
		new_creds = RefreshToken(refreshtoken, username, sessionKey)
		
		#Get New API Key	
		new_creds = json.loads(new_creds)
		api_key=new_creds["APIKey"]
		r=requests.get('https://classroom.googleapis.com/v1/courses?pageSize=1000&access_token='+api_key+'&teacherId=me')

		r = json.loads(r.text)

		results = []
		for course in r["courses"]:
			result={}
			if "name" in course:
				result["name"] = course["name"]
			else:
				result["name"] = "(None)"
			
			if "courseState" in course:
				result["courseState"] = course["courseState"]
			else:
				result["courseState"] = "(None)"	
			
			if "id" in course:
				result["id"] = course["id"]
			else:
				result["id"] = "(None)"
		
			if "creationTime" in course:
				result["creationTime"] = course["creationTime"]
			else:
				result["creationTime"] = "(None)"
			results.append(result)

		if 'nextPageToken' in r:
			page_token=r["nextPageToken"]
			results = GetCourses(api_key, page_token, results, logger)

		splunk.Intersplunk.outputResults(results)

        	
	except Exception as e:
		logger.info(str(e))
		results = []
		result = {}
		result["Error"] = str(e)
		results.append(result)
		splunk.Intersplunk.outputResults(results)