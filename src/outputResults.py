from getCompetitionNames import *
def outputAllGradeResults(Grade, Sex):
    con = connect('../GTO.db')
    cur = con.cursor()
    if Sex == "Мужской":
        chosen_sex = "Male"
    else:
        chosen_sex = "Female"
    command = f"SELECT * FROM Grade{Grade}{chosen_sex} ORDER BY Сумма DESC"
    cur.execute(command)
    result = cur.fetchall()
    output_data = []
    for ind, i in enumerate(result):
        command = f"SELECT * FROM Participants WHERE ParticipantNumber = {i[1]}"
        cur.execute(command)
        user = cur.fetchone()
        birth_date = user[5].split("-")
        new_birth_date = f"{birth_date[2]}.{birth_date[1]}.{birth_date[0]}"
        competition_names = getCompetitionNames(Grade, Sex)
        normatives = []
        k = 2
        for j in competition_names:
            normatives.append(j)
            normatives.append(i[k])
            normatives.append(i[k+1])
            k+=2
        Out_object = (ind+1, user[1], user[2], user[3], new_birth_date, str(user[6]), user[7], normatives, i[len(i)-1])
        output_data.append(Out_object)
    cur.close()
    con.close()
    return output_data

for i in outputAllGradeResults(8, "Мужской"):
    print(i)

