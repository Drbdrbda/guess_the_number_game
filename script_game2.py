from random import *
from time import *
from utils import get_resource_path, get_records_path

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
        return not_win_text, False
    elif user_number > the_secret_number:
        not_win_text = 'Это число больше загаданного'
        return not_win_text, False
    
    return win_text, True

def keep_track_of_time(start_time, end_time):
    result_time = round(end_time - start_time, 3)

    return result_time

def to_write_records(txt, filename = 'records.txt'):
    file_path = get_resource_path(filename)

    with open(file_path, 'a') as file:
        file.write(f'{str(txt)}\n')

def to_update_records(filename = 'records.txt', max_count = 10):
    file_path = get_resource_path(filename)

    result = 'Предыдущих результатов ещё нет'
    records_list = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line not in records_list and len(records_list) <= max_count:
                try:
                    records_list.append(float(line))
                except ValueError:
                    print(f"Предупреждение: некорректное значение в файле: {line}")
                    continue

    records_list = sorted(records_list)

    if len(records_list) > max_count:
        records_list = records_list[:max_count]

    with open(file_path, 'w') as file:
        for record in range(len(records_list)):
            file.write(str(records_list[record]) + '\n')

    if len(records_list) == 0:
        return result
    else:
        result = 'Предыдущие результаты:\n'
        for i, records_list in enumerate(records_list, start=1):
            result += f'\n{i}. {records_list} секунд'

    return result

def to_read_records(filename = 'records.txt'):
    file_path = get_resource_path(filename)

    with open(file_path, 'r') as file:
        cnt = file.read()
    return cnt
