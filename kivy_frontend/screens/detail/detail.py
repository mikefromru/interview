from kivymd.app import MDApp
import requests
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty

domain = 'http://iammike.pythonanywhere.com/'
url = 'http://iammike.pythonanywhere.com/api'

class Detail(Screen):

    params = ObjectProperty()
    title = StringProperty()
    body = StringProperty()

    def on_enter(self):
        lang = self.params.get('lang') 
        answer = self.params.get('answer')

        r = requests.get(url + f'/app/subject/question/detail/{self.data.get("id")}/')
        data = r.json()

        self.title = data.get(lang)
        self.body = data.get(answer)

        self.ids.title.ids.label_title.font_size = '15sp'

    def go_back(self):
        self.title, self.body = '', ''
        MDApp.get_running_app().sm.current = 'questions'
        MDApp.get_running_app().sm.transition.direction = 'right'
