__version__ = '1.0'

import random
import kivy
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.clock import Clock

kivy.require('1.10.0') # replace with your current kivy version !


class TimeTracker():
    
    starting_point = time.time()
    color = None

    @classmethod
    def generate_starting_point(cls, new_color):
        TimeTracker.starting_point = time.time()
        TimeTracker.color = new_color

    @classmethod
    def get_reaction(cls, new_color):
        if TimeTracker.starting_point:
            if TimeTracker.color == tuple(new_color):
                reaction = time.time() - TimeTracker.starting_point
                TimeTracker.starting_point = None
            else:
                reaction = TimeTracker.color
            return reaction


class RandomColor():

    red = (0.9, 0, 0, 1)
    green = (0, 0.9, 0, 1)
    blue = (0, 0, 0.9, 1)
    yellow = (0.9, 0.9, 0, 1)
    colors = (red, green, blue, yellow)

    @classmethod
    def get(cls):
        return RandomColor.colors[random.randrange(len(RandomColor.colors))]


class ColorChangingButton(Button):

    def __init__(self, change_time=1):
        super(ColorChangingButton, self).__init__()
        self.change_time = change_time

    def change_color(self, delta_time):
        new_color = RandomColor.get()
        self.background_color = new_color
        TimeTracker.generate_starting_point(new_color)

    def start(self):
        Clock.schedule_interval(self.change_color, self.change_time)


class MyApp(App):

    def __init__(self):
        super(MyApp, self).__init__()
        self.touch_times = []
        self.misses = []

    def finish(self, instance):
        if not self.touch_times:
            text = 'No touches registered!'
        else:
            text = 'Average reaction time is {}'.format(sum(self.touch_times)/len(self.touch_times))
        if self.misses:
            text += '\nMismatched colors: '+ str(len(self.misses))
        content = Button(text=text)
        content.bind(on_press=App.get_running_app().stop)
        popup = Popup(title='Results', content=content)
        popup.open()

    def tap(self, instance):
        color = instance.background_color
        print ('Tap on color ' + str(color))
        reaction = TimeTracker.get_reaction(color)
        print('Reaction time: ' + str(reaction))
        if type(reaction) is float:
            self.touch_times.append(reaction)
        elif type(reaction) is tuple:
            self.misses.append(reaction)

    def create_color_button(self, color, callback=None, cls=Button):
        if callback is None:
            callback = self.tap
        btn = cls()
        btn.background_color = color
        btn.background_normal = ''
        btn.bind(on_press=callback)
        return btn

    def build(self):
        grid_layout = GridLayout(cols=2, size_hint_y=0.67)
        grid_layout.add_widget(self.create_color_button(RandomColor.red))
        grid_layout.add_widget(self.create_color_button(RandomColor.green))
        grid_layout.add_widget(self.create_color_button(RandomColor.blue))
        grid_layout.add_widget(self.create_color_button(RandomColor.yellow))
        everything = BoxLayout(orientation='vertical')
        bottom = self.create_color_button(color=(1, 1, 1, 1), cls=ColorChangingButton, callback=self.finish)
        bottom.size_hint_y = 0.33
        bottom.start()
        everything.add_widget(grid_layout)
        everything.add_widget(bottom)
        return everything


if __name__ == '__main__':
    MyApp().run()