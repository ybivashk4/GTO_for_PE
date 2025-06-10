from sqlite3 import *
from datetime import datetime
def inputResult(Grade, Sex, Number, Competition, Competition_number, Result):
    con = connect('../GTO.db')
    cur = con.cursor()
    if Sex == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    table_name = f"Grade{str(Grade)}{str(chosen_sex)}"
    standarts_table_name = f"{table_name}Standarts"
    command = f"SELECT Id, {standarts_table_name}.'{Competition}' FROM {standarts_table_name}"
    cur.execute(command)
    normatives = cur.fetchall()
    if ':' in normatives[99][1]:
        result_time = datetime.strptime(Result, '%M:%S.%f').time()
        for i in range(len(normatives)):
            if normatives[i][1]:
                normative = datetime.strptime(normatives[i][1], '%M:%S.%f').time()
                if normative == result_time:
                    score = float(normatives[i][0])
                    break;
                elif normative < result_time:
                    score = float(normatives[i-1][0])
                    break;
    else:
        for i in range(len(normatives)):
            result = float(Result)
            if normatives[i][1]:
                normative = float(normatives[i][1])
                if normative == result:
                    score = float(normatives[i][0])
                    break;
                elif normative < result:
                    score = float(normatives[i-1][0])
                    break;
    command = f"UPDATE {table_name} SET Соревнование{Competition_number}='{Result}', Балл{Competition_number}={score} WHERE ParticipantId = (SELECT Id FROM Participants WHERE ParticipantNumber = {Number})"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
