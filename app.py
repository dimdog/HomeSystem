import struct
import serial

from flask import Flask, Response, render_template, request

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=.5)
except:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=.5)
power_state = True

app = Flask(__name__)

strip_length = 25


def int_to_bin(value):
    return struct.pack('I', value)


def write_to_strip(red, green, blue, position=None):
    if position == -1 or position >= strip_length:
        position = None
    if position:
        ser.write(int_to_bin(401))
        ser.write(int_to_bin(position))
    ser.write(int_to_bin(red))
    ser.write(int_to_bin(green))
    ser.write(int_to_bin(blue))
    ser.write(int_to_bin(400))


@app.route('/color')
def api_data():
    red = int(request.args.get('red'))
    green = int(request.args.get('green'))
    blue = int(request.args.get('blue'))
    position = int(request.args.get('position', -1))

    try:
        write_to_strip(red, green, blue, position)
    except Exception as e:
        print e
    return Response()


@app.route('/power')
def power():
    for led in xrange(strip_length):
        write_to_strip(0, 0, 0, led)
    return Response()


@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
