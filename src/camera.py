import picamera

##################################
##### PICAMERA FUNCTIONALITY #####
##################################

class Camera:
    """Simple class to initialise the camera with user submitted settings"""
    def __init__(self, framerate=24, resolution='720x480', flip=True):
        self.camera = picamera.PiCamera()
        self.camera.framerate = framerate
        self.camera.resolution = resolution
        if flip:
            self.camera.rotation = 180
        
    def start_recording(self, path, video_file):
        output = path + '/' + video_file
        self.camera.start_recording(output)

    def stop_recording(self):
        self.camera.stop_recording()
        