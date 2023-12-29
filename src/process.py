import subprocess
import cv2

file_h264 = '20231229_footage.h264'
file_mp4 = 'fixed-fps-20231229_footage.mp4'

def convert_h264_to_mp4(file_h264, file_mp4, framerate='25'):
    command = ["MP4Box", "-add", file_h264, "-fps", framerate, file_mp4]

    try:
        subprocess.run(command, check=True)
        print("Conversion successful")
        return True
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
        return False

def count_frames(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not video.isOpened():
        print("Error: Could not open video file")
        return

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    total_fps = int(video.get(cv2.CAP_PROP_FPS))

    # Release the video capture object
    video.release()

    return (total_frames, total_fps)


convert_h264_to_mp4(file_h264, file_mp4, framerate='10')

num_frames = count_frames(file_h264)
print(f"The video has {num_frames} frames.")
num_frames = count_frames(file_mp4)
print(f"The video has {num_frames} frames.")