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
import splunklib.client as client

class Unbuffered:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

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


now = datetime.datetime.now()

logger = setup_logger(logging.INFO)
#logger.info("Let's Begin")

sys.stdout = Unbuffered(sys.stdout)
sys.stdout.flush()

#Just grab some Splunk Environment Info and log it
splunk_home = os.path.expandvars("$SPLUNK_HOME")
splunk_pid = open(os.path.join(splunk_home, "var", "run", "splunk", "conf-mutator.pid"), 'rb').read()
sessionKey = sys.stdin.readline().strip()

#Connect to Splunk
try:
    #Second GET Method
    splunkService = client.connect(token=sessionKey,app='GoogleDriveAddonforSplunk')
except Exception as e:
    logger.info(str(e))

credentials = GetTokens(sessionKey)
for credential in credentials:
    try:
        #Get Google Drive Name and API Creds from Password Store
        username=credential.content.get('username')
        password=credential.content.get('clear_password')
        
        #Parse JSON API Creds
        tokens = json.loads(password)
        
        #Get the API Key and Refresh Token
        apikey = tokens['APIKey']
        refreshtoken = tokens['RefreshToken']
        RefreshToken(refreshtoken, username, sessionKey)

    except Exception as e:
        logger.info(str(e))


