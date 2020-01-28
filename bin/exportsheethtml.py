#!/usr/bin/env python

import os
import platform
import stat
import sys
import subprocess
import time
import traceback
import splunk.Intersplunk
import urllib
import urllib2
import time
import splunk.clilib.cli_common
import json
import sys
import splunk.rest
import datetime
import re
import csv
import logging
import logging.handlers
import sys
import json
from shutil import copyfile
import splunklib.client as client
from multiprocessing import Process
from signal import signal, SIGTERM
from time import sleep
import atexit
import requests
import os
import copy
from bs4 import BeautifulSoup
from StringIO import StringIO
import zipfile


# This code ensures that memory-mapped file support is added to core Splunk Python prior to pandas being imported. 
supported_systems = {
    ('Linux', 'i386'): 'linux_x86',
    ('Linux', 'x86_64'): 'linux_x86_64',
    ('Darwin', 'x86_64'): 'darwin_x86_64',
    ('Windows', 'AMD64'): 'windows_x86_64',
}

system = (platform.system(), platform.machine())
if system not in supported_systems:
    raise Exception('Unsupported platform: %s %s' % (system))

sa_scipy = 'Splunk_SA_Scientific_Python_%s' % (supported_systems[system])

mmap_path = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', sa_scipy, 'bin', supported_systems[system], 'lib', 'python2.7','lib-dynload')
mmap = "mmap.so"
splunk_python_package_loc = os.path.join(os.environ['SPLUNK_HOME'], 'lib', 'python2.7')
# sa_path = os.path.join(bundle_paths.get_base_path(), sa_scipy)
try:
    if not os.path.isdir(mmap_path):
        raise Exception('Failed to find location of mmap.so' % mmap_path)
    if not os.path.isdir(splunk_python_package_loc):
        raise Exception('Failed to find Splunk Python Package Location' % splunk_python_package_loc)
    else:
        copyfile(mmap_path+'/'+mmap, splunk_python_package_loc+'/'+mmap)

except Exception as e:
    results = []
    result = {}
    result["Error"] = str(e)
    results.append(result)
    splunk.Intersplunk.outputResults(results)
    sys.exit()


import pandas as pd

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
    splunkService = client.connect(token=sessionKey,app='SheetsAddonforSplunk')
    for storage_password in splunkService.storage_passwords:
        logger.info(storage_password.name)

def CreateToken(sessionKey, password, user, realm):
    splunkService = client.connect(token=sessionKey,app='SheetsAddonforSplunk')
    splunkService.storage_passwords.create(password, user, realm)

def DeleteToken(sessionKey, user):
    splunkService = client.connect(token=sessionKey,app='SheetsAddonforSplunk')
    try:
        splunkService.storage_passwords.delete(user,user)
    except Exception as e:
        logger.info(str(e))

def GetTokens(sesssionKey):
    splunkService = client.connect(token=sessionKey,app='SheetsAddonforSplunk')
    return splunkService.storage_passwords

def GetFiles(api_key, page_token, results, logger):
    try:
        r=requests.get('https://www.googleapis.com/drive/v3/files?pageToken'+page_token+'&access_token='+api_key+'&q=name+contains+%27.spreadsheet%27+or+name+contains+%27csv%27+or+name+contains+%27xls%27')
        r = json.loads(r.text)

        for file in r["files"]:
            result={}
        if "name" in file:
            result["name"] = file["name"]
        else:
            result["name"] = "(None)"

        if "id" in file:
            result["id"] = file["id"]
        else:
            result["id"] = "(None)"

        if "mimeType" in file:
            result["mimeType"] = file["mimeType"]
        else:
            result["mimeType"] = "(None)"
            results.append(result)

        if 'nextPageToken' in r:
            page_token=r["nextPageToken"]
            GetFiles(api_key, page_token, results, logger)
        else:
            return results
    except Exception as e:
        logger.info(str(e))
        return results



def GetSheet(api_key, id, fieldsKeep, fieldsDiscard, logger, subsheet, headerrow):
    try:
        results = []
        r=requests.get('https://www.googleapis.com/drive/v3/files/'+id+'/export?access_token='+api_key+'&mimeType=application/zip')

        f = StringIO()
        f.write(r.content)
        input_zip = zipfile.ZipFile(f)

        for line in input_zip.namelist():
            if "html" in line and subsheet in line:
                #result = {}
                fileContent = input_zip.open(line)
                data = fileContent.read()



                url_soup = BeautifulSoup(data)
                tables = []
                tables_html = url_soup.find_all("table")

                # Parse each table
                for n in range(0, len(tables_html)):

                    n_cols = 0
                    n_rows = 0

                    for row in tables_html[n].find_all("tr"):
                        col_tags = row.find_all(["td", "th"])
                        if len(col_tags) > 0:
                            n_rows += 1
                            if len(col_tags) > n_cols:
                                n_cols = len(col_tags)

                    # Create dataframe
                    df_frame = pd.DataFrame(index=range(0, n_rows), columns=range(0, n_cols))

                    # Create list to store rowspan values
                    skip_index = [0 for i in range(0, n_cols)]

                    # Start by iterating over each row in this table...
                    row_counter = 0
                    for row in tables_html[n].find_all("tr"):

                        # Skip row if it's blank
                        if len(row.find_all(["td", "th"])) == 0:
                            next

                        else:

                            # Get all cells containing data in this row
                            columns = row.find_all(["td", "th"])
                            col_dim = []
                            row_dim = []
                            col_dim_counter = -1
                            row_dim_counter = -1
                            col_counter = -1
                            this_skip_index = copy.deepcopy(skip_index)

                            for col in columns:

                                # Determine cell dimensions
                                colspan = col.get("colspan")
                                if colspan is None:
                                    col_dim.append(1)
                                else:
                                    col_dim.append(int(colspan))
                                col_dim_counter += 1

                                rowspan = col.get("rowspan")
                                if rowspan is None:
                                    row_dim.append(1)
                                else:
                                    row_dim.append(int(rowspan))
                                row_dim_counter += 1

                                # Adjust column counter
                                if col_counter == -1:
                                    col_counter = 0
                                else:
                                    col_counter = col_counter + col_dim[col_dim_counter - 1]

                                while skip_index[col_counter] > 0:
                                    col_counter += 1

                                # Get cell contents
                                cell_data = col.get_text()

                                # Insert data into cell
                                df_frame.iat[row_counter, col_counter] = cell_data
                                # Record column skipping index
                                if row_dim[row_dim_counter] > 1:
                                    this_skip_index[col_counter] = row_dim[row_dim_counter]

                        # Adjust row counter
                        row_counter += 1

                        # Adjust column skipping index
                        skip_index = [i - 1 if i > 0 else i for i in this_skip_index]

                    # Append dataframe to list of tables
                    tables.append(df_frame)

                i = 0
                row_incr = 0
                # Setup the dataframe to be returned as the processed table
                new_df = tables[0]

                # Replace any empty values with the word "null"
                new_df = new_df.fillna("null")

                # Iterate through every row looking for null values
                for index, row in new_df.iterrows():
                    row_incr += 1

                    # Set the header incrementer
                    i_incr = 0
                    # Iterate through every column in the row
                    while i < len(row):
                        # If the value is null, let's act on it
                        if row[i] == "null":
                            # Increment the header incrementer
                            i_incr += 1
                            # Set the value of the null header to the previous value plus the incrementer
                            row[i] = row[i - 1] + str(i_incr)
                        # Restart header incrementer
                        i_incr = 0
                        # Increment the column counter
                        i = i + 1
                    # Restart the column counter before next row
                    i = 0
                    if row_incr > 1:
                        break
                new_df.reindex(new_df)

                new_df = new_df.drop(columns=[0]).drop([0])
                new_df.columns = new_df.iloc[headerrow]
                new_df.reindex(new_df)
                new_df = new_df.iloc[headerrow + 1:]
                fieldsDiscard = fieldsDiscard.split(",")
                fieldsKeep = fieldsKeep.split(",") 
                if fieldsDiscard[0] != "":
                    for field in fieldsDiscard:
                        logger.info("Discarding Fields:"+field)
                        logger.info(str(new_df))
                        new_df.drop(field, axis=1,  inplace=True)
                    new_df.reindex(new_df)
                
                if fieldsKeep[0] != "":
                    logger.info("Keeping Fields:"+str(fieldsKeep))
                    logger.info(str(new_df))
                    new_df = new_df.filter(fieldsKeep)
                    new_df.reindex(new_df)

                logger.info(str(new_df))
                #result["content"] = str(new_df)
                #results.append(result)
                results = new_df.to_dict('records')

            return results


    except Exception as e:
        results = []
        result["ERROR"] = str(e)
        results.append(result)
        logger.info(str(e))
        return results


now = datetime.datetime.now()

logger = setup_logger(logging.INFO)


results,dummy,settings = splunk.Intersplunk.getOrganizedResults()
sessionKey = settings.get("sessionKey")
keywords, argvals = splunk.Intersplunk.getKeywordsAndOptions()

for result in results:
    try:
        #Get Google Drive Name and API Creds from Password Store
        username=result['username']
        password=result['clear_password']

        headerrow = int(argvals.get("headerRow",0))
	fieldsDiscard = argvals.get("fieldsDiscard","")
        fieldsKeep = argvals["fieldsKeep"]
        logger.info(fieldsKeep)
        fieldsKeep = fieldsKeep.replace("%20"," ")
        fileId = result['fileId']
        #Parse JSON API Creds
        tokens = json.loads(password)

        #Get Refresh Token
        refreshtoken = tokens["RefreshToken"]

        subsheet = result['subsheet']
        #Get the API Key and Refresh Token
        new_creds = RefreshToken(refreshtoken, username, sessionKey)

        #Get New API Key
        new_creds = json.loads(new_creds)
        api_key=new_creds["APIKey"]

        try:
            results = GetSheet(api_key, fileId, fieldsKeep, fieldsDiscard, logger, subsheet, headerrow)
        except Exception as e:
            logger.info(str(e))
            results = []
            result["Error"]=str(e)
            results.append(result)
        splunk.Intersplunk.outputResults(results)


    except Exception as e:
        logger.info(str(e))
        results = []
        result = {}
        result["Error"] = str(e)
        results.append(result)
        splunk.Intersplunk.outputResults(results)
