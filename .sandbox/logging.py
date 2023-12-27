import subprocess
import os

def run_temperature_logging():
    script_path = os.path.join(os.path.dirname(__file__), "temperature_logger.sh")
    process = subprocess.Popen([script_path])
    return process