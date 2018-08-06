from pusher_push_notifications import PushNotifications

pn_client = PushNotifications(
    instance_id="5fb00808-3b8d-4533-9079-9fec45c7d781",
    secret_key='11027CDC0A5627F5F6EE83961C72D34',
)


response = pn_client.publish(
  interests=['debug-hello'],
  publish_body={
    'apns': {
      'aps': {
        'alert': 'Hello!',
      },
    },
    'fcm': {
      'notification': {
        'title': 'Hello',
        'body': 'Hello, world!',
        'sound':'default',
      },
    },
  },
)

print(response['publishId'])
