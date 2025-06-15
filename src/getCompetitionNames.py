from sqlite3 import *
def getCompetitionNames(Grade, Sex):
    con = connect('../GTO.db')
    cur = con.cursor()
    if Sex == "Мужской":
        sex_chosen = "Male"
    else:
        sex_chosen = "Female"
    table_name = f"Grade{Grade}{sex_chosen}Standarts"
    command = f"PRAGMA table_info({table_name})"
    cur.execute(command)
    info = cur.fetchall()
    column_names = {}
    for i in range(1, len(info)):
        command = f"SELECT \"{info[i][1]}\" FROM {table_name} WHERE Id = 100"
        cur.execute(command)
        format = cur.fetchone()
        column_names.update({info[i][1]: format[0]})
    cur.close()
    con.close()
    return column_names

def getCompetitionNamesNumber(Number):
    con = connect('../GTO.db')
    cur = con.cursor()
    command = f"SELECT GTOGrade, Sex FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    user = cur.fetchone()
    if user:
        cur.close()
        con.close()
        return getCompetitionNames(user[0], user[1])
