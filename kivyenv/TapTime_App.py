from kivy.app import App
from kivy.properties import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFabButton
import requests
import datetime

# Server API URL
API_URL = "http://localhost:5000/clock"

# Custom image for next button

class ImageButton(ButtonBehavior, Image):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        return super().on_touch_down(touch)

def set_background(screen):
    with screen.canvas.before:
        from kivy.graphics import Rectangle
        screen.rect= Rectangle(
            source="C:/Users/AhmadN/OneDrive/Desktop/TapTime/bg1.jpg",
            size=(1920,1080),
            pos=(screen.width / 2- 1920, screen.height / 2 - 1080)
        )
    screen.bind(size=screen.update_rect, pos=screen.update_rect)

# Intro Screen
class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        set_background(self)

        self.bind(size=self.update_rect, pos=self.update_rect)

        float_layout = FloatLayout()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        image = Image(source="C:/Users/AhmadN/OneDrive/Desktop/TapTime/logo.png",
        size_hint=(None,None),
        width=300,
        height=500,
        pos_hint={"center_x": 0.5, "center_y": 0.7}
    )
        float_layout.add_widget(image)

        # Welcome Text
        welcome_label = Label(
            text="Welcome to TapTime \n Tap Next to Clock In & Out \n Developed by Ahmad Noori \n Version 1.0",
            halign="center",
            valign="middle",
            font_size=25,
            color=get_color_from_hex("#020202"),
            font_name=r"C:\Users\AhmadN\AppData\Local\Microsoft\Windows\Fonts\NexaExtraLight.ttf",
            size_hint=(None, None),
            width=50,
            height=50,
            pos_hint={"center_x": 0.5, "y": 0.35},
        )
        welcome_label.bind(size=welcome_label.setter("text_size"))
        float_layout.add_widget(welcome_label)
        self.add_widget(float_layout)


        # Next Button to go to ClockInScreen
        next_button = ImageButton(
            source="C:/Users/AhmadN/OneDrive/Desktop/TapTime/bluenext.png",
            size_hint=(2, None),
            width=200, # Ahmad keep changing this
            height=300,
            pos_hint={"center_x": 0.5, "y": 0}
        )

        next_button.bind(on_press=self.go_to_clock_in)
        float_layout.add_widget(next_button)
        self.add_widget(layout)

    def update_text(self, new_text):
        self.welcome_label.text = new_text

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def go_to_clock_in(self, instance):
        self.manager.current = "clock_in"

    def go_to_clock_in(self, instance):
        self.manager.current = "clock_in"

# Clock In Screen
class ClockInScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        set_background(self)

        layout = FloatLayout()

        # Title
        layout.add_widget(Label(
            text="Clock In / Clock Out",
            font_size=30,
            color=get_color_from_hex("#020202"),
            font_name =r"C:\Users\AhmadN\AppData\Local\Microsoft\Windows\Fonts\NexaHeavy.ttf",
            size_hint_y=(1, None),
            height=20,
            pos_hint={"center_x": 0.5, "y": 0.9}
        ))

        self.name_input = TextInput(
            hint_text="Enter your name",
            multiline=False,
            font_size=24,
            size_hint=(None, None),
            width=300,
            height=50,
            pos_hint={"center_y": 0.8, "center_x": 0.5}
        )
        layout.add_widget(self.name_input)

        button_width = 300
        button_height = 290

        # Clock In Button
        clock_in_button = ImageButton(
            source="C:/Users/AhmadN/OneDrive/Desktop/TapTime/clockin.png",
            size_hint=(None, None),
            width=button_width,
            height=button_height,
            pos_hint={"center_y": 0.6, "center_x": 0.5}
        )

        clock_in_button.bind(on_press=lambda x: self.send_attendance("Clock In"))
        layout.add_widget(clock_in_button)

        # Clock Out Button
        clock_out_button = ImageButton(
            source="C:/Users/AhmadN/OneDrive/Desktop/TapTime/clockout.png",
            size_hint=(None, None),
            width=button_width,
            height=button_height,
            pos_hint={"center_y": 0.4, "center_x": 0.5}
        )

        clock_out_button.bind(on_press=lambda x: self.send_attendance("Clock Out"))
        layout.add_widget(clock_out_button)

        # Back to Welcome Screen
        back_button = ImageButton(
            source="C:/Users/AhmadN/OneDrive/Desktop/TapTime/back.png",
            size_hint=(None, None),
            width=button_width,
            height=button_height,
            pos_hint={"center_y": 0.2, "center_x": 0.5}
        )

        back_button.bind(on_press=self.go_to_intro)
        layout.add_widget(back_button)

        self.status_label = Label(text="")
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def go_to_clock_in(self,instance):
        self.manager.current = "clock_in"

    def go_to_intro(self, instance):
        self.manager.current = "intro"

        # Function to send clock-in/clock-out request

    def send_attendance(self, action):
        name = self.name_input.text.strip()

        if not name:
            self.status_label.text = "Please enter your name!"
            self.status_label.color = (1, 0.6, 0, 1)
            self.status_label.font_size = 30
            self.status_label.font_name = r"C:\Users\AhmadN\AppData\Local\Microsoft\Windows\Fonts\NexaHeavy.ttf"
            self.status_label.pos_hint={"center_y": 0.1, "center_x": 0.5}
            return

        clock_time = datetime.datetime.now().strftime('%I:%M %p')

        data = {
            "name": name,
            "action": action,
            "time": clock_time
        }

        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                self.status_label.text = f"{action} successful at {datetime.datetime.now().strftime('%I:%M %p')}"
                self.status_label.color = (0,0.5, 0, 1)
                self.status_label.font_size = 30
                self.status_label.font_name = r"C:\Users\AhmadN\AppData\Local\Microsoft\Windows\Fonts\NexaHeavy.ttf"
            else:
                self.status_label.text = "Failed to send attendance!"
                self.status_label.color = (1, 0, 0, 1)
                self.status_label.font_size = 30
                self.status_label.font_name = r"C:\Users\AhmadN\AppData\Local\Microsoft\Windows\Fonts\NexaHeavy.ttf"
        except requests.exceptions.RequestException:
            self.status_label.text = "Error connecting to server!"
            self.status_label.color = (1, 0, 0, 1)
            self.status_label.font_size = 30
            self.status_label.font_name = r"C:\Users\AhmadN\AppData\Local\Microsoft\Windows\Fonts\NexaHeavy.ttf"

# Main App
class Tap_Time(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=0.1))
        sm.add_widget(IntroScreen(name="intro"))
        sm.add_widget(ClockInScreen(name="clock_in"))
        return sm

if __name__ == "__main__":
    Tap_Time().run()
