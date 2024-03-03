import cv2

# run from video dir
video = cv2.VideoCapture("2024-02-04_footage.mp4")
# Get video properties
fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Define the codec
fourcc = cv2.VideoWriter_fourcc(*'avc1')
output_video = cv2.VideoWriter('TEST_output_video.mp4', fourcc, fps, (frame_width, frame_height))
status = True

while True:
    status, frame = video.read()
    if not status: # no more frames to parse
        output_video.release() # stop writing
        video.release()
        break

    output_video.write(frame)  # Write the frame to the output video