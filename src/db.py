import json

class DB:
    def __init__(self, sensor_db='databases/sensors.json', video_db='databases/videos.json'):
        self.sensor_db = sensor_db
        self.video_db = video_db
    
    def _load_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        return data
    
    def _write_json(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def insert_video_entry(self, date, start_time, end_time):
        entries = self._load_json(self.video_db)
        if date in entries:
            print(f"Entry for {date} already exists.")
            return False
        
        entries[date] = {
            'start_time': start_time,
            'end_time': end_time,
            'clips': {}
        }
        
        self._write_json(self.video_db, entries)
        return True
    
    def insert_video_duration(self, date, duration):
        if type(duration) != int:
            return False
        entries = self._load_json(self.video_db)
        entries[date]['duration'] = duration
        self._write_json(self.video_db, entries)
        return True
    
    def insert_clip_entry(self, date, clip_number, start_time, end_time):
        entries = self._load_json(self.video_db)
        entries[date]['clips'][clip_number] = {
            'start_time': start_time,
            'end_time': end_time,
        }
        self._write_json(self.video_db, entries)
        return True
    
    def retrieve_video(self, date):
        entries = self._load_json(self.video_db)
        try:
            return entries[date]
        except KeyError:
            return False
    
    def retrieve_clips(self, date):
        entries = self._load_json(self.video_db)
        try:
            return entries[date]['clips']
        except KeyError:
            return False
    
    def insert_sensor_entry(self, date, entry_type, timestamp, entry):
        entries = self._load_json(self.sensor_db)
        if date in entries:
            if entry_type in entries[date]:
                entries[date][entry_type][timestamp] = entry
            else:
                entries[date].update({entry_type: {timestamp: entry}})
        else:
            entries[date] = {entry_type: {timestamp: entry}}
        
        self._write_json(self.sensor_db, entries)
        return True
    
    def retrieve_sensor_entries(self, date, entry_type):
        entries = self._load_json(self.sensor_db)
        try:
            return entries[date][entry_type]
        except KeyError:
            return False
