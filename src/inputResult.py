from sqlite3 import *
from datetime import datetime
def inputResult(Number, Competition, Result):
    con = connect('../GTO.db')
    cur = con.cursor()
    command = f"SELECT * FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    user = cur.fetchone()
    if user[4] == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    table_name = f"Grade{user[8]}{chosen_sex}"
    standarts_table_name = f"{table_name}Standarts"
    command = f"SELECT Id, {standarts_table_name}.'{Competition}' FROM {standarts_table_name}"
    cur.execute(command)
    normatives = cur.fetchall()
    if ':' in normatives[99][1]:
        last_not_none = 0
        result_time = datetime.strptime(Result, '%M:%S.%f').time()
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
    command = f"PRAGMA table_info({standarts_table_name})"
    cur.execute(command)
    table_info = cur.fetchall()
    for i in table_info:
        if i[1] == Competition:
            competition_number = i[0]
    command = f"UPDATE {table_name} SET Соревнование{competition_number}='{Result}', Балл{competition_number}={score} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    con.commit()
    command = f"SELECT * FROM {table_name} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    participant_result = cur.fetchone()
    total_score = 0
    for i in range(3, len(participant_result) - 1, 2):
        total_score += participant_result[i]
    command = f"UPDATE {table_name} SET Сумма = {total_score} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
