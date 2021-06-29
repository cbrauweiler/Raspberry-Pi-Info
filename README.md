# Raspberrypi Info
Python script to collect data from a Raspberry Pi and write it into a mySQL table. The data can then be displayed with, for example, Grafana.

# Usage
1. Create a mySQL database
2. Import the table "data.sql"

The following steps must be carried out on each Raspberry from which data is to be collected.

4. Save the Python script "RPi-Info.py" on the Raspberry (for example under / home / pi)
5. Edit the Python script:
    - Select correct network adapter in line 107 (eth0, wlan0 etc.)
    - Enter correct connection data to the database in lines 116 to 120
6. sudo apt install python-pip python3-pip
7. sudo pip install mysql-connector-python-rf
8. Create cron job with "sudo crontab -e"
    (example: * / 5 * * * * python /home/pi/RPi-Info.py
