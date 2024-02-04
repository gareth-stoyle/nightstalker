import picamera

##################################
##### PICAMERA FUNCTIONALITY #####
##################################

class Camera:
    """Simple class to initialise the camera with user submitted settings"""
    def __init__(self, framerate=24, resolution='720x480', bitrate=300000, quality=30, colour_effects=(128,128), flip=True):
        self.camera = picamera.PiCamera()
        self.camera.framerate = framerate
        self.camera.resolution = resolution
        self.bitrate = bitrate
        self.quality = quality
        self.camera.color_effects = colour_effects
        if flip:
            self.camera.rotation = 180
        
    def start_recording(self, path, video_file):
        output = path + '/' + video_file
        self.camera.start_recording(output, bitrate=self.bitrate, quality=self.quality)

    def stop_recording(self):
        self.camera.stop_recording()
        