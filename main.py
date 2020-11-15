'''
Developer: Юшкевич Игорь
Group: IA-832
Date: 13.11.2020
'''
from selenium import webdriver
from time import sleep
import shelve
from class_Date import Date
from os import remove

# Описание переменных и фукнций

# КАТЕГОРИИ
topics = ['5G', 'IP', 'AI', 'Cloud']

# РАБОТА БОТА
def run_bot():
    TOKEN = 'https://quiz.honorcup.ru/app/?id=57522&sign=d02f37e2f3b36a1eab6644eecad511f8'

    browser = webdriver.Firefox(executable_path='geckodriver.exe')

    xpath = {
        0: '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div',
        1: '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div',
        2: '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[3]/div/div/div[2]/div',
        3: '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[4]/div/div/div[2]/div'
    }

    # ФУНКЦИЯ ЕСЛИ ЕСТЬ ПРАВИЛЬНЫЙ ОТВЕТ
    def present_answer(points, db, answers, object):
        for key in db:
            if db[key] == True:
                correction = key
                break
        for j in range(4):
            if correction == answers[j].text:
                answers[j].click()
                print("Уже был такой вопрос, нажимаю правльный ответ")
                # object.tail()
                points += 2
                return points

    # ФУНКЦИЯ ЕСЛИ БЫЛ ТАКОЙ ВОПРОС, НО НЕТ ПРАВИЛЬНОГО ОТВЕТА
    def no_answer(points, db, answers, cat, question):
        with shelve.open(topics[cat]) as File:
            object = File[question.text]
            for j in range(4):
                if answers[j].text in db.keys():
                    pass
                else:
                    answers[j].click()
                    t = browser.find_elements_by_class_name('game__user-value')
                    after = str(t[0].text[0])
                    if int(after) > points:
                        points += 2
                        object.add_answer(answers[j].text, True)
                        # object.tail()
                        print("Правильный ответ")
                    else:
                        object.add_answer(answers[j].text, False)
                        # object.tail()
                        print('Неправильный ответ')
                    File[question.text] = object
                    return points

    # ФУНКЦИЯ ЕСЛИ НЕ БЫЛО ТАКОГО ВОПРОСА
    def new_question(points, cat, answers, question):
        with shelve.open(topics[cat]) as File:
            sleep(2)
            answers[0].click()
            t = browser.find_elements_by_class_name('game__user-value')
            after = str(t[0].text[0])
            if int(after) > points:
                points += 2
                object = Date(question.text, answers[0].text, True)
                print('Правильный ответ')
                # object.tail()
            else:
                object = Date(question.text, answers[0].text, False)
                print('Неправильный ответ')
                # object.tail()
            File[question.text] = object
            return points

    # ФУНКЦИЯ С ПОМОЩЬЮ КОТОРОЙ ОТКРЫВАЕТСЯ ТЕСТ
    def open_test(categ, tem):
        category = browser.find_elements_by_class_name('slider__item')
        try:
            category[categ].click()
        except IndexError:
            print("IndexError")
        theme = browser.find_elements_by_class_name('profile__theme')
        try:
            theme[tem].click()
        except IndexError:
            print('indexError')
            return False
        categories_play_button = browser.find_element_by_xpath(xpath[tem])
        categories_play_button.click()

    # РЕШЕНИЕ ТЕСТА
    def run_test(ct):
        points_before = 0

        print('У вас {} очков'.format(points_before * 10))
        for i in range(5):
            round_question = browser.find_element_by_class_name('game__question-text')
            round_answers = browser.find_elements_by_class_name('game__answer')

            with shelve.open(topics[ct]) as file:

                # Если был такой вопрос
                if round_question.text in file.keys():
                    object = file[round_question.text]
                    check = object.get_db()

                    # Если есть правильный ответ
                    if True in check.values():
                        points_before = present_answer(points_before, check, round_answers, object)
                        print('У вас {} очков'.format(points_before * 10))
                        sleep(40)



                    # Если нет правильного ответа
                    else:
                        points_before = no_answer(points_before, check, round_answers, ct, round_question)
                        print('У вас {} очков'.format(points_before * 10))
                        sleep(40)


                # если не было такого вопроса
                else:
                    points_before = new_question(points_before, ct, round_answers, round_question)
                    print('У вас {} очков'.format(points_before * 10))
                    sleep(40)


    # MAIN БОТА
    browser.get(TOKEN)
    sleep(4)
    # #click battle_button
    battle_button = browser.find_element_by_class_name('about__buttons')
    battle_button.click()
    while True:
        for ct in range(4):
            for tm in range(4):
                sleep(4)
                # Открытие теста
                open_test(ct, tm)

                sleep(25)
                # Решение теста
                run_test(ct)

                # Выбор другой темы
                replay = browser.find_element_by_xpath('/html/body/app/div[1]/result/div/div/div[9]/div[2]')
                replay.click()
                sleep(4)

# ФУНКЦИЯ ДЛЯ ВЫГРУЗКИ БАЗЫ
def date_base_to_txt():
    for top in topics:
        with shelve.open(top) as file:
            iteration = 1
            try:
                remove(top + '.txt')
            except FileNotFoundError:
                pass
            for key in file.keys():
                object = file[key]
                object.to_txt(top + '.txt', iteration)
                iteration += 1

# MAIN ПРОГРАММЫ
print(__doc__)
print('1. Выгрузить базу с правильными ответами в файлы .txt')
print('2. Запустить бота')
choise = int(input())
if choise == 1:
    date_base_to_txt()
    print('База выгружена')
if choise == 2:
    run_bot()

