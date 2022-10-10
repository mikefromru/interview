from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
import requests
from pathlib import Path

from kivy.uix.screenmanager import(
    CardTransition
)

domain = 'http://localhost:8000'
url = 'http://localhost:8000/api'


#domain = 'http://192.168.0.13:8000'
#url = 'http://192.168.0.13:8000/api'

class WindoManager(ScreenManager):
    pass

class Detail(Screen):

    data = ObjectProperty()

    def on_enter(self):
        self.ids.title.title = self.data['title'][2:]
        # change titl size in MDToolbar
        self.ids.title.ids.label_title.font_size = '14sp'
        body = self.data['body']
        
        self.ids.body.text = body
 
    def go_back(self):
        self.manager.current = 'list_questions'
        App.get_running_app().window_manager.transition.direction = 'right'

class ListItem(OneLineListItem):

    text = StringProperty()
    body = StringProperty()

    def on_release(self):
        Detail.data = {'title': self.text, 'body': self.body}
        App.get_running_app().window_manager.current = 'detail'


class Question(Screen):

    params = ObjectProperty()
    id = NumericProperty()
    page_id = NumericProperty(1)
    count = NumericProperty()
    next_ = True

    def on_enter(self):
        self.get_questions()

    def get_questions(self):
        #"next": "http://localhost:8000/api/app/subject/1/?page=2"
        r = requests.get(url + f'/app/subject/{self.id}/?page={self.page_id}', params=self.params)
        data_json = r.json()
        if self.next_ == True:
            self.create_card(data_json)

        if data_json['next'] == None:
                self.next_ = False

    def create_card(self, data):
        j = 1
        for x in data.get('results'):
            self.ids.box.add_widget(
                ListItem(body=x.get(self.params['answer']), text=str(j) + '. ' +  str(x.get(self.params['lang'])))
            )
            j += 1

    def next(self):
        if self.next_ == True:
            self.page_id += 1
            self.ids.box.clear_widgets() 
            self.get_questions()

    def prev(self):
        self.next_ = True
        if self.page_id > 1:
            self.page_id -= 1
            self.ids.box.clear_widgets() 
            self.get_questions()

    def on_leave(self):
        self.ids.box.clear_widgets()
        self.next_ = True

    def callback(self):
        self.page_id = 1
        self.manager.current = 'menu'
        App.get_running_app().window_manager.transition.direction = 'right'

class MD3Card(MDCard):
    id = NumericProperty()
    text = StringProperty()
    image = StringProperty()

    def get_questions(self):
        Question.id = self.id
        App.get_running_app().window_manager.current = 'list_questions'
        App.get_running_app().window_manager.transition.direction = 'left'

class Menu(Screen):

    subjects = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.create_card, 0.2)
        self.config = App.get_running_app().config
        self.lang = self.config.get('Settings', 'lang')
        self.answer = self.config.get('Settings', 'answer')
        Question.params = {'lang': self.lang, 'answer': self.answer}

    def switch_lang(self, instance):
        if instance == 'En':
            self.ids.lang.text = 'Ru'
            self.config.set('Settings', 'lang', 'ru_lang')
            self.config.set('Settings', 'answer', 'ru_answer')
            Question.params = {'lang': 'ru_lang', 'answer': 'ru_answer'}
        else:
            self.ids.lang.text = 'En'
            self.config.set('Settings', 'lang', 'en_lang')
            self.config.set('Settings', 'answer', 'en_answer')
            Question.params = {'lang': 'en_lang', 'answer': 'en_answer'}
        self.config.write()

        
        #print(lang_)

    def create_card(self, i):
        self.ids.lang.text = self.lang[:2].capitalize()
        for x in self.subjects:
            card = MD3Card(
                id=x.get('id'), text=x.get('name'), image=domain + x.get('image')
            )
            self.ids.box.add_widget(card)


class App(MDApp):

    def build(self):
        Builder.load_file('index.kv')
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        #App.get_running_app().theme_cls.primary_pallete = 'Teal'
        #self.window_manager = WindoManager(transition=CardTransition(duration=0.05))
        self.window_manager = WindoManager()
        return self.window_manager

    def on_start(self, **kwargs):
        r = requests.get(url + '/app/subjects')
        Menu.subjects = r.json()

    def build_config(self, config):
        self.config.setdefaults(
            'Settings', {
                'lang': 'en_lang',
                'answer': 'en_answer',
            }
        )
        

if __name__ == '__main__':
    App().run()
