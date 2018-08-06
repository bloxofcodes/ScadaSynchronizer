from firebase import firebase
import time
from datetime import datetime
if __name__ == '__main__':
    try:

        compareTimeStart = datetime.strptime('00:00:00','%H:%M:%S').time().strftime('%H:%M:%S')
        compareTimeEnd = datetime.strptime('00:05:00','%H:%M:%S').time().strftime('%H:%M:%S')
        compareTime = datetime.strptime(compareTimeEnd,'%H:%M:%S') - datetime.strptime(compareTimeStart,'%H:%M:%S')
        #firebase data timestamp
        datetime1 = datetime.strptime('08-06-18 09:03:00', '%m-%d-%y %H:%M:%S').time().strftime('%H:%M:%S')
        #server time
        datetime2 = datetime.strptime((datetime.now().strftime('%H:%M:%S')),'%H:%M:%S').time().strftime('%H:%M:%S')


        #delta time latest - prev
        elapseTime = datetime.strptime(datetime2,'%H:%M:%S') - datetime.strptime(datetime1,'%H:%M:%S')

        print (datetime1)
        print (datetime2)

        print (compareTime.seconds)
        print (elapseTime.seconds)
        print (compareTime.seconds > elapseTime.seconds)
        # secscompare = (compareTime.hour * 60 * 60) + (compareTime.minute * 60) + compareTime.second
        # print (secscompare / 60)
        # print ((secscompare/60) > (elapseTime.seconds/60))
        #
        # print (secscompare > elapseTime.seconds)
        # print (elapseTime)

        # elapseTime = datetime.time(elapseTime.hour, elapseTime.minute,elapseTime.second)

        #print (type(compareTime))
        #print (type(elapseTime.time()))

        ## your code, typically one function call
        #mytime = datetime.datetime.now()
        #print(mytime.strftime("%m-%d-%y %H:%M:%S"))
        #print ("Press Enter to continue ...")

    except Exception as e:
        print (e)
        # import sys
        # print sys.exc_info()[0]
        # import traceback
        # print traceback.format_exc()
    finally:
        print ("Press Enter to continue ...")
        #input()
