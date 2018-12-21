



## Install Google App for Splunk
1. Install Splunk
2. Clone GoogleDriveAddonforSplunk into /opt/splunk/etc/apps
3. Start Splunk
4. Login to Splunk

## Setup Google App for Splunk
1. Open Google App for Splunk from the Apps Dropdown
2. Click “Continue to App Setup Page”
3. Follow Instructions to Get an API Key
4. Restart Splunk


## Install Python for Scientific Computing
1. Download the appropriate Python for Scientific Computing app off of Splunkbase. For Mac, this app is https://splunkbase.splunk.com/app/2881/
2. From the Splunk Homepage click on the Gear Icon next to Apps
3. Select “Install App From File”
4. Click “Choose File” and select “Python for Scientific Computing”
5. Click “Upload”
6. Click on “Restart Now”


## Install Custom Splunk ML Algorithms

<THIS NEEDS TO BE FILLED OUT WHEN RYAN GETS ACCESS TO SPLUNK GIT>>

## Install new python libraries

1. Navigate to Python for Scientific Computing Python Home directory. For Mac this looks like:
```
cd $SPLUNK_HOME/etc/apps/Splunk_SA_Scientific_Python_darwin_x86_64/bin/darwin_x86_64/lib
```

2. Install the following packages:

```
pip install html5lib --target=.
pip install pandas --target=.
pip install bs4 --target=.
```
