import camera
import video_processing
import motion_algorithm
import db
import sensors

import datetime
import os
import time

#
# get file and path details
#

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_directory = os.getcwd()
path = os.path.abspath(os.path.join(current_directory, 'app', 'static', 'videos'))
video_file = f"unprocessed-{current_date}_footage.h264"
full_video_path = path + '/' + video_file
clips_output_path = path + '/' + f'{current_date}_footage.mp4'

#
# Setup Camera
#

framerate = 8
resolution = '640x360'
camera = camera.Camera(framerate, resolution, flip=False)

#
# Video recording
#

camera.start_recording(path, video_file)
start_time = datetime.datetime.now().strftime('%H:%M:%S')

print(f"Recording video to {video_file} in the path: {path}.\nPress 'q' and Enter to stop.")

#
# Sensor logging
#

motion_sensor = sensors.MotionSensor(motion_pin=22)
dht_sensor = sensors.DHTSensor(dht_pin=18)

try:
    dht_sensor.start_recording()
    motion_sensor.start_recording()
except Exception as e:
    print(e)

#
# Handle end of recording/logging.
# This includes performing motion detection
#

try:
    user_input = input()
    while user_input.lower() != 'q':
        user_input = input()
    print('Exiting while loop...')
except Exception as e:
    print('[EXCEPTION]', e)
finally:
    print('Ending sensor logging...')
    dht_sensor.stop_recording()
    motion_sensor.stop_recording()

    print('Ending recording sessions...')
    camera.stop_recording()
    end_time = datetime.datetime.now().strftime('%H:%M:%S')
    time.sleep(0.1) # just in case there is a delay in finishing file writing

    conversion_status, mp4_path = video_processing.convert_h264_to_mp4(path, video_file, framerate)
    # Delete h264
    if conversion_status:
        video_processing.delete_file(full_video_path)
    db.insert_video_entry(current_date, start_time, end_time)
    print(f'Recording successfully captured in {mp4_path}')

    print('Getting motion detected clips')
    motion_merged = motion_algorithm.trim_video_by_motion(mp4_path, clips_output_path, current_date, start_time)
    if motion_merged:
        print(f"Clips successfully merged to {clips_output_path}")
    else:
        print("Problem in motion detection functionality!")
