import kivy
from kivy.app import App
from kivy.uix.label import Label
class Window(kivy.App):
    def build(self):
        return Label(text="Hello world")

win =Window()
win.run()