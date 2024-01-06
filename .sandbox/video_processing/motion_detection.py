import cv2
import time

# run from video dir
video = cv2.VideoCapture("sleep_test1.mp4")
background = None
motion_frame_numbers = []

frame_number = 0
status = True

while status:
    status, frame = video.read()

    if not status:
        break
    
    if background is None:
        background = frame
        background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (21, 21), 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    diff = cv2.absdiff(background, gray)

    threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    cnts, _ = cv2.findContours(threshold.copy(),
                               cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        motion_detected = True

    if motion_detected:
        motion_frame_numbers.append(frame_number)

    cv2.imshow("All contours", frame) # this won't work ssh'd into a pi
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
    time.sleep(0.08)
    frame_number += 1
    # print(frame_number)


# video.release()
# cv2.destroyAllWindows()

print("Frames with motion detected:", motion_frame_numbers)
