from sqlite3 import *
# Функция при вызове удаляет всех участников из таблицы Participants и поскольку эта таблицы связана внешними ключами с таблицами результатов,
# то и в этих таблицах каскадно удаляются записи. Такими образом добивается очистка всей базы данных от участников и их результатов
def clear():
    con = connect('GTO.db')
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    command = "DELETE FROM Participants"
    cur.execute(command)
    con.commit()
    cur.close()
    con.close()
