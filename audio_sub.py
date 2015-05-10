import time
import pyaudio
import zmq

WIDTH = 2
CHANNELS = 2
RATE = 44100

port = 8888
topic = "ben-laptop"
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "collecting audio data!"
socket.connect ("tcp://10.0.1.8:%s" % port)

p = pyaudio.PyAudio()

p.

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output_device_index = 1,                
                output=True)

stream.start_stream()

# read data
topicfilter = ""
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
data =  socket.recv()

# play stream (3)
while data != '':
    stream.write(data)
    data =  socket.recv()

stream.stop_stream()
stream.close()

p.terminate()
