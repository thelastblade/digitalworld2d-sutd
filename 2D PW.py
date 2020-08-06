from kivy.core.window import Window
Window.fullscreen = 0
Window.size = (1000,500)
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import time
from kivy.clock import Clock
from kivy.properties import NumericProperty


    

class PW2D(App):
    time = NumericProperty(-10)
    countdown = NumericProperty(10)
    def build(self):
        self.root = root = GridLayout(rows=2,cols=4)
        self.mylabel =Label(text="Current Time:",font_size = 12,color=(1,1,1,1))
        self.mylabel2 = Label(text="Temperature Reading:", font_size = 12, color=(1,1,1,1))
        self.mylabel3 = Label(text="Prediction Time:", font_size = 12, color=(1,1,1,1))
        self.mylabel4 = Label(text="Predicted Temperature:", font_size = 12, color=(1,1,1,1))
        self.mylabela = Label(text = "0 second",font_size = 12)
        self.mylabel2a = Label(text = "3"+ " degrees", font_size = 12, color=(1,1,1,1))
        self.mylabel3a = Label(text = "0 second", font_size = 12, color=(1,1,1,1))
        self.mylabel4a = Label(text = "Predicting...", font_size = 12, color=(1,1,1,1))
        
        
        root.add_widget(self.mylabel)
        root.add_widget(self.mylabela)
        root.add_widget(self.mylabel3)
        root.add_widget(self.mylabel3a)
        root.add_widget(self.mylabel2)
        root.add_widget(self.mylabel2a)
        root.add_widget(self.mylabel4)
        root.add_widget(self.mylabel4a)

        Clock.schedule_interval(self.callback, 1)
        Clock.schedule_interval(self.pred_timer, 1)
        

        return root
    def callback(self, instance):
        self.time+=1
        if self.time >0:
            self.mylabela.text = (str(self.time) + " seconds")
        else:
            self.mylabela.text =("Countdown: "+ str(self.countdown))
        self.countdown -=1
    def pred_timer(self,instance):
        if self.mylabel4a.text == "Predicting...":
            self.mylabel3a.text = self.mylabela.text
        else:
            a = self.mylabel3a.text
            self.mylabel3a.text =a

            

        



if __name__ == "__main__":
    PW2D().run()