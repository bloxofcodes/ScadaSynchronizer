import threading
import time
from firebase import firebase

# DONE : Add firebase url references

URL_PATH =  'https://grocr-c344b.firebaseio.com/'
URL_PATH1 = 'https://grocr-c344b.firebaseio.com/'
URL_PATH2 = 'https://grocr-d5397.firebaseio.com/'
URL_PATH3 = 'https://fir-demoapprepo.firebaseio.com/'

SITE_NUMBER = 1
""""
put
patch
get
delete
"""
firebase = firebase.FirebaseApplication(URL_PATH, None)
# DONE : Get data on firebase using get method
def _get_data():
    """Simple get method command in firebase"""
    prevResult = ''
    while True:
        try:
            result = firebase.get('/ack', None)
            if prevResult == '':
                prevResult = result
            if prevResult != result:
                print ('changes in data')
                # Check which key has changes
                for key in prevResult:
                    # print ("prev:")
                    # print (prevResult[key]['isAck'])
                    # print ("current:")
                    # print (result[key]['isAck'])
                    if (prevResult[key]['isAck'] != result[key]['isAck']):
                        print ('changes in data')
                        print (key)

                        firebase.post('/message/',{'errname':prevResult[key]['errname'] + '-ACK',
                                                    'datetime':'2018-08-30 10:00:10 AM',
                                                    'name':'xxx',
                                                    'type':'ackbyserver',
                                                    'site':SITE_NUMBER})

                prevResult = result



            #print (result)
        except KeyboardInterrupt:
            print ("KeyboardInterrupt")

def _get_key_data():
    result = firebase.get('/ack', None)
    print (type(result))
    for key in result:
        print (result[key]['isAck'])

def _post_data():
    """Simple post method command in firebase"""
    """Add new data with auto generated id"""
    result = firebase.post('/message/',{'errname':'AHU-1001 TRIP',
                                        'datetime':'2018-08-30 10:00:10 AM',
                                        'name':'server',
                                        'type':'sentbyserver',
                                        'site':SITE_NUMBER})
    print (result['name'])

    resultack = firebase.put('/ack/',result['name'],{'errname':'AHU-1001 TRIP',
                                                    'isAck':False,
                                                    'name':'',
                                                    'site':SITE_NUMBER})

    print (resultack)

def _post_data_try():
    """Simple post method command in firebase"""
    """Add new data with auto generated id"""
    result = firebase.post('/alarm-items',{'alarmName':'AHU-1001 TRIP',
                                        'dateTime':'2018-08-30 10:00:10 AM',
                                        'phoneNumber':'server'})
    print (result['name'])

    # resultack = firebase.put('/ack/',result['name'],{'errname':'AHU-1001 TRIP',
    #                                                 'isAck':False,
    #                                                 'name':'',
    #                                                 'site':SITE_NUMBER})
    #
    # print (resultack)


# DONE : Add data to firebase using put method
def _add_new_data():
    """Simple add of data using put command"""
    result = firebase.put('/site1/','aaaxx',{'name':'ADD DATA AGAIN',
                                'addedByUser':'Anonymous@awts.com', 'completed':False})

# DONE : Update data on firebase using patch method
def _update_uniqid():
    """Must have a created unique id"""
    result = firebase.patch('/grocery-items/aaaxx',{'name':'ADD DATA AGAINSS',
                                'addedByUser':'Anonymous@awtss.com', 'completed':False})

# DONE : Delete data in firebase using delete method
# TODO : Either create a method passing with an argument by uniqueid
def _delete_data():
    """This will delete a data in the firebase data"""
    """Either by uniqued id"""
    result = firebase.delete('/grocery-items','add data')







if __name__ == '__main__':
    _post_data_try()
    # _post_data()
    # t = threading.Thread(target=_get_data)
    # t.start()
    # _get_key_data()
