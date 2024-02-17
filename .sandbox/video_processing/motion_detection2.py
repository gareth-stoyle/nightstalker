# https://pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
# an averaged background solution
# import the necessary packages
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import time

def detect_motion(frame, min_area, delta_thresh, show_video, avg):
	detected = False
	# convert frame to grayscale, and blur it
	# frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# if the average frame is None, initialize it
	if avg is None:
		print("[INFO] starting background model...")
		avg = gray.copy().astype("float")
		# rawCapture.truncate(0)
		return (False, avg)
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

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < min_area:
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
		detected = True

	# draw the text and timestamp on the frame
	# ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	# cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	# 	0.35, (0, 0, 255), 1)
		
	if show_video:
		# display the security feed
		cv2.imshow("Feed", frame) # this won't work when ssh'd into pi
		time.sleep(0.07)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			exit()
	# clear the stream in preparation for the next frame
	# rawCapture.truncate(0)
		
	return (detected, avg)

def trim_video(input_video, output_video, duration_to_trim):
    # Load the video clip
    clip = VideoFileClip(input_video)
    # Calculate the duration to keep
    duration_to_keep = clip.duration - duration_to_trim
    # Trim the video
    trimmed_clip = clip.subclip(0, duration_to_keep)
    # Write the trimmed video to a file
    trimmed_clip.write_videofile(output_video, codec="libx264")
    
    # Close the video clip
    clip.close()


# motion detection config
delta_thresh = 5
min_area = 1000
show_video = False
avg = None
# clip saving algo config
motion_length = 0
no_motion = 0
min_motion_frames = 4
min_clip_gap = 8*60 # 60s of no motion is enough to end clip and reset things
frame_number = -1
motion_frame_numbers = []
writing_clip = False
clip_count = 0


# run from video dir
video = cv2.VideoCapture("full-2024-01-21_footage.mp4")

# make from here down a function
# Define the codec
fourcc = cv2.VideoWriter_fourcc(*'avc1')
# get video details
fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
status = True

while True:
	status, frame = video.read()
	frame_number += 1
	if frame_number <= (fps*(60*10)):
		continue # skip first 10 mins...
	if frame_number >= total_frames - (fps*(60*10)):
		break # step when 10 mins left
	print(f'\n\n ### process frame {frame_number} ###\n')
	if not status: # no more frames to parse
		break
	
	detected, avg = detect_motion(frame, min_area, delta_thresh, show_video, avg)		

	# functionality to handle clip creation for separate motion incidents
	if detected:
		motion_length += 1 # increment frames with motion
		no_motion = 0 # reset frames with no motion
		# we should be recording clip
		if not writing_clip and motion_length >= min_motion_frames:
			clip_count += 1
			print('motion exceed min_motion_frames and not yet writing, starting writing process')
			writing_clip = True			
			output_video = cv2.VideoWriter(f'full_night_output_video_{clip_count}-untrimmed.mp4', fourcc, fps, (frame_width, frame_height))
			# write frames to video as well as previous x frames
		elif writing_clip:
			output_video.write(frame)  # Write the frame to the output video
		motion_frame_numbers.append(frame_number)
	else:
		motion_length = 0 # reset frames with motion
		no_motion += 1 # increment frames of no motion
		if writing_clip and no_motion >= min_clip_gap: # no motion for over 60s, end clip (and shave 30s worth of frames)
			print('we are writing but no_motion exceeds the min gap between clips, stop writing')
			output_video.release() # stop writing
			# trim end of clip
			seconds_to_shave = (min_clip_gap * 0.75) // 8  # get rid of 75% of those last no motion frames
			print(f'shaving {seconds_to_shave} off video.')
			trim_video(f'full_night_output_video_{clip_count}-untrimmed.mp4', f'full_night_output_video_{clip_count}.mp4', seconds_to_shave)
			print('video trimmed.')
			writing_clip = False
		elif writing_clip: # continue writing
			print("we are writing and haven't met the threshold to stop writing")
			output_video.write(frame)  # Write the frame to the output video
		else:
			print('no motion detected and we are not writing, continue')


	print(f'motion length: {motion_length}')
	print(f'writing clip: {writing_clip}')
	print(f'no motion detected for: {no_motion} frames')
		

print("Frames with motion detected:", motion_frame_numbers)
