import os
import struct
import serial
import time
import ConfigParser

from flask import Flask, Response, render_template, request

   
ser = serial.Serial('COM3', 9600,timeout=.5)
power_state=True

app = Flask(__name__)

def int_to_bin(value):
  return struct.pack('I', value)

def write_to_strip(red,green,blue):
  
  ser.write(int_to_bin(red))
  ser.write(int_to_bin(green))
  ser.write(int_to_bin(blue))
  ser.write(int_to_bin(400))


@app.route('/color')
def api_data():
  red = int(request.args.get('red'))
  green = int(request.args.get('green'))
  blue = int(request.args.get('blue'))


  try:
    write_to_strip(red,green,blue)
    
  except Exception as e:
    print e
  return Response()

@app.route('/power')
def power():
  ser.close()
  print "closed"
  ser.open()
  print "open"
  return Response()





@app.route('/')
def root(): 
  return render_template('index.html')
    
print "here"

write_to_strip(125,0,0)
time.sleep(1)
write_to_strip(125,0,0)


if __name__ == '__main__':
  app.run(port=80,host='0.0.0.0')



