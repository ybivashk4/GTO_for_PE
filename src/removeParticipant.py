from sqlite3 import *
def removeParticipant(Number):
    con = connect('../GTO.db')
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    command = f"DELETE FROM Participants WHERE ParticipantNumber = {Number}"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
