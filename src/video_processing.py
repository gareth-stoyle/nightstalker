import subprocess
import os

def convert_h264_to_mp4(path, video_file, framerate='25'):
    '''convert a h264 file to mp4 using MP4Box'''
    print('### Converting file to mp4 ###')
    h264_path = path + '/' + video_file
    # Extract the file name (without extension) from the input path
    video_basename = os.path.splitext(os.path.basename(h264_path))[0]
    
    # Create the output file path with the .mp4 extension
    mp4_path = os.path.join(path, f"{video_basename}.mp4")
    command = ["MP4Box", "-add", h264_path, "-fps", framerate, mp4_path]
    print(command)
    try:
        subprocess.run(command, check=True)
        print("Conversion successful")
        return True
    except Exception as e:
        print("Error during conversion:", e)
        return False

def delete_file(file_path):
    '''Delete a file given entire path'''
    print('Deleting h264 file.')
    try:
        os.remove(file_path)
        print(f"File deleted successfully: {file_path}")
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except PermissionError:
        print(f"Error: Permission denied - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

import os

def find_video(date):
    '''return the full path to a video given the path and date'''
    current_directory = os.getcwd()
    path = os.path.abspath(os.path.join(current_directory, 'static', 'videos'))
    video_file = f"{date}_footage.mp4"
    full_video_path = os.path.join(path, video_file)
    if os.path.exists(full_video_path):
        print(f"Video found at: {full_video_path}")
        return video_file
    else:
        print(f"The video file '{video_file}' does not exist.")
        return None

def set_video_info(video_file, start, end, length, fps, resolution):
    '''set video metadata such as start and end time in JSON DB'''
    pass

def retrieve_video_info(video_file):
    '''return video metadata such as start and end time from JSON DB'''
    pass