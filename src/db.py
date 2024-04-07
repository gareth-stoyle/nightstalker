import json

sensor_db = 'databases/sensors.json'
video_db = 'databases/videos.json'

def insert_video_entry(date, start_time, end_time):
    try:
        with open(video_db, 'r') as f:
            entries = json.load(f)
    except FileNotFoundError:
        entries = {}

    if date in entries:
        print(f"Entry for {date} already exists.")
        return False

    entries[date] = {
        'start_time': start_time,
        'end_time': end_time,
        'clips': {}
    }

    with open(video_db, 'w') as f:
        json.dump(entries, f, indent=4)

    return True

def insert_video_duration(date, duration):
    with open(video_db, 'r') as f: 
        entries = json.load(f)

    entries[date]['duration'] = duration

    with open(video_db, 'w+') as f:
        json.dump(entries, f, indent=4)

    return True

def insert_clip_entry(date, clip_number, start_time, end_time):
    with open(video_db, 'r') as f: 
        entries = json.load(f)
        
    entries[date]['clips'][clip_number] = {
        'start_time': start_time,
        'end_time': end_time,
    }

    with open(video_db, 'w+') as f:
        json.dump(entries, f, indent=4)
    
    return True

def retrieve_video(date):
    with open(video_db, 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date]
    except:
        return False
    
def retrieve_clips(date):
    with open(video_db, 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date]['clips']
    except:
        return False
    
def insert_sensor_entry(date, entry_type, timestamp, entry):
    try:
        with open(sensor_db, 'r') as f:
            entries = json.load(f)
    except FileNotFoundError:
        entries = {}

    if date in entries:
        if entry_type in entries[date]:
            entries[date][entry_type][timestamp] = entry
        else:
            entries[date].update({
                entry_type: {timestamp: entry}
            })
    else:
        entries[date] = {
            entry_type: {timestamp: entry}
        }

    with open(sensor_db, 'w') as f:
        json.dump(entries, f, indent=4)

    return True

def retrieve_sensor_entries(date, entry_type):
    with open(sensor_db, 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date][entry_type]
    except:
        return False