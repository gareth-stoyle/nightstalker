import json

def insert_video_entry(date, start_time, end_time):
    with open('db.json', 'r') as f: 
        entries = json.load(f)
    # check if date already exists and return error
    
    entries[date] = {
        'start_time': start_time,
        'end_time': end_time,
        'clips': {}
    }

    with open('db.json', 'w+') as f:
        json.dump(entries, f, indent=4)

    return True

def insert_clip_entry(date, clip_number, start_time, end_time):
    with open('src/db.json', 'r') as f: 
        entries = json.load(f)
    entries[date]['clips'][clip_number] = {
        'start_time': start_time,
        'end_time': end_time,
    }

    with open('src/db.json', 'w+') as f:
        json.dump(entries, f, indent=4)
    
    return True

def retrieve_video(date):
    with open('src/db.json', 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date]
    except:
        return False
    
def retrieve_clips(date):
    with open('src/db.json', 'r') as f: 
        entries = json.load(f)
    try:
        return entries[date]['clips']
    except:
        return False
