# Raspberry Pi Info
Python script to collect data from one or more Raspberry Pi and write it into a mySQL table. The data can then be displayed with, for example, Grafana.

![alt Grafana Dashboard](https://github.com/cbrauweiler/raspberrypi_info/blob/5e1ec055e0c3b96e4174510a828d3da5a1533da7/Grafana_Dashboard_Example.png)

# Usage
1. Create a mySQL database
2. Import the table "data.sql"

The following steps must be carried out on each Raspberry from which data is to be collected.

3. Save the Python script "RPi-Info.py" on the Raspberry (for example under /home/pi)
4. Edit the Python script:
    - Select correct network adapter in line 107 (eth0, wlan0 etc.)
    - Enter correct connection data to the database in lines 116 to 120
5. sudo apt install python-pip python3-pip
6. sudo pip install mysql-connector-python-rf
7. Create cron job with "sudo crontab -e"
    (example: */5 * * * * python /home/pi/RPi-Info.py
