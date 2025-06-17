from sqlite3 import *
# Функции при вызове передаются ступень и пол и на основе этих данных она возвращает названия всех соревнований в данной возрастной ступени
def getCompetitionNames(Grade, Sex):
    con = connect('../GTO.db')
    cur = con.cursor()
    if Sex == "Мужской":
        sex_chosen = "Male"
    else:
        sex_chosen = "Female"
    # Название таблицы из которой будем получать названия соревнований создается на основе входных данных
    table_name = f"Grade{Grade}{sex_chosen}Standarts"
    # Команда для получения данных по таблице
    command = f"PRAGMA table_info({table_name})"
    cur.execute(command)
    info = cur.fetchall()
    # Из полученных данных из БД выделяется название колонки и стобалльный результат
    # (для вывода пользователю на экран формата в котором он должен вводить результат)
    column_names = {}
    for i in range(1, len(info)):
        # Команда для получения стобалльного результата соревнования из БД
        command = f"SELECT \"{info[i][1]}\" FROM {table_name} WHERE Id = 100"
        cur.execute(command)
        format = cur.fetchone()
        # Названия и стобалльные результаты добавляются в словарь
        column_names.update({info[i][1]: format[0]})
    cur.close()
    con.close()
    return column_names

# Функции при вызове передается номер участника (не id) и на основе полученного числа она возвращает названия
# всех соревнований ступени в которой находится участник
def getCompetitionNamesNumber(Number):
    con = connect('../GTO.db')
    cur = con.cursor()
    # Команда для получения возрастной ступени и пола участника по его номеру
    command = f"SELECT GTOGrade, Sex FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    user = cur.fetchone()
    if user:
        cur.close()
        con.close()
        # Вызов функции getCompetitionNames, которая вернет словарь с названиями соревнований и стобалльными результатами
        # возрастной ступени к которой принадлежит участник
        return getCompetitionNames(user[0], user[1])
