# https://pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
# an averaged background solution
# import the necessary packages
import datetime
# import imutils
import cv2
import time

# conf 
delta_thresh = 5
min_area = 1000
min_motion_frames = 8
min_upload_seconds = 3.0
show_video = True

client = None

# uploaded timestamp, and frame motion counter
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
frame_number = -1
motion_frame_numbers = []

# run from video dir
video = cv2.VideoCapture("2024-02-04_footage.mp4")
status = True

while True:
	status, frame = video.read()
	frame_number += 1
	if not status:
		break
	
	timestamp = datetime.datetime.now()
	text = "Unoccupied"
	# convert frame to grayscale, and blur it
	# frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# if the average frame is None, initialize it
	if avg is None:
		print("[INFO] starting background model...")
		avg = gray.copy().astype("float")
		# rawCapture.truncate(0)
		continue
	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
	
    # threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
	thresh = cv2.threshold(frameDelta, delta_thresh, 255,
		cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	
	cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	# cnts = imutils.grab_contours(cnts)
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < min_area:
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
		text = "Occupied"
	
		
		
	# draw the text and timestamp on the frame
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	# check to see if the room is occupied
	if text == "Occupied":
		motion_frame_numbers.append(frame_number)
		# check to see if enough time has passed between uploads
		if (timestamp - lastUploaded).seconds >= min_upload_seconds:
			# increment the motion counter
			motionCounter += 1
			# check to see if the number of frames with consistent motion is
			# high enough
			if motionCounter >= min_motion_frames:
				print('confident motion is detected.')
				# update the last uploaded timestamp and reset the motion
				# counter
				lastUploaded = timestamp
				motionCounter = 0
	# otherwise, the room is not occupied
	else:
		motionCounter = 0
		
	# check to see if the frames should be displayed to screen
	if show_video:
		# display the security feed
		cv2.imshow("Feed", frame) # this won't work when ssh'd into pi
		time.sleep(0.07)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
	# clear the stream in preparation for the next frame
	# rawCapture.truncate(0)

print("Frames with motion detected:", motion_frame_numbers)
