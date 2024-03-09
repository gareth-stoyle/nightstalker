import json

def insert_video_entry(date, start_time, end_time):
    with open('src/videos.json', 'r') as f: 
        entries = json.load(f)
    # check if date already exists and return error
    
    entries[date] = {
        'start_time': start_time,
        'end_time': end_time,
        'clips': {}
    }

    with open('src/videos.json', 'w+') as f:
        json.dump(entries, f, indent=4)

    return True

def insert_clip_entry(date, clip_number, start_time, end_time):
    with open('src/videos.json', 'r') as f: 
        entries = json.load(f)
    entries[date]['clips'][clip_number] = {
        'start_time': start_time,
        'end_time': end_time,
    }

    with open('src/videos.json', 'w+') as f:
        json.dump(entries, f, indent=4)
    
    return True

def retrieve_video(date):
    with open('src/videos.json', 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date]
    except:
        return False
    
def retrieve_clips(date):
    with open('src/videos.json', 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date]['clips']
    except:
        return False
    
def insert_sensor_entry(date, entry_type, timestamp, entry):
    with open('src/sensors.json', 'r') as f: 
        entries = json.load(f)
    
    if date in entries:
        if entry_type in entries[date]:
            entries[date][entry_type][timestamp] = entry
        else:
            entries[date].update({
                f'{entry_type}': {timestamp: entry}
            })
            
    else:
        entries[date] = {
            f'{entry_type}': {timestamp: entry}
        }

    with open('src/sensors.json', 'w+') as f:
        json.dump(entries, f, indent=4)

    return True

def retrieve_sensor_entry(date, type, timestamp):
    pass

def retrieve_sensor_entries(date, entry_type):
    with open('src/sensors.json', 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date][entry_type]
    except:
        return False