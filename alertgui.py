import MySQLdb
from tkinter import *

master = Tk()

def callback():

    db=MySQLdb.connect(passwd="",db="qamessage",user="root")
    c=db.cursor()
    c.execute("""INSERT INTO `tbl_alertmsg`(`name`, `inprocess`) VALUES ("AHU-1001-TRIP",0)""")
    db.commit()
    db.close()
    print ("click1!")

def callback2():

    db=MySQLdb.connect(passwd="",db="qamessage",user="root")
    c=db.cursor()
    c.execute("""INSERT INTO `tbl_alertmsg`(`name`, `inprocess`) VALUES ("AHU-1002-TRIP",0)""")
    db.commit()
    db.close()
    print ("click2!")


b1 = Button(master, text="AHU-1001-TRIP", command=callback)
b1.pack()

b2 = Button(master, text="AHU-1002-TRIP", command=callback2)
b2.pack()

mainloop()
