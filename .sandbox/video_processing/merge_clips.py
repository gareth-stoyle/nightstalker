from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_video_clips(input_paths, output_path):
    video_clips = [VideoFileClip(path) for path in input_paths]
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(output_path)
    print("Merge successful!")

# Example usage
input_paths = ["app/static/videos/full_night_output_video_1.mp4", "app/static/videos/full_night_output_video_2.mp4", "app/static/videos/full_night_output_video_3.mp4"]  # Replace with actual paths
output_path = "test.mp4"  # Replace with desired output path
merge_video_clips(input_paths, output_path)
