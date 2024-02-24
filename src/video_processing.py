from moviepy.editor import VideoFileClip
import subprocess
import os

def trim_video(input_video, output_video, duration_to_trim):
    '''Cuts a predefined duration off of a video'''
    # Load the video clip
    clip = VideoFileClip(input_video)
    # Calculate the duration to keep
    duration_to_keep = clip.duration - duration_to_trim
    # Trim the video
    trimmed_clip = clip.subclip(0, duration_to_keep)
    # Write the trimmed video to a file
    trimmed_clip.write_videofile(output_video, codec="libx264")
    
    # Close the video clip
    clip.close()
    delete_file(input_video) # use video_processing file deletion when ready.

def convert_h264_to_mp4(path, video_file, framerate='25'):
    '''convert a h264 file to mp4 using MP4Box'''
    print('\n### Converting file to mp4 ###\n')
    h264_path = path + '/' + video_file
    # Extract the file name (without extension) from the input path
    video_basename = os.path.splitext(os.path.basename(h264_path))[0]
    
    # Create the output file path with the .mp4 extension
    mp4_path = os.path.join(path, f"{video_basename}.mp4")
    command = ["MP4Box", "-add", h264_path, "-fps", str(framerate), mp4_path]
    try:
        subprocess.run(command, check=True)
        print("Conversion successful")
        return [True, mp4_path]
    except Exception as e:
        print("Error during conversion:", e)
        return [False, mp4_path]

def delete_file(file_path):
    '''Delete a file given entire path'''
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except PermissionError:
        print(f"Error: Permission denied - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def find_video(date):
    '''return the full path to a video given the path and date'''
    current_directory = os.getcwd()
    path = os.path.abspath(os.path.join(current_directory, 'app', 'static', 'videos'))
    video_file = f"{date}_footage.mp4"
    full_video_path = os.path.join(path, video_file)
    if os.path.exists(full_video_path):
        print(f"Video found at: {full_video_path}")
        return video_file
    else:
        print(f"The video file '{video_file}' does not exist.")
        return None
