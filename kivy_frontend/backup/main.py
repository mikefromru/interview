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
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.screenmanager import(
    CardTransition
)
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from threading import Thread

if platform == 'android':
    domain = 'http://iammike.pythonanywhere.com/'
    url = 'http://iammike.pythonanywhere.com/api'

else:
    domain = 'http://iammike.pythonanywhere.com/'
    url = 'http://iammike.pythonanywhere.com/api'
    #domain = 'http://localhost:8000'
    #url = 'http://localhost:8000/api'

    Window.size = (350, 700)
    Window.top = 80
    Window.right = 80

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
        sm.current = 'list_questions'
        sm.transition.direction = 'right'

class ListItem(ButtonBehavior, MDBoxLayout):

    fuck = NumericProperty()
    id = NumericProperty()
    text = StringProperty()
    body = StringProperty()
    params = ObjectProperty()

    def on_release(self):
        if not sm.has_screen(name='detail'):
            print('creating Detail screen ...')
            Builder.load_file('detail.kv')
            sm.add_widget(Detail(name='detail'))
        print('fucky you Scotty')
        Detail.data = {'id': self.id, 'title': self.text, 'body': self.body}
        print(self.id)
        sm.current = 'detail'

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
        print('Question ___init__')

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
            kak = str(j)
            self.ids.box.add_widget(
                ListItem(id=x.get('id'), text=str(x.get(self.params['lang'])))
                #ListItem(id=x.get('id'), text=f'{kak}' + '. ' +  str(x.get(self.params['lang'])))
                #ListItem(id=x.get('id'), fuck=kak, text=str(x.get(self.params['lang'])))
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
        sm.current = 'menu'
        sm.transition.direction = 'right'
        self.event_load.cancel()
        self.remove_widget(self.loading)

class MD3Card(MDCard):
    id = NumericProperty()
    text = StringProperty()
    image = StringProperty()

    def get_questions(self):
        if not sm.has_screen(name='list_questions'):
            print('creating list_question screen ...')
            Builder.load_file('questions.kv')
            sm.add_widget(Question(name='list_questions'))
        Question.title = self.text
        print(self.text)
        Question.id = self.id
        sm.current = 'list_questions'
        sm.transition.direction = 'left'

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
        self.ids.lang.text = self.lang[:2].capitalize()

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

sm = ScreenManager()

class App(MDApp):

    def build(self):
        print('build')

        self.theme_cls.theme_style = "Light"
        #self.theme_cls.primary_palette = 'BlueGray'  #"Gray"
        self.theme_cls.primary_palette = 'BlueGray'  #"Gray"
        self.theme_cls.primary_hue = "300"
        #self.window_manager = WindoManager(transition=FadeTransition(duration=1))

        Builder.load_file('index.kv')
        #Builder.load_file('questions.kv')
        #Builder.load_file('detail.kv')
        sm.add_widget(Menu(name='menu'))
        #sm.add_widget(Question(name='list_questions'))
        #sm.add_widget(Detail(name='detail'))
        return sm
    
    def success(self, req, result):
        Menu.subjects = result
        print(req, result)

    def build_config(self, config):
        self.config.setdefaults(
            'Settings', {
                'lang': 'en_lang',
                'answer': 'en_answer',
            }
        )

if __name__ == '__main__':
    #try: 
        #shutil.rmtree('i/levels')
    #except:
        #pass

    '''
    def success(req, result):
        print('----' *6)
        print(result)
        print('----' *6)
        with open('json_data.json', 'w') as f:
            json.dump(result, f)


    r = UrlRequest(url + '/app/subjects/', on_success=success)
    '''

    
    App().run()
