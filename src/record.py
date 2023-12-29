import camera
import datetime
import os

# set the output path
current_directory = os.getcwd()
path = os.path.abspath(os.path.join(current_directory, 'app', 'static', 'videos'))

# set the file name
current_date = datetime.datetime.now().strftime("%Y%m%d")
video_file = f"{current_date}_footage.h264"

# setup camera with appropriate config
framerate = 10
resolution = '720x480'
camera = camera.Camera(framerate, resolution)
camera.start_recording(path, video_file)

print(f"Recording video to {video_file} in the path: {path}. Press 'q' and Enter to stop.")

# end recording on q input or any kind of exception
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

print(f'Recording successfully captured in {path}/{video_file}')