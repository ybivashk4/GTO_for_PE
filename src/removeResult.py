from sqlite3 import *
# Функция при вызове получает номер участника и название соревнования результат которого нужно удалить
def removeResult(Number, Competition):
    con = connect('../GTO.db')
    cur = con.cursor()
    # Команда для получения из БД id, возрастную ступень и пол участника номер которого был передан в функцию
    command = f"SELECT Id, GTOGrade, Sex FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    id, grade, sex = cur.fetchone()
    if sex == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    # Формирование названия таблиц с результатами и нормативами на основе полученных из БД данных
    table_name = f"Grade{grade}{chosen_sex}"
    standarts_table_name = f"{table_name}Standarts"
    # Команда для получения структуры таблицы с нормативами, для того чтобы получить индекс соревнования по его названию
    command = f"PRAGMA table_info({standarts_table_name})"
    cur.execute(command)
    table_info = cur.fetchall()
    # Сравнение названия колонок в таблице с нормативами с названием соревнования, которое было передано в функцию, если они совпадают,
    # то копируется номер колонки
    for i in table_info:
        if i[1] == Competition:
            competition_number = i[0]
    # Команда для обнуления результата соревнования и балла за это соревнование для участника
    command = f"UPDATE {table_name} SET 'Соревнование{competition_number}' = NULL, 'Балл{competition_number}' = 0 WHERE ParticipantId = {id}"
    cur.execute(command)
    con.commit()
    # Команда для получения результатов участника по его номеру, необходимо для пересчета суммы баллов участника
    command = f"SELECT * FROM {table_name} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    participant_result = cur.fetchone()
    total_score = 0
    # Подсчет суммы баллов участника
    for i in range(3, len(participant_result) - 1, 2):
        total_score += participant_result[i]
    # Команда для обновление суммы баллов участника
    command = f"UPDATE {table_name} SET Сумма = {total_score} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
