from random import *
from time import *

def is_correct_yes_or_not(answer_option):
    if answer_option.lower() in ('да', 'нет'):
        return True
    return False

def to_review_answer(answer_option):
    while not is_correct_yes_or_not(answer_option):
        answer_option = input('Введите корректный ответ: ')
    return answer_option

def setting_limits():
    min_lim, max_lim = 1, 100
    choice_answer = input('Хотите задать границу допустимых значений? (да / нет): ')
    while not is_correct_yes_or_not(choice_answer):
        choice_answer = to_review_answer(choice_answer)
        continue
    if is_correct_yes_or_not(choice_answer):
        if choice_answer.lower() == 'да':
            min_lim = int(input('Минимальное значение: '))
            max_lim = int(input('Максимальное значение: '))
            print(f'Выбранный интервал: от {min_lim} до {max_lim} включительно')
        else:
            print('В таком случае, будет использован стандартный интервал (от 1 до 100 включительно)')
    return min_lim, max_lim

def is_valid_range(user_text, min_lim, max_lim):
    if user_text.isdigit() and min_lim <= int(user_text) <= max_lim:
        return True
    return False

def to_write_records(txt, filename = 'records.txt'):
    with open(filename, 'a') as file:
        file.write(f'{str(txt)}\n')

def to_play(the_secret_num, user_digit, min_lim, max_lim):
    start_time = time()
    while str(user_digit) != str(the_secret_num):
        if is_valid_range(user_digit, min_lim, max_lim):
            user_digit = int(user_digit)
            if user_digit > the_secret_num:
                print('Это число больше загаданного, попробуйте еще раз')
            else:
                print('Это число меньше загаданного, попробуйте еще раз')
            user_digit = input()
        else:
            print(f'А может быть все-таки введем целое число от {min_lim} до {max_lim}?')
            user_digit = input()
            continue
    end_time = time()
    result_time = round(end_time - start_time, 3)

    to_write_records(result_time)

    print('Вы угадали, поздравляем!', f'Время, за которое было угадано число: {result_time} секунд', sep='\n')

def to_update_records(filename = 'records.txt', max_count = 10):
    records_list = []
    with open(filename, 'r') as file:
        for line in file:
            if line not in records_list and len(records_list) <= max_count:
                records_list.append(float(line))

    records_list = sorted(records_list)

    if len(records_list) > max_count:
        records_list = records_list[:max_count]

    with open(filename, 'w') as file:
        for record in range(len(records_list)):
            file.write(str(records_list[record]) + '\n')

    if len(records_list) == 0:
        print('Предвдущих результатов ещё нет')
    else:
        print('Предыдущие результаты:')
        for i, records_list in enumerate(records_list, start=1):
            print(f'{i}. {records_list} секунд')

def main():
    print('Добро пожаловать в числовую угадайку')
    print(f'Попробуйте угадать число')
    
    replay_flag = 'да'

    while replay_flag.lower() == 'да':
        if replay_flag.lower() == 'да':
            min_limit, max_limit = setting_limits()
            num = randint(min_limit, max_limit)
            answer = input()
            to_play(num, answer, min_limit, max_limit)
            to_update_records()
            replay_flag = input('Хотите сыграть ещё раз? (да/нет): ')
            if not is_correct_yes_or_not(replay_flag):
                replay_flag = to_review_answer(replay_flag)
        if replay_flag.lower() == 'нет':
            print('Спасибо, что играли в числовую угадайку. Еще увидимся!')
            break

main()