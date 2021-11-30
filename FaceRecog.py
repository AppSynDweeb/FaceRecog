import face_recognition as fr

def SelfieAuth(auth_image, new_image):
    user_given_image = fr.load_image_file(auth_image)
    user_selfie_image = fr.load_image_file(new_image)

    try:
        user_encoding = fr.face_encodings(user_given_image)[0]
        selfie_encoding = fr.face_encodings(user_selfie_image)[0]
    except:
        return False

    result = fr.compare_faces([user_encoding], selfie_encoding)
    # ShowPic(new_image)
    return result
