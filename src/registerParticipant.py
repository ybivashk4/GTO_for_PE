from sqlite3 import *
from datetime import datetime
# Функции при вызове передается ФИО, пол, дата рождения, номер и команда участника, функция на основе этих данных высчитывает возрастную
# ступень участника и добавляет его в БД
def register(Surname, Name, Patronymic, Sex, BirthDate, ParticipantNumber, Team):
    con = connect('GTO.db')
    cur = con.cursor()
    # Высчитывание возраста участника на основе полученной строки с датой рождения (на основе даты на компьютере)
    year, month, day = map(int, BirthDate.split("-"))
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    # Определение возрастной ступени ГТО участника на основе его возраста
    if 8 <= age <= 9:
        grade = 2
    elif 10 <= age <= 11:
        grade = 3
    elif 12 <= age <= 13:
        grade = 4
    elif 14 <= age <= 15:
        grade = 5
    elif 16 <= age <= 17:
        grade = 6
    elif 18 <= age <= 19:
        grade = 7
    elif 20 <= age <= 24:
        grade = 8
    elif 25 <= age <= 29:
        grade = 9
    elif 30 <= age <= 34:
        grade = 10
    elif 35 <= age <= 39:
        grade = 11
    elif 40 <= age <= 44:
        grade = 12
    elif 45 <= age <= 49:
        grade = 13
    elif 50 <= age <= 54:
        grade = 14
    elif 55 <= age <= 59:
        grade = 15
    elif 60 <= age <= 64:
        grade = 16
    elif 65 <= age <= 69:
        grade = 17
    elif 70 <= age:
        grade = 18
    # Команда на добавление нового участника в БД
    command = f"INSERT INTO Participants VALUES ((SELECT (MAX(Id)+1) from Participants), '{Surname}', '{Name}', '{Patronymic}', '{Sex}', '{BirthDate}', {str(ParticipantNumber)}, '{Team}', {str(grade)})"
    cur.execute(command)
    con.commit()
    if Sex == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    # Формирование названия таблицы с результатами в которую будет добавлена запись с новым участником
    table_name = f"Grade{str(grade)}{str(chosen_sex)}"
    # Команда на добавление новой записи с результатами участника (изначально пустая)
    command = f"INSERT INTO {table_name} (Id, ParticipantId) VALUES ((SELECT (MAX(Id)+1) from {table_name} ), (SELECT MAX(Id) from Participants))"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
