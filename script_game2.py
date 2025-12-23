from random import *
from time import *

def to_create_number(min_lim, max_lim):
    the_secret_number = randint(min_lim, max_lim)

    return the_secret_number

def to_control_limits(min_lim, max_lim):
    not_error = ''
      
    if (not min_lim or str(min_lim).strip() == '-') and (not max_lim or str(max_lim).strip() == '-'):
        error_text = 'Оба поля должны быть заполнены'
        print(error_text)
        return error_text
    elif int(min_lim) >= int(max_lim):
        error_text = 'Минимальное должно быть меньше максимального'
        print(error_text)
        return error_text
    
    return not_error

def to_contol_user_number(min_lim, max_lim, user_number):
    not_error = ''
    
    if not (int(min_lim) <= int(user_number) <= int(max_lim)):
        error_text = (f'Число должно быть в диапазоне от {min_lim} до {max_lim} включительно')
        return error_text
    
    return not_error

def is_winner(the_secret_number, user_number):
    win_text = 'Поздравляю! Вы угадали число!'

    if user_number < the_secret_number:
        not_win_text = 'Это число меньше загаданного'
        return not_win_text
    elif user_number > the_secret_number:
        not_win_text = 'Это число больше загаданного'
        return not_win_text
    
    return win_text

