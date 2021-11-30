
import os
from flask import Flask, request
# !pip3 install dlib
# !pip3 install face_recognition
# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Face Recognition entrypoint'

@app.route('/face', methods=['GET','POST'])
def face():
    import FaceRecog
    import requests
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    cred = credentials.Certificate('FBkey.json')

    try:
        firebase_admin.initialize_app(cred)
    except:
        pass
    db = firestore.client()


    id = request.args.get('id')
    #Check FireBase collection if needs to be changed
    user_ref = db.collection(u'ProUsers').document(id)
    doc = user_ref.get()

    Auth_img_url = doc.to_dict()['dpUrl'] # single URL main IMG
    Verify_img_url = doc.to_dict()['imgUrls'] # list of urls of multiple IMG

    # temp folder directory
    # only two imgs at a time
    # dpimg will remain same
    # authimg will change based on list urls
    r1 = requests.get(Auth_img_url)
    with open("dpimg.jpg", "wb") as f:
        f.write(r1.content)
    img1 = "dpimg.jpg"

    FR_Verification = False
    try:
        for x in Verify_img_url:

            r2 = requests.get(x['image'])
            with open("authimg.jpg", "wb") as f:
                f.write(r2.content)
                
            img2 = "authimg.jpg"

            FR_Verification = FaceRecog.SelfieAuth(img1, img2)
            if FR_Verification == True:
                os.remove("dpimg.jpg")
                os.remove("authimg.jpg")
                user_ref.update({u'FaceVerified' : FR_Verification})
                return str(FR_Verification)
            else:
                os.remove("authimg.jpg")
            
        user_ref.update({u'FaceVerified' : FR_Verification})
        os.remove("dpimg.jpg")
        return str(FR_Verification)
    except Exception as e:
        # user_ref.update({u'FaceVerified' : False})
        return str(e)


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    # server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=port, host='0.0.0.0')
    # app.run(host='0.0.0.0')
