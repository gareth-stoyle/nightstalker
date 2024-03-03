# Convert start time to seconds
start_time = '23:25:00'
fps = 8
frame_number = 180000  # Replace with the actual frame number


# Calculate timestamp for each frame
def calculate_timestamp(start_time, fps, frame_number):
    '''Calculate the timestamp to put on a frame'''
    start_hour, start_minute, start_second = map(int, start_time.split(':'))
    start_seconds = start_hour * 3600 + start_minute * 60 + start_second
    elapsed_seconds = frame_number / fps
    total_seconds = start_seconds + elapsed_seconds
    total_seconds %= 86400  # Ensure it's within a 24-hour period
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Example usage:
timestamp = calculate_timestamp(start_time, fps, frame_number)

print(timestamp)
