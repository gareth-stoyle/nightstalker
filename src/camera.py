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
        