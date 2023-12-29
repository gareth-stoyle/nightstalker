import subprocess

def convert_h264_to_mp4(file_h264, file_mp4, framerate='25'):
    command = ["MP4Box", "-add", file_h264, "-fps", framerate, file_mp4]

    try:
        subprocess.run(command, check=True)
        print("Conversion successful")
        return True
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
        return False

