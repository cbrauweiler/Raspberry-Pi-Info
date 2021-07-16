# -*- coding: utf-8 -*-

import os
import sys
import socket
import fcntl
import struct
import mysql.connector
import subprocess


# global vars
mysql_server = ''
mysql_port = '3306'
mysql_database = ''
mysql_user = ''
mysql_pass = ''

network_adapter = 'eth0'


# Install dependecies and mysql database structure
if(sys.argv[0] == 'install'):
    Cmd1 = ["sudo apt install python-pip python-pip3 -y"]
    process1 = subprocess.Popen(Cmd1, stdout=subprocess.PIPE)
    
    Cmd2 = ["sudo pip install mysql-connector-python-rf"]
    process2 = subprocess.Popen(Cmd2, stdout=subprocess.PIPE)
    
    #Cmd3 = ["mysql import data.sql"]
    #process3 = subprocess.Popen(Cmd3, stdout=subprocess.PIPE)
else:

    # Return System Info
    def getOS():
        res = str.strip(subprocess.check_output("/bin/cat /etc/os-release | grep ^PRETTY_NAME=", shell=True)).replace('"','').split("=")
        return(res[1])

    # Return Board revision
    def getBoard():
        res = str.strip(subprocess.check_output("/bin/cat /proc/cpuinfo | grep ^Revision", shell=True)).replace(' ','').split(":")
        return(res[1])

    # Return CPU clock as a character string
    def getCPUclock():
        res = os.popen('/bin/cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq').readline()
        return(res[:-4])

    # Return CPU temperature as a character string
    def getCPUtemperature():
        res = os.popen('/usr/bin/vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

    # Return CPU voltage as a character string
    def getCPUvoltage():
        res = os.popen('/usr/bin/vcgencmd measure_volts core').readline()
        res = res.replace("V","")
        return(res.replace("volt=",""))

    # Return RAM information (unit=kb) in a list
    # Index 0: total RAM
    # Index 1: used RAM
    # Index 2: free RAM
    def getRAMinfo():
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                return(line.split()[1:4])

    # Return % of CPU used by user as a character string
    def getCPUuse():
        return(str(os.popen("/usr/bin/top -b -n1 | /usr/bin/awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
    )).replace(",","."))
        

    # Return information about disk space as a list (unit included)
    # Index 0: total disk space
    # Index 1: used disk space
    # Index 2: remaining disk space
    # Index 3: percentage of disk used
    def getDiskSpace():
        p = os.popen("/bin/df -h /")
        i = 0
        while 1:
            i = i +1
            line = p.readline()
            if i==2:
                return(line.split()[1:5])
                

    # Return IP from network adapter
    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
                
                

    # OS information
    OS = getOS()

    # CPU informatiom
    Board = getBoard()
    CPU_clock = getCPUclock()
    CPU_temp = getCPUtemperature()
    CPU_voltage = getCPUvoltage()
    CPU_usage = getCPUuse()

    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)

    # Disk information
    DISK_stats = getDiskSpace()
    DISK_total = DISK_stats[0].replace("G","")
    DISK_used = DISK_stats[1].replace("G","")
    DISK_perc = DISK_stats[3].replace("%","")

    # Hostname and IP from eth0
    hostname = (socket.gethostname())
    ipaddress = get_ip_address('eth0')


    # Insert data into mysql db
    from mysql.connector import Error
    from mysql.connector import errorcode
    from datetime import datetime
    def insertPythonVaribleInTable(hostname, ipaddress, os, board, cpu_clock, cpu_temp, cpu_usage, cpu_voltage, ram_total, ram_usage, ram_free, disk_total, disk_usage, disk_perc):
        try:
            connection = mysql.connector.connect(host=mysql_server,
                                 port=mysql_port,
                                 database=mysql_database,
                                 user=mysql_user,
                                 password=mysql_pass)
            cursor = connection.cursor(prepared=True)
            sql_insert_query = """ INSERT INTO `data`
                              (`hostname`, `ipaddress`, `os`, `board`, `cpu_clock`, `cpu_temp`, `cpu_usage`, `cpu_voltage`, `ram_total`, `ram_usage`, `ram_free`, `disk_total`, `disk_usage`, `disk_perc`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            insert_tuple = (hostname, ipaddress, os, board, cpu_clock, cpu_temp, cpu_usage, cpu_voltage, ram_total, ram_usage, ram_free, disk_total, disk_usage, disk_perc)
            result  = cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
            print ("Record inserted successfully into data table")
        except mysql.connector.Error as error :
            connection.rollback()
            print("Failed to insert into MySQL table {}".format(error))
        finally:
            #closing database connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    insertPythonVaribleInTable(hostname, ipaddress, OS, Board, CPU_clock, CPU_temp, CPU_usage, CPU_voltage, RAM_total, RAM_used, RAM_free, DISK_total, DISK_used, DISK_perc)