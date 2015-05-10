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
socket.connect ("tcp://localhost:%s" % port)

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    print "callback!"
    in_data = socket.recv() 
    print "received:|%s|"%in_data
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output_device_index = 1,                
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.001)

stream.stop_stream()
stream.close()

p.terminate()
