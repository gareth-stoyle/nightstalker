import unittest
import os
import time
from camera import Camera

class TestCamera(unittest.TestCase):
    def setUp(self):
        # Create a test directory
        self.test_dir = 'test_videos'
        os.makedirs(self.test_dir, exist_ok=True)
        self.camera = Camera(framerate=10, resolution='640x480', bitrate=500000, quality=40, colour_effects=None, flip=False)
        
    def tearDown(self):
        # Remove the test directory and its contents
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)
        self.camera.camera.close()

    def test_camera_initialisation(self):
        self.assertEqual(self.camera.camera.framerate, 10)
        self.assertNotEqual(self.camera.camera.framerate, 20)
        self.assertEqual(self.camera.camera.resolution, (640, 480))
        self.assertNotEqual(self.camera.camera.resolution, (1920, 1080))
        self.assertEqual(self.camera.bitrate, 500000)
        self.assertNotEqual(self.camera.bitrate, 1000000)
        self.assertEqual(self.camera.quality, 40)
        self.assertNotEqual(self.camera.quality, 50)
        self.assertIsNone(self.camera.camera.color_effects)
        self.camera.camera.color_effects = (128, 128)
        self.assertIsNotNone(self.camera.camera.color_effects)

    
    def test_camera_recording(self):
        # Start recording
        video_file = 'test_video.h264'
        
        self.assertFalse(self.camera.camera.recording)
        self.camera.start_recording(self.test_dir, video_file)
        self.assertTrue(self.camera.camera.recording)
        
        time.sleep(1)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, video_file)))
        
        self.camera.stop_recording()
        self.assertFalse(self.camera.camera.recording)
        
        video_path = os.path.join(self.test_dir, video_file)
        self.assertGreater(os.path.getsize(video_path), 0)
        
        self.camera.start_recording(self.test_dir, video_file)
        time.sleep(1)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, video_file)))
        
        self.camera.stop_recording()
        self.assertFalse(self.camera.camera.recording)

        

        
        
if __name__ == '__main__':
    unittest.main()
