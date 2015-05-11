import base64
import pyaudio
import numpy
import time
import zmq
from datetime import datetime, timedelta

WIDTH = 2
CHANNELS = 2
RATE = 44100

port = 8888
topic = "ben-laptop"

format_string = "%H:%M:%S %f"
dt = timedelta(seconds=1)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
ANDSUB=False



p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    timestamp = int(time.time())+60
    socket.send("%s|||%s"%(timestamp,in_data))
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                output=ANDSUB,
                output_device_index=1,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()


