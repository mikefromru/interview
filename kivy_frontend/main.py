from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition, FadeTransition
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
import requests
from pathlib import Path
from kivy.core.window import Window
from kivy.config import Config
import time

from kivy.uix.screenmanager import(
    CardTransition
)

from kivy.utils import platform

if platform == 'android':
    domain = 'http://iammike.pythonanywhere.com/'
    url = 'http://iammike.pythonanywhere.com/api'
else:
    domain = 'http://localhost:8000'
    url = 'http://localhost:8000/api'

    Window.size = (350, 700)
    Window.top = 80
    Window.right = 80

class WindoManager(ScreenManager):
    pass

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
        self.manager.current = 'list_questions'
        App.get_running_app().window_manager.transition.direction = 'right'

class ListItem(OneLineListItem):

    id = NumericProperty()
    text = StringProperty()
    body = StringProperty()
    params = ObjectProperty()

    def on_release(self):
        Detail.data = {'id': self.id, 'title': self.text, 'body': self.body}
        print(self.id)
        App.get_running_app().window_manager.current = 'detail'

class Question(Screen):
    
    title = StringProperty()
    params = ObjectProperty()
    id = NumericProperty()
    total = NumericProperty(0)
    page_id = NumericProperty(1)
    count = NumericProperty()
    next_ = True
    load = True

    def __init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def checking_load(self, i):
        self.get_questions()
        if self.load:
            print('loading ...')
        else:
            self.event_load.cancel()
            self.remove_widget(self.loading)
            print('done')

    def on_enter(self, *args):
        self.ids.mytitle.title = self.title.capitalize()
        self.event_load = Clock.schedule_interval(self.checking_load, 0.1)
        self.loading = MDLabel(text='Loading ...', halign='center')
        self.add_widget(self.loading)
        Detail.params = self.params

    def on_leave(self, *args):
        self.event_load.cancel()
        self.remove_widget(self.loading)
        self.title = ''

    def get_questions(self):
        r = requests.get(url + f'/app/subject/{self.id}/?page={self.page_id}', params=self.params)
        data_json = r.json()
        self.total = round(data_json.get('count')) // 20 + 1
        if self.next_ == True:
            self.create_card(data_json)

        if data_json['next'] == None:
                self.next_ = False

    def create_card(self, data):
        j = self.page_id * 20 - 20 + 1
        for x in data.get('results'):
            print(x.get('id'))
            self.ids.box.add_widget(
                ListItem(id=x.get('id'), text=str(j) + '. ' +  str(x.get(self.params['lang'])))
            )
            j += 1
        self.load = False

    def go_go_next(self, i):
        if self.next_ == True:
            self.page_id += 1
            self.get_questions()
        self.remove_widget(self.loading)
    
    def go_go_prev(self, i):
        if self.page_id > 1:
            self.page_id -= 1
            self.get_questions()
            self.remove_widget(self.loading)

    def next(self):
        self.ids.myscroll.scroll_y = 1
        if self.next_ == True:
            self.loading = MDLabel(text='Loading ...', halign='center')
            self.add_widget(self.loading)

            self.ids.box.clear_widgets() 
        Clock.schedule_once(self.go_go_next, 0.1)
        
    def prev(self):
        self.ids.myscroll.scroll_y = 1
        self.next_ = True
        if self.page_id > 1:
            self.loading = MDLabel(text='Loading ...', halign='center')
            self.add_widget(self.loading)
            self.ids.box.clear_widgets() 
        Clock.schedule_once(self.go_go_prev, 0.1)

    def on_leave(self):
        self.ids.box.clear_widgets()
        self.next_ = True

    def callback(self):
        self.page_id = 1
        self.manager.current = 'menu'
        App.get_running_app().window_manager.transition.direction = 'right'
        self.event_load.cancel()
        self.remove_widget(self.loading)

class MD3Card(MDCard):
    id = NumericProperty()
    text = StringProperty()
    image = StringProperty()

    def get_questions(self):
        Question.title = self.text
        print(self.text)
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

    def create_card(self, i):
        self.ids.lang.text = self.lang[:2].capitalize()
        for x in self.subjects:
            card = MD3Card(
                id=x.get('id'), text=x.get('name'), image=domain + x.get('image')
            )
            self.ids.box.add_widget(card)

class NotConnection(Screen):
    pass

class App(MDApp):

    def build(self):
        import platform
        print(f'{platform.python_version()=}')

        try:
            r = requests.get(url + '/app/subjects/', timeout=3)
            Menu.subjects = r.json()

            Builder.load_file('index.kv')
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = 'BlueGray'  #"Gray"
            self.theme_cls.primary_hue = "300"
            #self.window_manager = WindoManager(transition=FadeTransition(duration=1))
            self.window_manager = WindoManager()
            return self.window_manager

        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            return MDLabel(text='Connection error!', halign='center')
        except requests.exceptions.ConnectionError as errc:
            return MDLabel(text='Connection error!', halign='center')
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            return MDLabel(text='Connection error!', halign='center')
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            return MDLabel(text='Connection error!', halign='center')

    def build_config(self, config):
        self.config.setdefaults(
            'Settings', {
                'lang': 'en_lang',
                'answer': 'en_answer',
            }
        )

if __name__ == '__main__':
    App().run()
