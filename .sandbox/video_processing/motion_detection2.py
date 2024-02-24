# https://pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
# an averaged background solution
# import the necessary packages
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from progressbar import progressbar
import time
import os

def detect_motion(frame, min_area, delta_thresh, show_video, avg):
	detected = False
	# convert frame to grayscale, and blur it
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
    os.remove(input_video) # use video_processing file deletion when ready.

def trim_video_by_motion(video_path):
	# motion detection config
	delta_thresh = 5
	min_area = 4000
	show_video = False
	avg = None

	# clip saving algo config
	motion_length = 0
	no_motion = 0
	min_motion_frames = 8
	min_clip_gap = 8*60 # 60s of no motion is enough to end clip and reset things
	writing_clip = False
	clip_count = 0

	# run from video dir
	video = cv2.VideoCapture(video_path)

	# make from here down a function
	# Define the codec
	fourcc = cv2.VideoWriter_fourcc(*'avc1')
	# get video details
	fps = video.get(cv2.CAP_PROP_FPS)
	total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	frames_for_iteration = int(total_frames - (fps*(60*10))) # skip last 10 mins for footage
	frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
	start = time.time()

	for i in progressbar(range(frames_for_iteration)):
		if i <= (fps*(60*10)):
			continue # skip first 10 mins...

		status, frame = video.read()
		detected, avg = detect_motion(frame, min_area, delta_thresh, show_video, avg)		

		# functionality to handle clip creation for separate motion incidents
		if detected:
			motion_length += 1 # increment frames with motion
			no_motion = 0 # reset frames with no motion
			# we should be recording clip
			if not writing_clip and motion_length >= min_motion_frames:
				clip_count += 1
				writing_clip = True			
				output_video = cv2.VideoWriter(f'full_night_output_video_{clip_count}-untrimmed.mp4', fourcc, fps, (frame_width, frame_height))
				# write frames to video as well as previous x frames
			elif writing_clip:
				output_video.write(frame)  # Write the frame to the output video
		else:
			motion_length = 0 # reset frames with motion
			no_motion += 1 # increment frames of no motion
			if writing_clip and no_motion >= min_clip_gap: # no motion for over 60s, end clip (and shave 30s worth of frames)
				output_video.release() # stop writing
				# trim end of clip
				seconds_to_shave = (min_clip_gap * 0.75) // 8  # get rid of 75% of those last no motion frames
				trim_video(f'full_night_output_video_{clip_count}-untrimmed.mp4', f'full_night_output_video_{clip_count}.mp4', seconds_to_shave)
				print('video trimmed.')
				writing_clip = False
			elif writing_clip: # continue writing
				output_video.write(frame)  # Write the frame to the output video
		
	# end writing in case last frame was being written
	if writing_clip:
		writing_clip = False
		output_video.release()

	end = (time.time() - start) // 60
	print(f'{total_frames} frames processed in {end} minutes.')
