from sqlite3 import *
def removeResult(Number, Competition):
    con = connect('../GTO.db')
    cur = con.cursor()
    command = f"SELECT Id, GTOGrade, Sex FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    id, grade, sex = cur.fetchone()
    if sex == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    table_name = f"Grade{grade}{chosen_sex}"
    standarts_table_name = f"{table_name}Standarts"
    command = f"PRAGMA table_info({standarts_table_name})"
    cur.execute(command)
    table_info = cur.fetchall()
    for i in table_info:
        if i[1] == Competition:
            competition_number = i[0]
    command = f"UPDATE {table_name} SET 'Соревнование{competition_number}' = NULL, 'Балл{competition_number}' = 0 WHERE ParticipantId = {id}"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
