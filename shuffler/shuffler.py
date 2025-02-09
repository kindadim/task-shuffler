"""Shuffle randomizes lists"""
from random import shuffle
import sys


def read_files(file_name):
    """Opens file, returns list of lines and line count"""
    with open(file_name, 'r', encoding='utf-8') as file:
        file_list = []
        line_count = 0
        for line in file:
            read_list = line.splitlines()
            read_list = [x for x in read_list if x]
            file_list += read_list
            line_count += 1
            continue
    return file_list, line_count

def shuffler(file_list):
    """A funny little shuffle"""
    shuffle(file_list)
    return file_list

def format_check(title_file):
    """Ensures that the lines of title_file follow the correct format"""
    titles = read_files(title_file)[0]
    for line in titles:
        new = line.split(',')
        if len(new) > 2:
            print('Format incorrect: Additional values.')
            print('Correct format: <name>, <weight>')
            print(f'Provided format: {line}')
            sys.exit()
        elif len(new) < 2:
            print('Format incorrect: Missing values.'
                  'Correct format: <name>, <weight>')
            print(f'Provided format: {line}')
            sys.exit()
        else:
            continue

def task_list(task_file):
    """Uses read_file() and shuffler() on task_file"""
    tasks, task_count = shuffler(read_files(task_file)[0]), (read_files(task_file)[1])
    return tasks, task_count

def title_list(title_file):
    """Uses read_file() and shuffler() on title_file, orders titles by weight"""
    format_check(title_file)
    titles = shuffler(read_files(title_file)[0])

    titles.sort(reverse=True, key=lambda v: v.split()[-1])
    return titles

def unavailable_people(title_file):
    """Allows an input for people that will be unavailable"""
    ua_list = ''
    ticker = 0
    titles = read_files(title_file)[0]
    while ticker < 2:
        ua = input('Input the name of an unavailable person. If none, press ENTER: ')
        if ua != '':
            for title in titles:
                name = str(title).split(',', maxsplit=1)[0]
                if ua == name:
                    print(f'{ua} is unavailable.')
                    ua_list += f'{name}, '
        elif ua == '':
            if ua_list == '':
                print('All available. '
                      'Continuing assignment...\n\n'
                      '-=-=- Chore Roster -=-=-')
            else:
                print(f'Absences: {ua_list[:-2]}.\n'
                       'Continuing assignment...\n\n'
                       '-=-=- Chore Roster -=-=-')
            ticker += 2
    return ua_list

def zipper(titles, tasks, task_count):
    """Zips titles/tasks, resets/adds weight, refactors titles"""
    to_file = ''
    assigned = zip(titles, tasks)
    for title, task in assigned:
        name = title.split(',')[0]
        name = str(name.replace('[', '').replace(']', '').replace('\'', ''))
        print(f'{name} - {task}')
        to_file += f'{name}, 0\n'
        continue
    unassigned = titles[task_count:]
    for title in unassigned:
        name, weight = title.split(',')[0], title.split(',')[1]
        weight = int(weight) + 1
        to_file += f'{name}, {weight}\n'
        continue
    return to_file

def assign(title_file, task_file):
    """Writes to_file to title_file"""
    unavailable_people(title_file)
    to_file = zipper(
                    title_list(title_file),
                    task_list(task_file)[0],
                    task_list(task_file)[1])
    with open(title_file, 'w', encoding='utf-8') as file:
        file.write(to_file)