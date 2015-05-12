import base64
import pyaudio
import numpy
import time
import random
import zmq

WIDTH = 2
CHANNELS = 2
RATE = 44100

port = 8888
sync_port = 8889
topic = "ben-laptop"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
sync_socket = context.socket(zmq.PUB)
sync_socket.bind("tcp://*:%s" % sync_port)
counter = 0



p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    rand = random.Random()
    timestamp = time.time()+.5
    if rand.randint(0,300) == 0:
      sync_socket.send("%s|||||sync"%timestamp)
    socket.send("%s|||||%s"%(timestamp,in_data))
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()


