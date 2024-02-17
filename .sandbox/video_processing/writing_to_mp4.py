import cv2

# run from video dir
video = cv2.VideoCapture("2024-02-04_footage.mp4")
video.set(3,640)
video.set(4,480)
# Get video properties
fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

status = True
count = 0
writing = False

while True:
    count += 1
    status, frame = video.read()
    if not status: # no more frames to parse
        break

    if not writing and count >= 50 and count <= 150:
        # Define the codec
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        output_video = cv2.VideoWriter('TEST_output_video.mp4', fourcc, fps, (frame_width, frame_height))
        # write frames to video as well as previous x frames
        writing = True
        output_video.write(frame)  # Write the frame to the output video

    if writing:
        output_video.write(frame)

    if count >= 150:
        print('releasing')
        output_video.release() # stop writing
        video.release()
        break