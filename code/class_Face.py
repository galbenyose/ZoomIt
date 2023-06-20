import cv2
import dlib
import os

class Face:
    def __init__(self,image):
        self.image=image

    
    #אמירת שקר לחץ
    # כשאנחנו בלחץ נאגר לנו דם באף ונוצר לחץ במקום זה מה שיוצר את הרצון לגעת באף
    def Thouching_the_nose(self):
        predictor = dlib.shape_predictor('code/shape_model/shape_predictor_68_face_landmarks.dat')
        image_thouching_nose_check=cv2.imread(self.image)
        gray = cv2.cvtColor(image_thouching_nose_check, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        # Iterate over the detected faces
        for face in faces:
    # Detect the facial landmarks for the face
            landmarks = predictor(gray, face)
    
    # Get the coordinates of the nose
            nose = landmarks.part(34)  
            top_lip = landmarks.part(51)  
            lower_lip = landmarks.part(58) 
    # מרחק בפיקסלים על פי נקודות המצפן
            minimum_distance = 10    
    
    # Check if the top lip or bottom lip is close to the nose
    #מגע של היד באף תקרב את נקודות המצפן של השפה העליונה או התחתונה לאף ולכן נבדוק את המרחק 
            if abs(top_lip.y - nose.y) <  minimum_distance  or abs(lower_lip.y - nose.y) <  minimum_distance :
                print("thouching the nose")
                return True
        
            else:
               print("isnt thouching the nose") 
               return False


    
    def Thouching_the_mouth(self):
        # כיסוי הפה במהלך אמירת תשובה עלול להעיד על שקר חרטה הסתרה או בושה
        predictor = dlib.shape_predictor('shape_model/shape_predictor_68_face_landmarks.dat.bz2')
        image_thouching_nose_check=cv2.imread(self.image)
        gray = cv2.cvtColor(image_thouching_nose_check, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        # Iterate over the detected faces
        for face in faces:
    # Detect the facial landmarks for the face
            landmarks = predictor(gray, face)
            top_lip= landmarks.part(51)
            lower_lip = landmarks.part(58)
            chin =landmarks.part(9)
            minimum_distance = 10  
            
            if abs(top_lip.y-chin.y)<minimum_distance or abs(lower_lip.y-chin.y)<minimum_distance:
                print("thouching the mouth")
                return True
            else:
                print("isnt thouching the mouth")
                return False
            
    
    def Thouching_the_ear(self):
        #חוסר נוחות
        predictor = dlib.shape_predictor('shape_model/shape_predictor_68_face_landmarks.dat.bz2')
        image_thouching_nose_check=cv2.imread(self.image)
        gray = cv2.cvtColor(image_thouching_nose_check, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        # Iterate over the detected faces
        for face in faces:
    # Detect the facial landmarks for the face
            landmarks = predictor(gray, face)
            right_ear=landmarks.part(1)
            left_ear = landmarks.part(17)
            chin_right = landmarks.part(10)
            chin_left = landmarks.part(8)
            minimum_distance = 10  
            if abs(right_ear-chin_right)<minimum_distance or abs(left_ear-chin_left)<minimum_distance:
                print("thouching the ear")
                return True
            else:
                print("not thouching the ear")
                return False
                
            
    
    def Thouching_the_forehead(self):
         # הנחת יד על המצח- חשיבה/ הרגשת תסכול או יאוש
        predictor = dlib.shape_predictor('shape_model/shape_predictor_68_face_landmarks.dat.bz2')
        image_thouching_nose_check=cv2.imread(self.image)
        gray = cv2.cvtColor(image_thouching_nose_check, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        # Iterate over the detected faces
        for face in faces:
    # Detect the facial landmarks for the face
            landmarks = predictor(gray, face)
            left_eyebrow= landmarks.part(22)
            right_eyebrow =landmarks.part(23)
            minimum_distance = 5
            
            if abs(right_eyebrow.x-left_eyebrow.x)<minimum_distance:
                print("thouching the forehead")
                return True
            else:
                print("not thouching the forehead")
                return False
            
    
    def mouth_clenched(self):
    # קיווץ הפה לכיוון אחד חוסר שיבעות רצון
        predictor = dlib.shape_predictor('shape_model/shape_predictor_68_face_landmarks.dat.bz2')
        image_thouching_nose_check=cv2.imread(self.image)
        gray = cv2.cvtColor(image_thouching_nose_check, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        # Iterate over the detected faces
        for face in faces:
    # Detect the facial landmarks for the face
            landmarks = predictor(gray, face)
            top_lip= landmarks.part(51)
            lower_lip = landmarks.part(58)
            minimum_distance = 2
            if abs(top_lip.y-lower_lip.y)<minimum_distance:
                print("pursing the lips")
                return True
            else:
                print("not pursing the lips")
                return False
            