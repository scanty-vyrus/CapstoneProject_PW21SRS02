#!/usr/bin/python           # This is server.py file
import socket
import os
import webbrowser
import json
import sqlite3
conn = sqlite3.connect('new.db')
cur = conn.cursor()

s = socket.socket()  # Create a socket object
# host = socket.gethostname() # Get local machine name
host = '192.168.1.34'  # go to cmd and type ipconfig get host from there
port = 12345 #Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)
print('host is lisening at ', host, port)  # Now wait for client connection.
while True:
    print('hi im loop')
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    print(addr)
    msg = c.recv(1024)
    #print(msg)
    if msg == b'decrpyt':
        cur.execute('select * from ip_data where ip = "{}"'.format(addr[0]))
        print(cur.fetchall())
    else:
        webbrowser.open_new("http://127.0.0.1:5000/")
        #print(msg.decode('utf-8'))
        msg = json.loads(msg)
        print(msg)
        day = msg["Day"]
        CaloriesBurned = msg["CaloriesBurned"]
        steps = msg["Steps"]
        distance = msg["Distance"]
        heartbeat = msg["HeartRate"]
        TotalMinutesAsleep = msg["TotalMinutesAsleep"]
        TotalTimeinBed = msg["TotalTimeInBed"]
        print(msg["CaloriesBurned"],CaloriesBurned)
        os.system('python login.py {} {} {} {} {} {} {} {}'.format(day,CaloriesBurned,steps,distance,heartbeat,TotalMinutesAsleep,TotalTimeinBed,addr[0]))
    c.send(b'Thank you for connecting')
    c.close()  # Close the connection