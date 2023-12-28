#
# Discontinued RPi5 picamera2 stuff because it needs camera adapter, using Rpi3 again.
#

# ## Installation

# Tested on Raspberry Pi 5 64bit Debian bookworm

# install necessary packages:

# sudo apt update
# sudo apt upgrade
# sudo apt install -y python3-libcamera python3-kms++ libcap-dev
# sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip

# Enter into virtual environment:

# python -m venv --system-site-packages .venv # needed to prevent libcamera importing issue.
# pip3 install -r requirements.txt

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder


class Camera:
    def __init__(self, framerate=30, resolution=(720, 480)):
        self.camera = Picamera2()
        config = self.camera.video_configuration()
        self.camera.configure(config)
        self.camera.video_configuration.controls.FrameRate = framerate
        self.camera.video_configuration.size = resolution
        encoder = H264Encoder(10000000)

        
    def start_recording(self, path, video_file):
        output = path + video_file
        # self.camera.start_recording(self.encoder, output)

    def stop_recording(self):
        pass
        # self.camera.stop_recording()
        


camera = Camera()
