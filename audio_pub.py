import pyaudio
import numpy
import time
import zmq

WIDTH = 2
CHANNELS = 2
RATE = 44100

port = 8888
topic = "ben-laptop"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)



p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    print "sending:|%s|"%in_data
    socket.send("%s %s"%(topic, in_data))
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


