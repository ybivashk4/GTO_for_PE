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
        command = f"SELECT * FROM Participants WHERE Id = {i[1]}"
        cur.execute(command)
        user = cur.fetchone()
        birth_date = user[5].split("-")
        new_birth_date = f"{birth_date[2]}.{birth_date[1]}.{birth_date[0]}"
        competition_names = getCompetitionNames(Grade, Sex)
        normatives = []
        k = 2
        for j in competition_names:
            normatives.append(j)
            if i[k]:
                normatives.append(i[k])
            else:
                if chosen_sex == "Male":
                    normatives.append('Не участвовал')
                else:
                    normatives.append('Не участвовала')
            normatives.append(i[k+1])
            k += 2
        out_object = (ind+1, user[1], user[2], user[3], new_birth_date, str(user[6]), user[7], normatives, i[len(i)-1])
        output_data.append(out_object)
    cur.close()
    con.close()
    return output_data

def outputTeamsResults():
    con = connect('../GTO.db')
    cur = con.cursor()
    command = f"SELECT DISTINCT Team FROM Participants"
    cur.execute(command)
    result = cur.fetchall()
    teams_results = []
    for i in result:
        team_score = 0
        team_result = []
        team_result.append(i[0])
        command = f"SELECT * FROM Participants WHERE Team = '{i[0]}'"
        cur.execute(command)
        team_participants = cur.fetchall()
        for team_member in team_participants:
            if team_member[4] == "Мужской":
                team_member_sex = "Male"
            else:
                team_member_sex = "Female"
            command = f"SELECT Сумма FROM Grade{team_member[8]}{team_member_sex} WHERE ParticipantId = {team_member[0]}"
            cur.execute(command)
            team_member_score = cur.fetchone()
            if team_member_score:
                team_score += team_member_score[0]
        team_result.append(team_score)
        teams_results.append(team_result)
        teams_results.sort(reverse=True, key=lambda x: x[1])
    for i in range(len(teams_results)):
        teams_results[i].insert(0, i+1)
    cur.close()
    con.close()
    return teams_results

def outputParticipants():
    con = connect('../GTO.db')
    cur = con.cursor()
    command = f"SELECT * FROM Participants ORDER BY Surname, Name, Patronymic"
    cur.execute(command)
    users = cur.fetchall()
    for ind, i in enumerate(users):
        users[ind] = list(users[ind])
        users[ind][0] = ind+1
    cur.close()
    con.close()
    return users

