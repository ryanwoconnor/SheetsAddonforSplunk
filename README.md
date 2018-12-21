
# Google App for Splunk Setup Instructions

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

![Alt text](/images/auth1.jpg?raw=true "Auth Option 1")

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

<THIS NEEDS TO BE FILLED OUT WHEN RYAN GETS ACCESS TO SPLUNK GIT>>



