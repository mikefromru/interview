import requests
import urllib
from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.lang import Builder

from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior 
from kivymd.uix.boxlayout import MDBoxLayout

from ..detail.detail import Detail

from kivy.utils import platform

if platform == 'android':
    domain = 'http://iammike.pythonanywhere.com/'
    url = 'http://iammike.pythonanywhere.com/api'

else:
    domain = 'http://iammike.pythonanywhere.com/'
    url = 'http://iammike.pythonanywhere.com/api'

    #domain = 'http://localhost:8000'
    #url = 'http://localhost:8000/api'


#domain = 'http://localhost:8000'
#url = 'http://localhost:8000/api'


class ListItem(ButtonBehavior, MDBoxLayout):
    
    fuck = NumericProperty()
    id = NumericProperty()
    text = StringProperty()
    body = StringProperty()
    params = ObjectProperty()

    def on_release(self):
        Detail.data = {'id': self.id, 'title': self.text, 'body': self.body}
        MDApp.get_running_app().sm.current = 'detail'
        MDApp.get_running_app().sm.transition.direction = 'left'

class Question(Screen):
    
    title = StringProperty()
    params = ObjectProperty()
    id = NumericProperty()
    total = NumericProperty(0)
    page_id = NumericProperty(1)
    count = NumericProperty()
    next_ = True
    load = True
    check_it = False

    def __init__(self, *args, **kwargs):
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
        #self.get_questions()
        # Create  Detail screen if it doesn't exists
        if not MDApp.get_running_app().sm.has_screen(name='detail'):
            print('creating Detail screen ...')
            Builder.load_file('screens/detail/detail.kv')
            MDApp.get_running_app().sm.add_widget(Detail(name='detail'))

        self.ids.mytitle.title = self.title.capitalize()
        self.event_load = Clock.schedule_interval(self.checking_load, 0.1)
        self.loading = MDLabel(text='Loading ...', halign='center')
        self.add_widget(self.loading)
        Detail.params = self.params

    def on_leave(self, *args):
        self.event_load.cancel()
        self.remove_widget(self.loading)
        self.title = ''
        self.ids.mytitle.title = ''

    def get_questions(self, i=None):
        print(self.page_id, ' page_id')
        self.r = requests.get(url + f'/app/subject/{self.id}/?page={self.page_id}', params=self.params, timeout=None)
        data_json = self.r.json()
        
        print('<<<< - >>>>')
        print(data_json)
        print('<<<< - >>>>')
        self.total = round(data_json.get('count')) // 20 + 1
        if self.next_ == True:
            self.create_card(data_json)

        if data_json['next'] == None:
                self.next_ = False

        self.load = False
        
    def create_card(self, data):

        def bak(i): 
            j = self.page_id * 20 - 20 + 1
            for x in data.get('results')[self.slice_1:self.slice_2]:
                print(x.get('id'))
                kak = str(j)
                self.ids.box.add_widget(
                    ListItem(id=x.get('id'), text=str(x.get(self.params['lang'])))
                )
                j += 1
            self.slice_1 += 10
            self.slice_2 += 10

            print(self.slice_2)
            if self.slice_2 > 20:
                self.event_cards.cancel()
            print('working working ...')

        self.slice_1, self.slice_2 = 0, 10
        self.event_cards = Clock.schedule_interval(bak, 0.01)

    def next(self):
        self.event_cards.cancel()
        self.ids.myscroll.scroll_y = 1
        if self.next_ == True:
            self.ids.box.clear_widgets() 
            self.page_id += 1
            #Clock.schedule_once(self.get_questions, 0.7)
            Clock.schedule_once(self.get_questions, 0.0)

    def prev(self):
        self.event_cards.cancel()
        self.ids.myscroll.scroll_y = 1
        self.next_ = True
        if self.page_id > 1:
            self.ids.box.clear_widgets() 
            self.page_id -= 1
            #Clock.schedule_once(self.get_questions, 0.7)
            Clock.schedule_once(self.get_questions, 0.0)

    def on_leave(self):
        self.event_cards.cancel()
        self.ids.box.clear_widgets()
        self.next_ = True

    def callback(self):
        self.ids.mytitle.title = ''
        self.event_cards.cancel()
        print('fuck you bitch')
        self.page_id = 1
        #self.sm.current = 'menu'
        MDApp.get_running_app().sm.current = 'menu'
        MDApp.get_running_app().sm.transition.direction = 'right'
        self.event_load.cancel()
        self.remove_widget(self.loading)
