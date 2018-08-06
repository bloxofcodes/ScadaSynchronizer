from firebase import firebase
#from firebase_admin import db
#from firebase_admin import credentials
# firebase = firebase.FirebaseApplication('https://dentalqueue.firebaseio.com/', None)
# firebase = firebase.FirebaseApplication('https://grocr-d5397.firebaseio.com/', None)
firebase = firebase.FirebaseApplication('https://grocr-c344b.firebaseio.com/', None)
# result = firebase.get('/User', None)
# sprint (result)
# {'1': 'John Doe', '2': 'Jane Doe'}
# result = firebase.put('/queueinfo/queuecount','value',"200")
# result = firebase.put('/grocery-items/ahu 1002-8 trip','name','NAKA OFF TWO')
#result = firebase.post('/queueinfo/queuecount','asda' ,{'name':'NAKA OFF TWO'})
#result = firebase.patch('/queueinfo/queuecount',{'value':'400'})
# result = firebase.post('/grocery-items',{'value',"200"})

# result = firebase.put('/grocery-items/','aaaxx',{'name':'ADD DATA AGAIN',
#                             'addedByUser':'Anonymous@awts.com', 'completed':False})




# will add new data on firebase
# result = firebase.patch('/queueinfo/queuecount',{'value':'500'})

# patch method
# result = firebase.post('/grocery-items/',{'name':'ADDED ALERT',
#                             'addedByUser':'Anonymous@awts.com', 'completed':"true"})
result = firebase.patch('/grocery-items/aaaxx',{'name':'ADD DATA AGAINSS',
                            'addedByUser':'Anonymous@awtss.com', 'completed':False})
# print (result)
# firebase.delete('/grocery-items','add data')


# from pyfcm import FCMNotification
#
# push_service = FCMNotification(api_key="<api-key>")
#
# # OR initialize with proxies
#
# # proxy_dict = {
# #           "http"  : "http://127.0.0.1",
# #           "https" : "http://127.0.0.1",
# #         }
# # push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)
#
# # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
#
# registration_id = "<device registration_id>"
# message_title = "Sample Title"
# message_body = "This is a sample body message!."
# result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
#
# print result
# cred = credentials.Certificate('dentalqueue-firebase-adminsdk-y1qrm-5b48476e33.json')
# # Get a database reference to our blog.
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://dentalqueue.firebaseio.com/'
# })




# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# # Fetch the service account key JSON file contents
# cred = credentials.Certificate('dentalqueue-firebase-adminsdk-y1qrm-5b48476e33.json')
#
# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://dentalqueue.firebaseio.com/'
# })
#
# # As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference('/User')
#
# # posts_ref = ref.child('posts')
# #
# #
# # # We can also chain the two calls together
# # posts_ref.push('xxx').set({
# #     'author': 'alanisawesome',
# #     'title': 'The Turing Machine'
# # })
#
# users_ref = ref.child('users')
# users_ref.set({
#     'another': {
#         'date_of_birth': 'June 23, 1912',
#         'full_name': 'Alan Turing'
#     }
# })
#
#
#
# # ref.update({
# #     'alanisawesome': {
# #         'date_of_birth': 'June 23, 1913',
# #         'full_name': 'Alan Turing'
# #     },
# #     'gracehop': {
# #         'date_of_birth': 'December 9, 1906',
# #         'full_name': 'Grace Hopper'
# #     }
# # })
#
#
# print(ref.get())
