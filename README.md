
# Google App for Splunk

## Installation Steps

## Install Google App for Splunk
1. Install Splunk
2. Clone GoogleDriveAddonforSplunk into /opt/splunk/etc/apps
3. Start Splunk
4. Login to Splunk

### Install Python for Scientific Computing
1. Download the appropriate Python for Scientific Computing app off of Splunkbase. For Mac, this app is https://splunkbase.splunk.com/app/2881/
2. From the Splunk Homepage click on the Gear Icon next to Apps
3. Select “Install App From File”
4. Click “Choose File” and select the downloaded file. 
5. Click “Upload”
6. Click on “Restart Now”

### Install Splunk Machine Learning Toolkit
1. Download the Splunk Machine Learning Toolkit from Splunkbase https://splunkbase.splunk.com/app/2890/
2. From the Splunk Homepage click on the Gear Icon next to Apps
3. Select “Install App From File”
4. Click “Choose File” and select the downloaded file.
5. Click “Upload”
6. Click on “Restart Now”

## Configure Apps

## Setup Google App for Splunk
1. Open Google App for Splunk from the Apps Dropdown
2. Click “Continue to App Setup Page”
3. Follow Instructions to Get an API Key
4. Restart Splunk

### Setup Python for Scientific Computing with custom python libraries
**_Please keep in mind that this step will not survive future upgrades of this app. If you do update the Python for Scientific Computing app, you will need to repeat this step_**

1. Navigate to Python for Scientific Computing Python Home directory. For Mac this looks like:
```
cd $SPLUNK_HOME/etc/apps/Splunk_SA_Scientific_Python_darwin_x86_64/bin/darwin_x86_64/lib/python2.7
```

2. Install the following Python packages:

```
pip install html5lib pandas bs4 numpy --target=.

```

### Install Custom Splunk ML Algorithms

```<THIS NEEDS TO BE FILLED OUT WHEN RYAN GETS ACCESS TO SPLUNK GIT>>```
  
## Security

Security is the largest area of concern with this app. In order to help with security we have done a couple of things. 

1. This Splunk App will only request Read-Only Access to your Google Drive. The app cannot modify or delete anything in your Google Account.  
2. Splunk does not view any of your data, the only people that will be able to access your Google Drive data is anyone who has admin access to your Splunk instance once this app is setup. 
3. We specifically do not recommend setting this app up on a shared instance if you have any concerns about other admins seeing the content in the Google Account you authenticate with. 

Our current recommended setup would look like the following, where you would only authenticate this app to an account where you specifically share out the files you want to use in Splunk. This way the app does not have access to your entire Google Drive. 
![Alt text](/images/auth1.jpg?raw=true "Auth Option 1")

#### Revoking Access
If you need to revoke access to the Splunk App for any reason, you can do so by visiting the following Website. https://myaccount.google.com/permissions



