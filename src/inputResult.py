from sqlite3 import *
from datetime import datetime
# Функции при вызове передается номер участника, название соревнования и результат
def inputResult(Number, Competition, Result):
    con = connect('GTO.db')
    cur = con.cursor()
    # Команда для выбора участника из БД по его номеру
    command = f"SELECT * FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    user = cur.fetchone()
    if user[4] == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    # Формирование названия таблиц с результатами и нормативами на основе полученных из БД данных
    table_name = f"Grade{user[8]}{chosen_sex}"
    standarts_table_name = f"{table_name}Standarts"
    # Команда для получения баллов и результатов таблицы нормативов
    command = f"SELECT Id, {standarts_table_name}.'{Competition}' FROM {standarts_table_name}"
    cur.execute(command)
    normatives = cur.fetchall()
    # Замена запятой на точку, если пользователь для разделения целой и дробной частей использует запятую
    if ',' in Result:
        Result = Result.replace(',', '.')
    # Определение формата вводимых данных, если в нормативе есть двоеточие, то необходимо обрабатывать как datetime объект,
    # если есть точка, но нет двоеточия, то как float объект, иначе как integer объект (в этом случае надо считать,
    # что чем выше результат - тем выше балл)
    if ':' in normatives[99][1]:
        last_not_none = 0
        # Формирование datetime объекта из строки
        result_time = datetime.strptime(Result, '%M:%S.%f').time()
        # Поиск первого норматива, который будет меньше или равен результату,
        # если меньше результата, то необходимо брать последний не NoneType результат.
        # Если такой результат не найден, считаем, что участник получил 100 баллов
        for i in range(len(normatives)):
            if normatives[i][1]:
                normative = datetime.strptime(normatives[i][1], '%M:%S.%f').time()
                if normative == result_time:
                    score = int(normatives[i][0])
                    break
                elif normative < result_time:
                    score = last_not_none
                    break
                else:
                    score = 100
                    last_not_none = int(normatives[i][0])
    elif '.' in normatives[99][1]:
        last_not_none = 0
        # Поиск первого норматива, который будет меньше или равен результату,
        # если меньше результата, то необходимо брать последний не NoneType результат.
        # Если такой результат не найден, считаем, что участник получил 100 баллов
        for i in range(len(normatives)):
            result = float(Result)
            if normatives[i][1]:
                normative = float(normatives[i][1])
                if normative == result:
                    score = int(normatives[i][0])
                    break
                elif normative < result:
                    score = last_not_none
                    break
                else:
                    score = 100
                    last_not_none = int(normatives[i][0])
    else:
        last_not_none = 0
        # Поиск первого норматива, который будет больше или равен результату,
        # если больше результата, то необходимо брать последний не NoneType результат.
        # Если такой результат не найден, считаем, что участник получил 100 баллов
        for i in range(len(normatives)):
            result = float(Result)
            if normatives[i][1]:
                normative = float(normatives[i][1])
                if normative == result:
                    score = int(normatives[i][0])
                    break
                elif normative > result:
                    score = last_not_none
                    break
                else:
                    score = 100
                    last_not_none = int(normatives[i][0])
    # Команда для получения структуры таблицы с нормативами ступени
    command = f"PRAGMA table_info({standarts_table_name})"
    cur.execute(command)
    table_info = cur.fetchall()
    # Сравнение названия колонок в таблице с нормативами с названием соревнования, которое было передано в функцию, если они совпадают,
    # то копируется номер колонки
    for i in table_info:
        if i[1] == Competition:
            competition_number = i[0]
    # Команда для записи переданного результата и высчитанного балла участника
    command = f"UPDATE {table_name} SET Соревнование{competition_number}='{Result}', Балл{competition_number}={score} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    con.commit()
    # Команда для получения результатов участника по номеру
    command = f"SELECT * FROM {table_name} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    participant_result = cur.fetchone()
    total_score = 0
    # Пересчет суммы баллов участника с добавленным новым результатом
    for i in range(3, len(participant_result) - 1, 2):
        total_score += participant_result[i]
    # Команда для обновления суммы баллов участника
    command = f"UPDATE {table_name} SET Сумма = {total_score} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
