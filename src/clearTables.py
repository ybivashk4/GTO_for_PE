from sqlite3 import *
def clear():
    con = connect('../GTO.db')
    cur = con.cursor()
    command = "DELETE FROM Participants"
    cur.execute(command)
    con.commit()
    for i in range(2, 19):
        command = f"DELETE FROM Grade{i}Male"
        cur.execute(command)
        con.commit()
        command = f"DELETE FROM Grade{i}Female"
        cur.execute(command)
        con.commit()
    cur.close()
    con.close()
