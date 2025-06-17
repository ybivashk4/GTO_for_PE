from sqlite3 import *
# Функции при вызове передается номер участника (не id) и она удаляет этого участника, поскольку записи в таблице участников связаны
# внешними ключами с записями в таблицах результатов, то при удалении участника каскадно удаляются его результаты
def removeParticipant(Number):
    con = connect('../GTO.db')
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    command = f"DELETE FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
