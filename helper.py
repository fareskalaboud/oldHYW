import cv2
import mediapipe as mp
camera = cv2.VideoCapture(2)

pose_parts = ["nose", "L_eye_IN", "L_eye", "L_eye_OUT", "R_eye_IN", "R_eye", "R_eye_OUT", "L_ear", "R_ear", "L_mouth", "R_mouth", "L_shoulder", "R_shoulder", "L_elbow", "R_elbow",
              "L_wrist", "R_wrist", "L_pinky", "R_pinky", "L_index", "R_index", "L_thumb", "R_thumb", "L_hip", "R_hip", "L_knee", "R_knee", "L_ankle", "R_ankle", "L_heel", "R_heel", "L_foot", "R_foot"]

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()


def gen_frames():
    while True:
        success, img = camera.read()  # read the camera frame

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks,
                                  mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if(id == 11 or id == 12 or id == 13 or id == 14 or id == 23 or id == 24):
                    h, w, c = img.shape
                    print(h, w, pose_parts[id], lm.x, lm.y)   

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img[0:720,260:980])
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # concat frame one by one and show result
