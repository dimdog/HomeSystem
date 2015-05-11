from datetime import datetime
import pyaudio
import sched
import time
import zmq

WIDTH = 2
CHANNELS = 2
RATE = 44100

format_string = "%H:%M:%S %f"
trim = -4

port = 8888
topic = "ben-laptop"
context = zmq.Context()
socket = context.socket(zmq.SUB)
s = sched.scheduler(time.time, time.sleep)

print "collecting audio data!"
socket.connect ("tcp://localhost:%s" % port)

def parse_data_stream(data):
  return data.split("|||")
  #return 0, data

def writing_data(stream, data):
  print "writing data..."
  stream.write(data)

def schedule_event(scheduler, stream, time, data):
  scheduler.enterabs(time,1,writing_data,(stream.write,data)) 

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output_device_index = 1,                
                output=True)

stream.start_stream()

# read data
topicfilter = ""
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)


ts, data =  parse_data_stream(socket.recv())
schedule_event(s,stream,ts,data)



# play stream (3)
while True:
  ts, data =  parse_data_stream(socket.recv())
  schedule_event(s,stream,ts,data)

stream.stop_stream()
stream.close()

p.terminate()



