import pyrebase
from firebasedata import LiveData
import MySQLdb
import datetime

pyrebase_config = {
    "apiKey": "AIzaSyC66S7eKefVdS3cYIYcvnLB",
    "authDomain": "qamessaging-cb430.firebaseapp.com",
    "databaseURL": "https://qamessaging-cb430.firebaseio.com",
    "projectId": "qamessaging-cb430",
    "storageBucket": "qamessaging-cb430.appspot.com"
}

# pyrebase_config = {
#     "apiKey": "AIzaSyCq1zxEuw1hXkzcEBjPwE1m3mrHlomXR3Y",
#     "authDomain": "fir-demoapprepo.firebaseapp.com",
#     "databaseURL": "https://fir-demoapprepo.firebaseio.com",
#     "projectId": "fir-demoapprepo",
#     "storageBucket": "fir-demoapprepo.appspot.com"
# }

app = pyrebase.initialize_app(pyrebase_config)
db = app.database()
# live = LiveData(app, '/message')

# data = live.get_data()
#
# print (data)
# all_data = data.get()
#
# print (all_data)



# def my_handler(sender, value=None):
#     print(value)
#
# live.signal('/message').connect(my_handler)
def stream_handler(message):
    # print(message["event"]) # put
    # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    print (message)
    #print ("changes happen")

def stream_handler2(message):
    # print(message["event"]) # put
    # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    print (message)

#my_stream = db.child("/").stream(stream_handler)
# my_stream2 = db.child("ack").stream(stream_handler2)


sqldb=MySQLdb.connect(passwd="",db="qamessage",user="root")


c=sqldb.cursor()
c.execute("""SELECT * FROM tbl_alertmsg WHERE inprocess != 1""")

result = c.fetchall()


for i in result:
    print (i[1])
    print ("%s" % datetime.datetime.now())
    data = {"alarmname": i[1], "acknowledge":False, "datetime":("%s" % datetime.datetime.now())}
    db.push(data)

print ("goes here")
