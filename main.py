from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from time import *
from script_game2 import *
from utils import get_resource_path, get_records_path

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
        btn_new_game.bind(on_press=self.to_show_settings)
        #btn_new_game.bind(on_press=self.to_show_game)
        
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

    def to_show_settings(self, instance):
        main_limits_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20)
        
        buttons_limits_layout = BoxLayout(
            spacing=10,
            size_hint=(1, 0.4))
        
        self.title = Label(
            text='Задайте диапазон значений',
            font_size='24sp',
            size_hint=(1, 0.2)
        )
        
        self.text_min_limit_input = TextInput(
            hint_text='Минимальное значение',
            size_hint=(.4, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.2},
            input_filter = 'int',
            multiline = False,
            allow_copy = False,
            write_tab=False
            )   

        self.text_max_limit_input = TextInput(
            hint_text='Максимальное значение',
            size_hint=(.4, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.3},
            input_filter = 'int',
            multiline = False,
            allow_copy = False,
            write_tab=False
            )
        
        btn_confirm_limits = Button(
            text ='Подтвердить',
            background_color = (0.2, 0.6, 0.2, 1),
            size_hint = (.3, None),
            height = 50,
            pos_hint = {"center_x":0.5, "center_y":0.5},
            font_size = '18sp'
        )
        btn_confirm_limits.bind(on_press = self.to_save_limits)

        btn_back = Button(
            text='Назад в меню',
            size_hint=(0.3, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size='18sp',
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press = self.go_back_to_menu_from_popup)
        
        main_limits_layout.add_widget(self.title)
        main_limits_layout.add_widget(self.text_min_limit_input)
        main_limits_layout.add_widget(self.text_max_limit_input)
        main_limits_layout.add_widget(btn_confirm_limits)
        main_limits_layout.add_widget(btn_back)
        
        main_limits_layout.add_widget(buttons_limits_layout)

        self.popup = Popup(
            title = 'Задать диапазон значений',
            content = main_limits_layout,
            size_hint=(0.8, 0.8),
            auto_dismiss = False
        )
        self.popup.open()
    
    def to_confirm_error(self, error_text = '', instance = None):
        error_layout = FloatLayout()
        
        self.error_message = Label(
            text = error_text,
            font_size='14sp',
            halign='center', 
            valign='middle',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            text_size=(400, None),
            shorten=False
            )
        btn_ok = Button(
            text='ОК',
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint=(0.4, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.1}
            )
        btn_ok.bind(on_press=lambda ok: self.error_popup.dismiss())

        self.error_popup = Popup(
            title = 'Ошибка',
            content = error_layout,
            size_hint=(0.45, 0.45)
        )
        self.error_popup.open()

        error_layout.add_widget(self.error_message)
        error_layout.add_widget(btn_ok)

    def to_save_limits(self, instance = None):
        entered_min_limit = self.text_min_limit_input.text.strip()
        entered_max_limit = self.text_max_limit_input.text.strip()

        error_text = to_control_limits(entered_min_limit, entered_max_limit)

        app = App.get_running_app()
        app.start_time = time()

        if error_text == '':
            app.min_limit = int(entered_min_limit)
            app.max_limit = int(entered_max_limit)
            app.hidden_number = to_create_number(app.min_limit, app.max_limit)

            self.popup.dismiss()
            self.to_show_game()

        else:
            self.to_confirm_error(error_text)

    def go_back_to_menu_from_popup(self, instance):
        self.popup.dismiss()
        self.manager.current = 'menu'

    def to_show_game(self, instance = None):
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
            size_hint=(0.7, 0.4),
            auto_dismiss = False
        )
        self.popup.open()
    
    def exit_game(self, instance):
        self.popup.dismiss()
        App.get_running_app().stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_game_menu_layout = FloatLayout()
        self.range_label = Label(
            text = '',
            font_size='20sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.9},
            halign='center',
            valign='middle'
        )

        self.text_number_input = TextInput(
            hint_text = 'Введите число',
            size_hint = (0.5, None),
            height = 50,
            pos_hint = {'center_x': 0.5, 'center_y': 0.65},
            input_filter = 'int',
            multiline = False,
            allow_copy = False,
            write_tab = False
        )
        
        btn_confirm_input = Button(
            text='Подтвердить',
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='18sp'
        )
        btn_confirm_input.bind(on_press=self.to_save_number)

        btn_back = Button(
            text='Назад в меню',
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            font_size='18sp'
        )
        btn_back.bind(on_press=self.go_back_to_menu)

        main_game_menu_layout.add_widget(self.range_label)
        main_game_menu_layout.add_widget(self.text_number_input)
        main_game_menu_layout.add_widget(btn_confirm_input)
        main_game_menu_layout.add_widget(btn_back)
        self.add_widget(main_game_menu_layout)

    def on_enter(self):
        app = App.get_running_app()

        if hasattr(app, 'min_limit') and hasattr(app, 'max_limit'):
            self.range_label.text = f'Диапазон значений от {app.min_limit} до {app.max_limit}'
            self.text_number_input.hint_text = f'Введите число от {app.min_limit} до {app.max_limit}'

        self.text_number_input.text = ""

    def to_save_records(self):
        app = App.get_running_app()
        app.end_time = time()
        app.result_time = keep_track_of_time(app.start_time, app.end_time)
        to_write_records(app.result_time, filename='records.txt')

    def close_popup_and_clear(self, instance):
        self.text_number_input.text = ""
        self.win_popup.dismiss()
        self.to_save_records()

        app = App.get_running_app()
        app.update_records_display()

        self.go_back_to_menu(instance)

    def to_confirm_the_win(self):
        win_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20)
        
        win_message = Label(
            text = 'Поздравляю! Вы угадали число!',
            font_size='18sp'
        )

        btn_ok = Button(
            text='ОК',
            background_color=(0.2, 0.6, 0.2, 1),
            size_hint=(0.4, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.1}
            )
        btn_ok.bind(on_press=self.close_popup_and_clear)

        self.win_popup = Popup(
            title = 'Победа',
            content = win_layout,
            size_hint=(0.45, 0.45)
        )
        self.win_popup.open()


        win_layout.add_widget(win_message)
        win_layout.add_widget(btn_ok)

    def to_save_number(self, instance):
        app = App.get_running_app()
        entered_number = self.text_number_input.text.strip()
        
        if not entered_number:
            self.flash_error("Введите число!")
            return
        
        error_text = to_contol_user_number(app.min_limit, app.max_limit, entered_number)
        
        if error_text:
            self.flash_error(error_text)
        else:
            app.user_number = int(entered_number)
            compare_text, win_flag = is_winner(app.hidden_number, app.user_number)
            if win_flag:
                self.to_confirm_the_win()
            else:
                self.flash_success(compare_text)
                self.text_number_input.text = ""

    def flash_error(self, message):
        original_text = self.range_label.text
        original_color = self.range_label.color

        self.range_label.text = message
        self.range_label.color = (1, 0, 0, 1)
        
        for i in range(3):
            Clock.schedule_once(lambda dt, i=i: self.toggle_error_color(i % 2 == 0), i * 0.3)

        Clock.schedule_once(lambda dt: self.restore_range_appearance(original_text, original_color), 2)
        
    def toggle_error_color(self, red):
        if red:
            self.range_label.color = (1, 0, 0, 1)
        else:
            self.range_label.color = (1, 1, 1, 1)
        
    def flash_success(self, message):
        original_text = self.range_label.text
        original_color = self.range_label.color
        
        self.range_label.text = message
        self.range_label.color = (1, 1, 1, 1)
        
        Clock.schedule_once(lambda dt: self.restore_range_appearance(original_text, original_color), 1.5)
        
    def restore_range_appearance(self, text, color):
        self.range_label.text = text
        self.range_label.color = color

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
            text='[b][size=24]ТАБЛИЦА РЕКОРДОВ[/size][/b]',
            markup=True,
            font_size='24sp',
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1)
        )

        self.text_label = Label(
            text='',
            font_size='18sp',
            size_hint=(1, 0.6),
            halign='center',
            valign='middle',
            markup=True
        )

        self.update_records_text()

        btn_back = Button(
            text='Назад в меню',
            size_hint=(0.3, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size='18sp',
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press=self.go_back_to_menu)
        
        buttons_records_layout.add_widget(title)
        buttons_records_layout.add_widget(self.text_label)
        buttons_records_layout.add_widget(btn_back)
        self.add_widget(buttons_records_layout)

    def update_records_text(self):
        records_text = to_update_records(filename='records.txt', max_count=10)
        
        if records_text == 'Предыдущих результатов ещё нет':
            self.text_label.text = 'Рекордов ещё нет'
        else:
            lines = records_text.split('\n')
            formatted = ''
            for line in lines:
                if line.strip() and 'Предыдущие результаты' not in line:
                    formatted += line + '\n\n'
            self.text_label.text = formatted

    def go_back_to_menu(self, instance):
        self.manager.current = 'menu'

class Game_App(App):
    def build(self):
        self.title = 'Числовая угадайка'
        sm = ScreenManager()

        menu_screen = MenuScreen(name='menu')
        game_screen = GameScreen(name='game')
        records_screen = RecordsScreen(name='records')
        
        self.records_screen = records_screen
        
        sm.add_widget(menu_screen)
        sm.add_widget(game_screen)
        sm.add_widget(records_screen)

        return sm
    
    def update_records_display(self):
        if hasattr(self, 'records_screen'):
            self.records_screen.update_records_text()
    
if __name__ == '__main__':
    Game_App().run()