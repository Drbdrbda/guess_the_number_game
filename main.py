from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from read_records import to_read_records
from script_game import *

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_menu_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5,'center_y': 0.5}
            )
        
        buttons_menu_layout = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=10,
            padding=20,
        )
        
        btn_new_game = Button(
            text='Новая игра',
            size_hint=(.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size='18sp'
        )
        btn_new_game.bind(on_press=self.to_show_game)
        
        btn_records = Button(
            text='Посмотреть рекорды',
            size_hint=(.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size='18sp'
        )
        btn_records.bind(on_press=self.to_show_records)

        btn_exit = Button(
            text='Выйти из игры',
            size_hint=(.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size='18sp'
        )
        btn_exit.bind(on_press=self.to_confirm_exit)
        
        buttons_menu_layout.add_widget(btn_new_game)
        buttons_menu_layout.add_widget(btn_records)
        buttons_menu_layout.add_widget(btn_exit)
        
        main_menu_layout.add_widget(buttons_menu_layout)
        self.add_widget(main_menu_layout)

    def to_show_game(self, instance):
        self.manager.current = 'game'
    
    def to_show_records(self, instance):
        self.manager.current = 'records'

    def to_confirm_exit(self, instance):
        main_exit_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20)
        
        message = Label(
            text='Вы уверены, что хотите выйти?',
            font_size='18sp'
        )
        
        buttons_exit_layout = BoxLayout(
            spacing=10,
            size_hint=(1, 0.4))
        
        btn_yes = Button(
            text='Да',
            background_color=(0.8, 0.2, 0.2, 1)
            )
        btn_yes.bind(on_press=self.exit_game)

        btn_no = Button(
            text='Нет',
            background_color=(0.2, 0.6, 0.2, 1)
            )
        btn_no.bind(on_press=lambda exit: self.popup.dismiss())
        
        buttons_exit_layout.add_widget(btn_yes)
        buttons_exit_layout.add_widget(btn_no)
        
        main_exit_layout.add_widget(message)
        main_exit_layout.add_widget(buttons_exit_layout)
        
        self.popup = Popup(
            title = 'Подтверждение выхода',
            content = main_exit_layout,
            size_hint=(0.7, 0.4)
        )
        self.popup.open()
    
    def exit_game(self, instance):
        self.popup.dismiss()
        App.get_running_app().stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_game_menu_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.2),
            pos_hint={'center_y': 0.5})
        
        buttons_game_menu_layout = BoxLayout(
            orientation='vertical',
            pos_hint = {"center_x":0.5, "center_y":0.5},
            spacing=10,
            padding=20
            )

        text_input = TextInput(
            hint_text='Введите число',
            size_hint=(.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            insert_text = int,
            multiline = False
        )
        
        btn_confirm_input = Button(
            text ='Подтвердить',
            background_color = (0.2, 0.6, 0.2, 1),
            size_hint = (.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size = '18sp'
        )
        btn_confirm_input.blind(on_press=self.to_save_number)

        btn_back = Button(
            text ='Назад в меню',
            size_hint = (.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size = '18sp'
        )
        btn_back.bind(on_press=self.go_back_to_menu)

        buttons_game_menu_layout.add_widget(text_input)
        buttons_game_menu_layout.add_widget(btn_confirm_input)
        buttons_game_menu_layout.add_widget(btn_back)
        main_game_menu_layout.add_widget(buttons_game_menu_layout)
        self.add_widget(main_game_menu_layout)

    def to_save_number(self, instance):
        entered_number = text_input.text.strip()
        return entered_number

    def go_back_to_menu(self, instance):
        self.manager.current = 'menu'

class RecordsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        buttons_records_layout = BoxLayout(
            orientation='vertical',
            padding=20
        )

        title = Label(
            text='Таблица рекордов',
            font_size='24sp',
            size_hint=(1, 0.2)
        )

        text_label = Label(
            text = 'Текст появится здесь',
            font_size = '16sp',
            size_hint = (1, 0.6)
        )

        text_label.text = to_read_records()

        btn_back = Button(
            text = 'Назад в меню',
            size_hint = (.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size = '18sp'
        )
        btn_back.bind(on_press=self.go_back_to_menu)
        
        buttons_records_layout.add_widget(title)
        buttons_records_layout.add_widget(text_label)
        buttons_records_layout.add_widget(btn_back)
        self.add_widget(buttons_records_layout)
    
    def go_back_to_menu(self, instance):
        self.manager.current = 'menu'

class Game_App(App):
    def build(self):
        self.title = 'Числовая угадайка'
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(RecordsScreen(name='records'))
        return sm
    
    def to_compare_numbers():
        pass
 
if __name__ == '__main__':
    Game_App().run()