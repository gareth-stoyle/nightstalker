import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
from progressbar import progressbar
import os
import math

import video_processing
import db


def trim_video_by_motion(video_path, output_path, date, start_time):
    '''
    Takes a full length video file and converts into 
    one video compiled of clips where motion is detected
    '''
    if not os.path.exists(video_path):
        print(f"The video file '{video_path}' does not exist.")
        return False
    
    video = cv2.VideoCapture(video_path)
    config = get_config(video)
    
    # skip first x mins
    video.set(cv2.CAP_PROP_POS_FRAMES, config['frames_to_skip'])

    ready_clips = []
    writing_clip = False
    avg = None
    clip_count, motion_length, no_motion = 0, 0, 0

    for i in progressbar(range(config['frames_to_skip'], config['frames_for_iteration']), redirect_stdout=True):
        status, frame = video.read()
        detected, avg = detect_motion(frame, config['min_area'], config['delta_thresh'], avg)		

        # functionality to handle clip creation for separate motion incidents
        if detected:
            motion_length += 1 # increment frames with motion
            no_motion = 0 # reset frames with no motion
            if not writing_clip and motion_length < config['min_motion_frames']:
                continue
            
            # we know we are going to write this frame
            frame = add_timestamp(frame, start_time, config['fps'], i, config['font'], config['font_scale'], config['font_color'], config['font_thickness'])

            if writing_clip:
                output_video.write(frame)  # Write the frame to the output video
            else: # lets start writing
                clip_count += 1
                clip_start_time = calculate_timestamp(start_time, config['fps'], i)
                writing_clip = True	
                input_clip_path = f'app/static/videos/full_night_output_video_{clip_count}-untrimmed.mp4'
                output_video = cv2.VideoWriter(input_clip_path, config['fourcc'], config['fps'], (config['frame_width'], config['frame_height']))
                output_video.write(frame)
                # write frames to video as well as previous x frames
        else:
            motion_length = 0 # reset frames with motion
            no_motion += 1 # increment frames of no motion
            if writing_clip and no_motion >= config['min_clip_gap']: # no motion, end clip (and shave frames)
                output_video.release() # stop writing
                # trim end of clip
                trimmed_clip_path = f'app/static/videos/full_night_output_video_{clip_count}.mp4'
                video_processing.trim_video(input_clip_path, trimmed_clip_path, config['frames_to_shave'] / config['fps'])
                ready_clips.append(trimmed_clip_path)
                clip_end_time = calculate_timestamp(start_time, config['fps'], i-config['frames_to_shave'])
                db.insert_clip_entry(date, clip_count, clip_start_time, clip_end_time)
                writing_clip = False
            elif writing_clip: # continue writing
                frame = add_timestamp(frame, start_time, config['fps'], i, config['font'], config['font_scale'], config['font_color'], config['font_thickness'])
                output_video.write(frame)  # Write the frame to the output video
        
    # end writing in case last frame was being written
    if writing_clip:
        writing_clip = False
        output_video.release()
        trimmed_clip_path = f'app/static/videos/full_night_output_video_{clip_count}.mp4'
        video_processing.trim_video(input_clip_path, trimmed_clip_path, 1)
        ready_clips.append(trimmed_clip_path)
        clip_end_time = calculate_timestamp(start_time, config['fps'], i - config['fps'])
        db.insert_clip_entry(date, clip_count, clip_start_time, clip_end_time)

    try:
        merge_video_clips(ready_clips, output_path)
    except ValueError as e:
        print(f'Error, likely no motion detected: {e}')
        return False
    return True

def merge_video_clips(input_paths, output_path):
    video_clips = [VideoFileClip(path) for path in input_paths]
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(output_path)

    # finish by deleting clips
    for clip in input_paths:
        video_processing.delete_file(clip)
      
def detect_motion(frame, min_area, delta_thresh, avg):
    '''Determines if motion was detected based on config variables'''
    detected = False
    # convert frame to grayscale, and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the average frame is None, initialize it
    if avg is None:
        avg = gray.copy().astype("float")
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
        
    return (detected, avg)

def add_timestamp(frame, start_time, fps, frame_number, font, font_scale, font_color, font_thickness):
    ts = calculate_timestamp(start_time, fps, frame_number)
    text_size = cv2.getTextSize(ts, font, font_scale, font_thickness)[0]
    text_position = (10, text_size[1] + 10)
    cv2.putText(frame, ts, text_position, font, font_scale, font_color, font_thickness)
    return frame

def calculate_timestamp(start_time, fps, frame_number):
    '''Calculate the timestamp to put on a frame'''
    start_hour, start_minute, start_second = map(int, start_time.split(':'))
    start_seconds = start_hour * 3600 + start_minute * 60 + start_second
    elapsed_seconds = frame_number / fps
    total_seconds = math.ceil(start_seconds + elapsed_seconds)
    total_seconds %= 86400  # Ensure it's within a 24-hour period
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_config(video):
    '''Return configuration variables in dictionary format'''
    config = {}
    
    # get video details
    config['fourcc'] = cv2.VideoWriter_fourcc(*'avc1')
    config['fps'] = video.get(cv2.CAP_PROP_FPS)
    config['total_frames'] = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    config['frames_to_skip'] = int(config['fps']*60*15) # skip first x mins
    config['frames_for_iteration'] = int(config['total_frames'] - config['frames_to_skip']) # skip last x mins for footage
    config['frame_width'] = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    config['frame_height'] = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # motion detection config
    config['delta_thresh'] = 5
    config['min_area'] = 4000

    # clip saving algo config
    config['min_motion_frames'] = 4
    config['min_clip_gap'] = config['fps']*30 # no motion enough to end clip and reset things
    config['frames_to_shave'] = (config['min_clip_gap'] * 0.75)  # get rid of 75% of those last no motion frames

    # drawing timestamp on frame
    config['font_scale'] = 1  # Increase this value for bigger text
    config['font_color'] = (255, 255, 255)  # White color
    config['font_thickness'] = 2  # Thickness of the text
    config['font'] = cv2.FONT_HERSHEY_SIMPLEX

    return config


if __name__ == "__main__":
    mp4_path = '/home/gareth/Desktop/nightstalker/app/static/videos/unprocessed-2024-03-12_footage.mp4'
    clips_output_path = '/home/gareth/Desktop/nightstalker/app/static/videos/2024-03-12_footage.mp4'
    current_date = "2024-03-12"
    start_time = "00:13:56"
    print('Getting motion detected clips')
    motion_merged = trim_video_by_motion(mp4_path, clips_output_path, current_date, start_time)
    if motion_merged:
        print(f"Clips successfully merged to {clips_output_path}")
    else:
        print("Problem in motion detection functionality!")
