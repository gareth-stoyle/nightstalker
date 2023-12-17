import picamera

class Camera:
    def __init__(self, framerate=30, resolution='720x480'):
        self.camera = picamera.PiCamera()
        self.camera.framerate = framerate
        self.camera.resolution = resolution
        
    def start_recording(self, path, video_file):
        output = path + video_file
        self.camera.start_recording(output)

    def stop_recording(self):
        self.camera.stop_recording()
        

framerate = 15
resolution = '720x480'
camera = Camera(framerate, resolution)
video_file = "framerate_test_video.h264"
path = '/home/gareth/Desktop/nightstalker/test_scripts/'

camera.start_recording(path, video_file)
print(f"Recording video to {video_file}. Press 'q' and Enter to stop.")
try:
    user_input = input()
    while user_input.lower() != 'q':
        user_input = input()
except KeyboardInterrupt:
    pass
finally:
    camera.stop_recording()



print("Script completed.")