from libdw import pyrebase
import os
import glob
import datetime

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'

url = "https://pw-2d-49d42.firebaseio.com/"
apikey = "AIzaSyCFnhnjVqiR5uRAR9QQPTgBttnk8QgL190"

config={
    "apiKey":apikey,
    "databaseURL":url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class StopWatch:
    def __init__(self, start_time = time.time(), end_time = -1):
        self.start_time = start_time
        self.end_time = end_time
        
    def start(self):
        self.start_time = time.time()
        
    def elapsed_time(self):
        x = time.time()
        y = self.start_time
        return round((x - y),3) #return time elapsed in seconds, to 3 dp
    
def update_firebase(variable, new_state):
    states = dict(db.child("Dataset").get().val())
    states[variable] = new_state
    db.child("Dataset").set(states)

sw = StopWatch()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
   lines = read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':
       time.sleep(0.2)
       lines = read_temp_raw()
   equals_pos = lines[1].find('t=')
   if equals_pos != -1:
        temp_string = lines[1][equals_pos +2:]
        temp_c = float(temp_string)/ 1000.0
        
        return temp_c
    
    
def start_predict():
    sw.start
    ls = []
    while True:
        temp_c = read_temp()
        ls.append(temp_c)
        update_firebase('time', sw.elapsed_time())
        update_firebase('current_temp', ls)
    
start_predict()
    
    
    
    
    
    
    
    
    
    
    
    
    