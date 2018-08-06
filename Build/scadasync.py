import MySQLdb
import datetime
import threading
import time
import pyrebase
from pusher_push_notifications import PushNotifications

# workon scadasync
# E:
# cd E:\1-Python\(P1) Firebase Connector
# python scadasync.py
# INSERT INTO `tbl_alertmsg`(`name`, `inprocess`) VALUES ("AHU-1001-TRIP",0)

API_KEY = "AIzaSyC66S7eKefVdS3cYIYcvnLB"
AUTH_DOMAIN = "qamessaging-cb430.firebaseapp.com"
DBURL = "https://qamessaging-cb430.firebaseio.com"
PROJECT_ID = "qamessaging-cb430"
STORAGE_BUCK = "qamessaging-cb430.appspot.com"
SERVICE_ACCT = "qamessaging.json"
PUSHER_INTEREST = "debug-hello"

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
                'body': data['alarmname'],
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
        self.serviceacct = SERVICE_ACCT


    def config(self):
        self.pyrebase_config = {
            "apiKey": self.apikey,
            "authDomain": self.authdomain,
            "databaseURL": self.dburl,
            "projectId": self.projid,
            "storageBucket": self.storebuck,
            "serviceAccount": self.serviceacct
        }

    def firebase_connect(self):
        self.app = pyrebase.initialize_app(self.pyrebase_config)
        self.db = self.app.database()

    def firebase_insert(self,data):
        try:
            self.db.push(data)
        except Exception as e:
            print (e)
            raise Exception("Problem Insertin in Firebase!")

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

class InvokeTimer(threading.Thread):
    def run(self):
        dbfetcher = DbFetcher(user="root",db="qamessage",passwd="")
        firebaseCmd = FireBaseCommands()
        beamPushNotif = BeamPusherNotif()
        #Set firebase config
        firebaseCmd.config()
        firebaseCmd.firebase_connect()
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

                        print ("Inserting to Firebase as Records as of " +  ("%s" % datetime.datetime.now()) + "!")
                        data = {"alarmname": i[1], "acknowledge":False, "datetime":("%s" % datetime.datetime.now())}
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



if __name__ == '__main__':
    invokeTimer = InvokeTimer()
    invokeTimer.start()

    # dbfetcher.connect()
    # t = threading.Timer(1.0,dbfetcher.query_data)
    # t.start()
    # dbfetcher.query_data()
