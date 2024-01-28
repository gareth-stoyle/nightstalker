import camera
import video_processing
import datetime
import os
import time

#
# get file and path details
#

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_directory = os.getcwd()
path = os.path.abspath(os.path.join(current_directory, 'app', 'static', 'videos'))
video_file = f"{current_date}_footage.h264"
full_video_path = path + '/' + video_file

#
# Setup Camera
#

framerate = 10
resolution = '720x480'
camera = camera.Camera(framerate, resolution, flip=True)
camera.start_recording(path, video_file)

print(f"Recording video to {video_file} in the path: {path}. Press 'q' and Enter to stop.")

#
# Video recording
#

try:
    user_input = input()
    while user_input.lower() != 'q':
        user_input = input()
    print('Exiting while loop...')
except Exception as e:
    print('[EXCEPTION]', e)
finally:
    print('Ending recording sessions...')
    camera.stop_recording()
    time.sleep(0.1) # just in case there is a delay in finishing file writing
    # h264 to mp4 conversion
    conversion = video_processing.convert_h264_to_mp4(path, video_file, framerate)
    # Delete h264 - don't do this step while developing.
    # if conversion:
    #     video_processing.delete_file(full_video_path)
    print(f'Recording successfully captured in {path}')
