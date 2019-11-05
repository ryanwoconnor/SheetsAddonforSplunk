
# Sheets App for Splunk

- [Sheets App for Splunk](#sheets-app-for-splunk)
  * [Requirements](#requirements)
  * [Installing Required Apps](#installing-required-apps)
    + [Install Sheets App for Splunk](#install-sheets-app-for-splunk)
    + [Install Python for Scientific Computing](#install-python-for-scientific-computing)
  * [Configure Apps](#configure-apps)
    + [Setup Sheets App for Splunk](#setup-sheets-app-for-splunk)
    + [Setup Sheets App with custom python libraries](#setup-python-for-scientific-computing-with-custom-python-libraries)
  * [Recommended Sheets Data Format](#recommended-sheets-data-format)
    + [Sheets Feature Support](#sheets-feature-support)
  * [Security](#security)
      - [Revoking Access](#revoking-access)


## Requirements

For full-functionality of this app, you will want to install side-by-side with the following Splunk Apps:

* Splunk App: Python for Scientific Computing.

_Note: Make sure you install the correct version of Python for Scientific Computing for your OS_
* Python for Scientific Computing - Linux 64-bit - https://splunkbase.splunk.com/app/2882/
* Python for Scientific Computing - Mac - https://splunkbase.splunk.com/app/2881/
* Python for Scientific Computing - Linux 32-bit - https://splunkbase.splunk.com/app/2884/
* Python for Scientific Computing - Windows - https://splunkbase.splunk.com/app/2883/

This App is tested against

* Splunk 7.1 and Above
* Mac OSX
* Ubuntu Linux

## Installing Required Apps

### Install Sheets App for Splunk
1. Install Splunk
2. Clone SheetsAddonforSplunk into /opt/splunk/etc/apps
3. Start Splunk
4. Login to Splunk

### Install Python for Scientific Computing
1. Download the appropriate Python for Scientific Computing app off of Splunkbase. 
2. From the Splunk Homepage click on the Gear Icon next to Apps
3. Select “Install App From File”
4. Click “Choose File” and select the downloaded file. 
5. Click “Upload”
6. Click on “Restart Now”

## Configure Apps

### Setup Sheets App for Splunk
1. Open Sheets App for Splunk from the Apps Dropdown
2. Click “Continue to App Setup Page”
3. Follow Instructions to Get an API Key
4. Restart Splunk

### Setup Sheets App with custom python libraries
**_Please keep in mind that this step will not survive future upgrades of this app. If you do update the Google App, you will need to repeat this step_**

1. Navigate to Sheets Apps bin directory:
```
cd $SPLUNK_HOME/etc/apps/SheetsAddonforSplunk/bin/
```

2. Install the following Python packages:

```
pip install pandas bs4 --target=.

```

## Recommended Sheets Data Format

This app allows you to import data from a Google Sheet into Splunk or a CSV file stored in Google Drive. You can start by selecting your Google Account, and then choosing one of the sheets that you have available. For more information on creating Google Sheets, you can visit https://www.google.com/sheets/about/

### Sheets Feature Support
Each Google Sheet you create comes with the possibility of a wide range of features. Unfortunately some of those features make formatting very complex and they are not currently supported within Splunk. The purpose of this app is mostly to be able to lookup "CSV-like" data from a Google Sheet. That means that your spreadsheet should look something like the following screenshot and hopefully abide by the following guidelines.

1. Row 1 should be reserved for your "header". These are also known as "column names" or "feature names". An example of a header is highlighted in green in the screenshot. You do not need to highlight your header in your document. 

2. All data should remain within the bounds of your header. So if you have 4 column names (like in the screenshot) you should only have data in columns A-D, not in column E. Your data should also start in Row 2, not in Row 1. Sample data is highlighted in yellow in the screenshot. You do not need to highlight your data in your document. 

3. Avoid using merged cells wherever possible. We have taken steps to be able to support merged cells, but keep in mind that things like merged cells are only for aesthetics and are not useful when trying to process large amounts of data. So use these sparingly and at your own risk. 

4. You are  able to lookup multiple subsheets inside of a Google Sheet. You can select any Spreadsheet and any subsheet. 

If you've followed these guidelines and are still encountering errors, please reach out. 

![Alt text](/appserver/static/sheet_info.jpg?raw=true "Auth Option 1")

## Security

Security is the largest area of concern with this app. In order to help with security we have done a couple of things. 

1. This Splunk App will only request Read-Only Access to your Google Drive. The app cannot modify or delete anything in your Google Account.  
2. Splunk does not view any of your data, the only people that will be able to access your Google Drive data is anyone who has admin access to your Splunk instance once this app is setup. 
3. We specifically do not recommend setting this app up on a shared instance if you have any concerns about other admins seeing the content in the Google Account you authenticate with. 

Our current recommended setup would look like the following, where you would only authenticate this app to an account where you specifically share out the files you want to use in Splunk. This way the app does not have access to your entire Google Drive. 
![Alt text](/appserver/static/auth1.jpg?raw=true "Auth Option 1")

#### Revoking Access
If you need to revoke access to the Splunk App for any reason, you can do so by visiting the following Website. https://myaccount.google.com/permissions



