import json, os, shutil
import tools.fontcolor as fontcolor
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition, FadeTransition
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
import requests
from pathlib import Path
from kivy.core.window import Window
from kivy.config import Config
import time
#from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.screenmanager import(
    CardTransition
)
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from threading import Thread

from screens.questions.questions import Question

import os
from local_settings import *
print(os.system('pip show kivymd'))

if platform == 'android':
    domain = prod_domain 
    url = prod_url

else:
    domain = dev_domain 
    url = dev_url
    Window.size = (350, 700)
    Window.top = 80
    Window.right = 80

class MD3Card(MDCard):

    id = NumericProperty()
    text = StringProperty()
    image = StringProperty()

    def get_questions(self):
        Question.title = self.text
        print(self.text)
        Question.id = self.id
        MDApp.get_running_app().sm.current = 'questions'
        MDApp.get_running_app().sm.transition.direction = 'left'

        #if not sm.has_screen(name='list_questions'):

class Menu(Screen):
    
    result = ObjectProperty()
    kak = StringProperty()
    subjects = ObjectProperty()
    fuck = ObjectProperty()
    load_pics = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Menu ___init__')

        if os.path.exists('storage/data.json'):
            print('<<< onep data_json file >>>>')

            with open('storage/data.json') as f:
                self.result = json.load(f)
                for x in self.result:
                    card = MD3Card(
                        #id=x.get('id'), text=x.get('name'), image=domain + x.get('image')
                        id=x.get('id'), text=x.get('name'), image=x.get('image')
                    )
                    self.ids.box.add_widget(card)
        else:
            print('<<< UrlRequest is working >>>>')
            self.loading = MDLabel(text='loading', halign='center')
            self.add_widget(self.loading)

            self.req = UrlRequest(url + '/app/subjects/',
                on_success=self.success,
                on_failure=self.fail, 
                on_error=self.error,
                on_progress=self.progress,
            )

        self.config = App.get_running_app().config
        self.lang = self.config.get('Settings', 'lang')
        self.answer = self.config.get('Settings', 'answer')
        Question.params = {'lang': self.lang, 'answer': self.answer}

    def success(self, req, result):
        self.result = result
        for x in self.result:
            card = MD3Card(
                id=x.get('id'), text=x.get('name'), image=domain + x.get('image')
            )
            self.ids.box.add_widget(card)
        self.remove_widget(self.loading)
        
        if not os.path.exists('storage'):
            os.mkdir('storage')

        th = Thread(target=self.get_pictures).start()

    def fail(self, req, result):
        self.add_widget(MDLabel(text='fail', halign='center'))
        print('fail')

    def error(self, req, result):
        self.add_widget(MDLabel(text='error', halign='center'))
        print('error')

    def progress(self, *args, **kwargs):
        print('loading....')
    
    def get_pictures(self):
        if not os.path.exists('i/levels'):
            os.mkdir('i/levels')

        for x in self.result:
            url_ = domain + x.get('image')
            name = os.path.basename(url_).split('/')[-1]
            print('You got --->', name.capitalize())
            r = requests.get(url_, stream=True)
            f = open('i/levels/' + name, 'wb')
            f.write(r.content)

        for x in self.result:
                name = os.path.basename(x['image']).split('/')[-1]
                x['image'] = 'i/levels/' + name
        with open('storage/data.json', 'w') as f:
            json.dump(self.result, f)

    def on_enter(self, *args):
        print('self.lang >> ', self.lang)
        self.ids.lang.text = self.lang[:2].capitalize()

        # Create  list_questions screen if it doesn't exists
        if not MDApp.get_running_app().sm.has_screen(name='questions'):
            print('creating Question screen ...')
            Builder.load_file('screens/questions/questions.kv')
            MDApp.get_running_app().sm.add_widget(Question(name='questions'))

    def switch_lang(self, instance):
        print(instance == 'En')
        if instance == 'En':
            self.lang = 'ru_lang'
            self.ids.lang.text = 'Ru'
            self.config.set('Settings', 'lang', 'ru_lang')
            self.config.set('Settings', 'answer', 'ru_answer')
            Question.params = {'lang': 'ru_lang', 'answer': 'ru_answer'}
        else:
            self.ids.lang.text = 'En'
            self.lang = 'en_lang'
            self.config.set('Settings', 'lang', 'en_lang')
            self.config.set('Settings', 'answer', 'en_answer')
            Question.params = {'lang': 'en_lang', 'answer': 'en_answer'}
        self.config.write()


#sm = ScreenManager()

class App(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = 'BlueGray'  #"Gray"
        self.theme_cls.primary_hue = "300"
        #self.window_manager = WindoManager(transition=FadeTransition(duration=1))

        Builder.load_file('index.kv')
        #Builder.load_file('screens/questions/questions.kv')
        #Builder.load_file('screens/detail/detail.kv')

        #self.sm = sm
        self.sm = ScreenManager()
        self.sm.add_widget(Menu(name='menu'))
        #self.sm.add_widget(Question(name='questions'))
        #self.sm.add_widget(Detail(name='detail'))
        return self.sm

    def build_config(self, config):
        self.config.setdefaults(
            'Settings', {
                'lang': 'en_lang',
                'answer': 'en_answer',
            }
        )

if __name__ == '__main__':
    
    App().run()
