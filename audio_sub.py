import time
import pyaudio
import Queue
import zmq
from functools import partial


WIDTH = 2
CHANNELS = 2
RATE = 44100
port = 8888
sync_port = 8889

context = zmq.Context()
socket = context.socket(zmq.SUB)
sync_socket = context.socket(zmq.SUB)
q = Queue.Queue()

print "collecting audio data!"
socket.connect ("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, "")

sync_socket.connect ("tcp://localhost:%s" % sync_port)
sync_socket.setsockopt(zmq.SUBSCRIBE, "")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
poller.register(sync_socket, zmq.POLLIN)

p = pyaudio.PyAudio()

def callback(*args, **kwargs):
  msg = q.get()
  if msg =="":
    return
  ts,data = msg.split("|||||") 
  if data=="sync":
    print "SYNCED"
    new_ts = 0
    while float(ts) >= float(new_ts):
      new_ts,data = q.get().split("|||||")

  return (data, pyaudio.paContinue)


stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output_device_index = 1,                
                output=True,
                stream_callback=callback)


stream.start_stream()



#read data
while True:
  try:
    socks = dict(poller.poll())
  except KeyboardInterrupt:
    break
  if socket in socks:
    try:
      q.put(socket.recv())
    except:
      pass
  if sync_socket in socks:
    try:
      q.put(sync_socket.recv())
    except:
      pass
  

stream.stop_stream()
stream.close()

p.terminate()
