import MySQLdb
# import datetime
from datetime import datetime
import threading
import time
import pyrebase
from pusher_push_notifications import PushNotifications

GLOBAL_LIST = []
# workon scadasync
# E:
# cd E:\1-Python\(P1) Firebase Connector
# python scadasync.py
# INSERT INTO `tbl_alertmsg`(`name`, `inprocess`) VALUES ("AHU-1001-TRIP",0)
PROD_TAG = 'JV'
FIRST_EVENT = False

if PROD_TAG != 'JV': # Production
    #production
    API_KEY = "AIzaSyB4IJv1JRUDhafwoksYENIGyl1w1028n7k"
    AUTH_DOMAIN = "grocr-c344b.firebaseapp.com"
    DBURL = "https://grocr-c344b.firebaseio.com"
    PROJECT_ID = "grocr-c344b"
    STORAGE_BUCK = "grocr-c344b.appspot.com"
else: # development
    API_KEY = "AIzaSyC66S7eKefVdS3cYIYcvnLB"
    AUTH_DOMAIN = "qamessaging-cb430.firebaseapp.com"
    DBURL = "https://qamessaging-cb430.firebaseio.com"
    PROJECT_ID = "qamessaging-cb430"
    STORAGE_BUCK = "qamessaging-cb430.appspot.com"

PUSHER_INTEREST = "debug-hello"
TIME_CHECK = 4#60 # (60s * 5)/60m
TIME_COMPARE = '00:01:00'

class BeamPusherNotif():

    def push_notif(self,data):
        pn_client = PushNotifications(
            instance_id="5fb00808-3b8d-4533-9079-9fec45c7d781",
            secret_key='11027CDC0A5627F5F6EE83961C72D34',
        )
        response = pn_client.publish(
          interests=[PUSHER_INTEREST],
          publish_body={
            'apns': {
              'aps': {
                'alert': 'Hello!',
              },
            },
            'fcm': {
              'notification': {
                'title': 'ALERT MESSAGE',
                'body': data['alarmName'],
                'sound':'default',
              },
            },
          },
        )

        print(response['publishId'])

class FireBaseCommands(dict):
    def __init__(self):
        self.apikey = API_KEY
        self.authdomain = AUTH_DOMAIN
        self.dburl = DBURL
        self.projid = PROJECT_ID
        self.storebuck = STORAGE_BUCK


    def config(self):
        self.pyrebase_config = {
            "apiKey": self.apikey,
            "authDomain": self.authdomain,
            "databaseURL": self.dburl,
            "projectId": self.projid,
            "storageBucket": self.storebuck
        }

    def firebase_connect(self):
        self.app = pyrebase.initialize_app(self.pyrebase_config)
        self.db = self.app.database()

    def firebase_insert(self,data):
        try:
            self.db.child('alarm-items').push(data)
        except Exception as e:
            print (e)
            raise Exception("Problem Insertin in Firebase!")
    def firebase_query_byindex(self,node,index,value):

        if(node == None):
            raise ValueError("Node Cannot be empty!")
        if(index == None):
            raise ValueError("Index Cannot be empty!")
        if(value == None):
            raise ValueError("Value Cannot be empty!")

        try:
            return (self.db.child(node).order_by_child(index).equal_to(value).get())
        except Exception as e:
            print (e)
            raise Exception("Problem in Firebase Indexing!")

    def firebase_update_id(self,node,keyid,data):
        try:
            self.db.child(node).child(keyid).update(data)
        except Exception as e:
            print (e)
            raise Exception("Problem Update in Firebase!")
    def firebase_data(self,alarname,acknowledge,datetime,phonenum):
        return ({"alarmName": alarname, "acknowledge":acknowledge, "dateTime":datetime,"phoneNum":phonenum,"userName":"","dateTimeACK":""})

    def callback(self,func):
        my_stream = self.db.child("alarm-items").stream(func)

class DbFetcher(list):
    def __init__(self,user,db,passwd):
        self.user = user
        self.db = db
        self.password = passwd

    def connect(self):
        try:
            self.sqldb = MySQLdb.connect(passwd=self.password,db=self.db,user=self.user)
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            raise Exception("Problem Connecting in the database")

    def close(self):
        self.sqldb.close()

    def commit(self):
        self.sqldb.commit()
    def query_data(self):
        try:
            self.cursor=self.sqldb.cursor()
            self.cursor.execute("""SELECT * FROM tbl_alertmsg WHERE inprocess != 1""")
            self.result = self.cursor.fetchall()

            if len(self.result) > 0:
                print ("%d data was fetch..." % len(self.result))
                return self.result
                    # data = {"alarmname": i[1], "acknowledge":False, "datetime":("%s" % datetime.datetime.now())}
                    # db.push(data)
        except Exception as e:
            raise Exception("Problem getting data to scada!")

    def update_inprocess(self,id):
        try:
            print ("Update Method!")
            self.cursor=self.sqldb.cursor()
            self.cursor.execute("""UPDATE tbl_alertmsg SET inprocess=1 WHERE id = %d""" % (id))

            print ("Passing Update Method!")
            #self.close()
        except Exception as e:
            print (e)
            raise Exception("Unable to update the inprocess!")


# class InvokeTimerForEscalation(threading.Thread):
#     def run(self):
#         count = 0
#         firebaseCmd = FireBaseCommands()
#         beamPushNotif = BeamPusherNotif()
#         firebaseCmd.config()
#         firebaseCmd.firebase_connect()
#         while True:
#             if (count == TIME_CHECK):
#                 # TODO : Check data if there are more than 5 minutes alarm items not 'acknowledge'
#                 # TODO : Use the autogenerate id for updating the content 'acknowledge' as empty
#                 # TODO : Create new instance re-write the previous data with new 'datetime' posted
#                 # db.child("alarm-items").order_by_child("acknowledge").equal_to(False)
#                 print ("5mins time triggered!")
#                 fquery = firebaseCmd.firebase_query_byindex("alarm-items","acknowledge","false")
#                 for q in fquery.each():
#                     firebaseCmd.firebase_update_id("alarm-items",q.key(),{"acknowledge":""})
#                     print(q.key()) # Morty
#                     print(q.val()["alarmName"]) # {name": "Mortimer 'Morty' Smith"}
#                     timestamp = datetime.datetime.now()
#                     # data = {"alarmName": q.val()["alarmName"], "acknowledge":False, "dateTime":q.val()["dateTime"],"phoneNum":""}
#                     data = firebaseCmd.firebase_data(alarname=q.val()["alarmName"], \
#                                                 acknowledge="false", \
#                                                 datetime=("%s" % timestamp.strftime("%d-%m-%y %H:%M:%S")), \
#                                                 phonenum="")
#                     firebaseCmd.firebase_insert(data)
#                     beamPushNotif.push_notif(data)
#
#                 count = 0
#             count = count + 1
#             time.sleep(5)

class InvokeDateTimerForEscalation(threading.Thread):
    def run(self):
        global GLOBAL_LIST
        count = 0
        firebaseCmd = FireBaseCommands()
        beamPushNotif = BeamPusherNotif()
        firebaseCmd.config()
        firebaseCmd.firebase_connect()
        while True:
            # print ("GLOBAL LIST")
            # print (GLOBAL_LIST)
            # if (count == TIME_CHECK):
                # TODO : Check data if there are more than 5 minutes alarm items not 'acknowledge'
                # TODO : Use the autogenerate id for updating the content 'acknowledge' as empty
                # TODO : Create new instance re-write the previous data with new 'datetime' posted
                # db.child("alarm-items").order_by_child("acknowledge").equal_to(False)
            print ("Cycle 10s triggered!")
            fquery = firebaseCmd.firebase_query_byindex("alarm-items","acknowledge","false")
            for q in fquery.each():
                # firebaseCmd.firebase_update_id("alarm-items",q.key(),{"acknowledge":""})
                # print(q.key()) # Morty
                # print(q.val()["alarmName"]) # {name": "Mortimer 'Morty' Smith"}
                # print(q.val()["dateTime"]) # {name": "Mortimer 'Morty' Smith"}

                compareTimeStart = datetime.strptime('00:00:00','%H:%M:%S').time().strftime('%H:%M:%S')
                compareTimeEnd = datetime.strptime(TIME_COMPARE,'%H:%M:%S').time().strftime('%H:%M:%S')
                compareTime = datetime.strptime(compareTimeEnd,'%H:%M:%S') - datetime.strptime(compareTimeStart,'%H:%M:%S')
                #firebase data timestamp
                datetime1 = datetime.strptime(q.val()["dateTime"], '%m-%d-%y %H:%M:%S').time().strftime('%H:%M:%S')
                #server time
                datetime2 = datetime.strptime((datetime.now().strftime('%H:%M:%S')),'%H:%M:%S').time().strftime('%H:%M:%S')
                #delta time latest - prev
                elapseTime = datetime.strptime(datetime2,'%H:%M:%S') - datetime.strptime(datetime1,'%H:%M:%S')
                # print (datetime1)
                # print (datetime2)
                # print (compareTime.seconds)
                # print (elapseTime.seconds)
                # print (compareTime.seconds > elapseTime.seconds)
                if((compareTime.seconds > elapseTime.seconds) == False):
                    # print ("Jv Here")
                    firebaseCmd.firebase_update_id("alarm-items",q.key(),{"acknowledge":""})
                    timestamp = datetime.now()
                    data = firebaseCmd.firebase_data(alarname=q.val()["alarmName"], \
                                                acknowledge="false", \
                                                datetime=("%s" % timestamp.strftime("%d-%m-%y %H:%M:%S")), \
                                                phonenum="")
                    firebaseCmd.firebase_insert(data)
                    beamPushNotif.push_notif(data)
                    # print ("Jv Out")

            # 10s cycle time
            time.sleep(10)

class InvokeTimer(threading.Thread):
    def run(self):
        dbfetcher = DbFetcher(user="root",db="qamessage",passwd="")
        firebaseCmd = FireBaseCommands()
        beamPushNotif = BeamPusherNotif()
        #Set firebase config
        firebaseCmd.config()
        firebaseCmd.firebase_connect()
        print ("Scada Synchronizer Started Listening...")
        while True:
            try:
                # DONE : Connect to database
                dbfetcher.connect()
                #DONE : Query data to scada logs
                #DONE : update the queried scada logs as inprocess = 1
                #TODO : send query scada logs to firebase
                result = dbfetcher.query_data()
                if result != None and len(result) > 0:
                    for i in result:
                        #print (i[0])
                        #print ("%s" % datetime.datetime.now())

                        print ("Inserting to Firebase as Records as of " +  ("%s" % datetime.now()) + "!")
                        timestamp = datetime.now()

                        # data = {"alarmName": i[1], "acknowledge":False, "dateTime":("%s" % timestamp.strftime("%d-%m-%y %H:%M:%S")),"phoneNum":""}
                        data = firebaseCmd.firebase_data(alarname=i[1], \
                                                    acknowledge="false", \
                                                    datetime=("%s" % timestamp.strftime("%d-%m-%y %H:%M:%S")), \
                                                    phonenum="")

                        firebaseCmd.firebase_insert(data)
                        beamPushNotif.push_notif(data)
                        print ("Updating Records..")
                        dbfetcher.update_inprocess(i[0])
                    dbfetcher.commit()
                    print ("Updating Records Done!")



                #TODO : update scada logs inprocess = 2 if successfully added to firebase
                dbfetcher.close()
                time.sleep(1)
            except Exception as e:
                print(e)
                break

def stream_handler(message):
    """This function is waiting for a callback changes in firebase"""
    """wanted to implement this method for copying the data from firebase"""
    """where acknowledge items was false"""
    global GLOBAL_LIST
    if message['path'] != '/':
        print (message['path'])
        if(message['data']['acknowledge'] != "false"):
            print ("ack id remove in list to monitor")
            print (message['path'].strip('/'))
            print ("LEN GLOBAL LIST")
            print(len(GLOBAL_LIST))
            if(len(GLOBAL_LIST) > 0):
                if message['path'].strip('/') in GLOBAL_LIST:
                    GLOBAL_LIST.remove(message['path'].strip('/'))
        else:
            print ("ack id add in list to monitor")
            # if message['path'] not in GLOBAL_LIST:
            GLOBAL_LIST.append(message['path'].strip('/'))
    else:
        print ("MESSAGE DATA")
        print (message['data'])
        for k,v in message['data'].items():
            if(v['acknowledge'] == "false"):
                print ("FALSESEESSE")
                GLOBAL_LIST.append(k.strip('/'))
        # print (GLOBAL_LIST)


if __name__ == '__main__':
    print ("Scada Synchronizer Starting...")
    invokeTimer = InvokeTimer()
    invokeTimer.start()

    # 5mins check time for every acknowledge "False"
    # invokeTimeForEscalate = InvokeTimerForEscalation()
    # invokeTimeForEscalate.start()
    #Triggers
    invokeDateTimeForEscalate = InvokeDateTimerForEscalation()
    invokeDateTimeForEscalate.start()

    # fCmd = FireBaseCommands()
    # fCmd.config()
    # fCmd.firebase_connect()
    # fCmd.callback(stream_handler)

    # Commented
    # dbfetcher.connect()
    # t = threading.Timer(1.0,dbfetcher.query_data)
    # t.start()
    # dbfetcher.query_data()
