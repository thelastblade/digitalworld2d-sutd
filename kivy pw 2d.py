from libdw import pyrebase
from kivy.core.window import Window
Window.fullscreen = 0
Window.size = (1000,500)
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import time
from kivy.clock import Clock
import os
import glob
import numpy as np
from kivy.properties import NumericProperty

def get_pred_values(temp, time, first_temp):
 #these values for m and c are derived from the test set that was obtained
    m = 13.28829685
    c = 24.32411823
    a = db.child("Dataset/current_temp").get().val()
    grad_1 = []

    for i in range(len(a)):
        if i != 0:
            grad = (a[i][0]-a[0][0])/(a[i][1]-a[0][1])
        grad_1.append(grad)
        
    grad_avg = sum(grad_1)/len(grad_1)
    Tw = (m*grad_avg)+c
    return Tw

url = "https://pw-2d-49d42.firebaseio.com/"
apikey = "AIzaSyCFnhnjVqiR5uRAR9QQPTgBttnk8QgL190"

config={
    "apiKey":apikey,
    "databaseURL":url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()



class PW2D(App):
    time = NumericProperty(-5)
    countdown = NumericProperty(5)
    def build(self):
        
        self.Tw_values = []
        self.t_time_values = []
        self.temp_c = []
        self.root = root = GridLayout(rows=2,cols=4)
        self.mylabel =Label(text="Current Time:",font_size = 24,color=(1,1,1,1))
        self.mylabel2 = Label(text="Temperature Reading:", font_size = 24, color=(1,1,1,1))
        self.mylabel3 = Label(text="Prediction Time:", font_size = 24, color=(1,1,1,1))
        self.mylabel4 = Label(text="Predicted Temperature:", font_size = 24, color=(1,1,1,1))
       
        self.mylabela =Label(text="0 second",font_size = 24)
        
        self.mylabel2a = Label(text='', font_size = 24, color=(1,1,1,1))
        
        self.mylabel3a = Label(text="0 second", font_size = 24, color=(1,1,1,1))
        
        self.mylabel4a = Label(text="Predicting...", font_size = 24, color=(1,1,1,1))



        root.add_widget(self.mylabel)
        root.add_widget(self.mylabela)
        root.add_widget(self.mylabel3)
        root.add_widget(self.mylabel3a)
        root.add_widget(self.mylabel2)
        root.add_widget(self.mylabel2a)
        root.add_widget(self.mylabel4)
        root.add_widget(self.mylabel4a)
        
        
        Clock.schedule_interval(self.callback_temp, 0.5)
        Clock.schedule_interval(self.callback, 1)
        Clock.schedule_interval(self.pred_timer, 1)
        Clock.schedule_interval(self.callback_pred_temp, 0.5)

        return root
# starts the countdown and timer
    def callback(self, instance):
        self.time+=1
        if self.time >0:
            self.mylabela.text = (str(self.time) + " seconds")
        else:
            self.mylabela.text =("Countdown: "+ str(self.countdown))
        self.countdown -=1
#starts the pred timer and stops at 10sec
    def pred_timer(self,instance):
        if self.mylabel4a.text != "Predicting..." or self.mylabel3a.text =="10 seconds":
            self.mylabel3a.text ="10 seconds"
        else:
            self.mylabel3a.text = self.mylabela.text
#gets the current temp
    def callback_temp(self, instance):
        temp = db.child("Dataset/current_temp").get().val()
        self.mylabel2a.text = str(temp[-1][0])

#gets the pred temp
    def callback_pred_temp(self, instance):
        m = 12.83767982
        c = 24.57750592

        a = db.child("Dataset/current_temp").get().val()
        grad_1 = []

        for i in range(len(a)):
            if i != 0:
                grad = (a[i][0]-a[0][0])/(a[i][1]-a[0][1])
                grad_1.append(grad)


        grad_avg = sum(grad_1)/len(grad_1)

        Tw = (m*grad_avg)+c
        if self.mylabela.text != '7 seconds':
            self.mylabel4a.text = str(Tw)

        else:
            self.mylabel4a.text = 'Predicting...'

#        temp = read_temp()
#        t_time = round(time.time()+dt-start_time,3)
#        first_temp = self.temp_c[0] #find a way to append the temperatures obtained into a list
#        
#        Tw = get_pred_values(temp, t_time, first_temp)
#        self.Tw_values.append(Tw)
#        Tw_avg = sum(self.Tw_values)/len(self.Tw_values)

        
            



if __name__ == "__main__":
    PW2D().run()
