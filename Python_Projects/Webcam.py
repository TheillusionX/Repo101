import cv2, time, pandas
from datetime import datetime

time.sleep(1)
first_frame = None
video = cv2.VideoCapture(0)
prev_frame_moving = False
current_frame_moving = False
time = []
data = pandas.DataFrame(columns = ["Start", "End"])
i = 0

while True:
    check, frame = video.read()
    graymage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    graymage = cv2.GaussianBlur(graymage, (21, 21), 0)
    if first_frame is None:
        first_frame = graymagepip install kivy.deps.glew
        continue
    delta = cv2.absdiff(first_frame, graymage)
    threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations = 5)

    (cnts,_) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            current_frame_moving = False
            continue
        else:
            current_frame_moving = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
    if current_frame_moving != prev_frame_moving:
        if current_frame_moving:
            time.append(str(datetime.now()))
        else:
            time.append(str(datetime.now()))

    i += 1
    if i % 60 == 0:
        first_frame = graymage
        i = 1

    prev_frame_moving = current_frame_moving

    cv2.imshow("Delta Video", delta)
    cv2.imshow("Threshold Video", threshold)
    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(15)
    if key == ord("z"):
        break

if prev_frame_moving:
    time.append(str(datetime.now()))
video.release()
cv2.destroyAllWindows()

start_times = []
end_times = []

for t in time:
    if time.index(t) % 2 == 0:
        start_times.append(t)
    else:
        end_times.append(t)

data["Start"] = start_times
data["End"] = end_times

data.to_csv("TimesOfMotion.csv")
