# DreamDash
A sleep tracking system which synchronises FitBit data with recorded footage and a DHT11 environmental sensor.

## Setup
Create virtual environment:

`python -m venv .venv`

(If you have opencv installed already on the pi, add `--system-site-packages` to the virtual environment and remove the opencv packages from requirements.txt, pip installing opencv takes a long time!)

Install requirements:

`pip install -r requirements.txt`

Install MP4Box:

`sudo apt-get install -y gpac`

## Run
### Run unit tests
`make test`

### Initiate recording
`make record`

### Launch Flask dashboard
`make dashboard`