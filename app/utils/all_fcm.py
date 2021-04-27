from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import datetime
from app.models.user import User 
from app.models.club import Club
from tqdm import tqdm
from app import create_app
from app import logger
import firebase_admin
import sys 

app = create_app('production')
cred = credentials.Certificate('ddyzd-firebase-adminsdk.json')
all_fcm_app = firebase_admin.initialize_app(cred, name='all_fcm_app')


sender = input('동아리 이름(전송자): ')
msg = input('전송할 메시지: ')

students = []
club_id = -1
with app.app_context():
    students = User.query.all()
    club_id = Club.query.filter_by(name=sender).first().id

print(club_id)

def fcm_alarm(sender, msg, club_id, to):
        try:
            aps = messaging.APNSPayload(messaging.Aps(sound="default"))
            message = messaging.Message(
                notification=messaging.Notification(
                    title=sender,
                    body=msg  
                ),
                data={"club_id": str(club_id)},
                apns=messaging.APNSConfig(payload=aps),
                token=to.device_token #eIenkFreQmaxQsHBI21CvD:APA91bE2Um_kj3M5J1m7DvWk44LUAb56VDEtTEhLfKD1VMmOgV-kcgxEP74vJrxfw7puc_Gn1LAIwQzCghPxnn40J1UgG0FfqiXZ1hrGTjv_C-MSxQzi50vG646Fk0f7gmC4_Jl4hrR4
            )
            messaging.send(message)
        except Exception as e:
            logger.info(e)

count = 0
for i in tqdm(range(len(students))):
    fcm_alarm(sender, msg, club_id, students[count])
    count = count + 1