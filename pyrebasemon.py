import pyrebase
from firebasedata import LiveData

pyrebase_config = {
    "apiKey": "AIzaSyC66S7eKefVdS3cYIYcvnLB",
    "authDomain": "qamessaging-cb430.firebaseapp.com",
    "databaseURL": "https://qamessaging-cb430.firebaseio.com",
    "projectId": "qamessaging-cb430",
    "storageBucket": "qamessaging-cb430.appspot.com"
}


# API_KEY = "AIzaSyC66S7eKefVdS3cYIYcvnLB"
# AUTH_DOMAIN = "qamessaging-cb430.firebaseapp.com"
# DBURL = "https://qamessaging-cb430.firebaseio.com"
# PROJECT_ID = "qamessaging-cb430"
# STORAGE_BUCK = "qamessaging-cb430.appspot.com"

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

# data = {"errname": "AHU-1001 TRIP", "completed":False}
# db.child("messages").push(data)
#
# print ("goes here")
#
# my_stream = db.child("messages").stream(stream_handler)


# fire_query = db.child("alarm-items").order_by_key().get()#db.child("alarm-items").child("acknowledge").equal_to(False).get()
fire_query = db.child("alarm-items").order_by_child("acknowledge").equal_to(False) \
                                    .order_by_child("alarmName").equal_to("AHU-1002-TRIP").get()#db.child("alarm-items").child("acknowledge").equal_to(False).get()

print(type(fire_query))

for user in fire_query.each():
    print(user.key()) # Morty
    print(user.val()) # {name": "Mortimer 'Morty' Smith"}
