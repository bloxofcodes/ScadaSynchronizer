import MySQLdb
db=MySQLdb.connect(passwd="",db="qamessage",user="root")


c=db.cursor()
max_price=5
c.execute("""SELECT * FROM tbl_alertmsg WHERE inprocess != 1""")

result = c.fetchall()


for i in result:
    print (i[1])
