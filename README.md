# Gospel Zoom&trade;

<p align="center">
   <img src="https://github.com/21beckem/Gospel-Zoom-python/blob/main/churchZoomIcon.png?raw=true" alt="logo" width="130"/>
</p>
   
<p align="center">Software made to make managing Zoom Webinars MUCH easier!</p>

## Demo

<p align="center">
   <a href="https://youtu.be/F2N2xZkTnfU">
      <img src="https://drive.google.com/uc?export=view&id=1p69An11DmVjCsnjjUQXXu07YRIEtgMo4" alt="Watch the demo video" width="40%"/>
   </a>
</p>

## Installation

Built on Python 3.10.0

1. Download the code as zip and extract it to a local folder.
2. Open extracted folder in cmd and run
```bash
pip install -r requirements.txt
```
3. Edit config.json for your webinar with your Zoom email, password, and webinarId
    - (`webinarId` could also be a meeting id as long as there is no password to join the meeting)

```json
{
    "zoom_email": "me@example.com",
    "zoom_password": "MySneakyPassword",
    "webinarId": "00000000000",
    "remotePort": 1830,
    "backspace_to_shutdown": true
}
```

## Zoom Setup
1. In your Webinar options, ensure that `Enable Practice Session` is turned off
2. Zoom settings you need to turn __ON__ on your computer
   - General
     - Always show meeting controls
     - Ask me to confirm when I leave a meeting
   - Video
     - Turn off my video when joining a meeting
   - Audio
     - Automatically join audio by computer when joining a meeting
     - Mute my microphone when joining a meeting

## Usage

1. Ensure the device you're using as your remote is on the same WiFi as the Gospel Zoom&trade; server.
2. Open cmd in project folder and run
```bash
py app.py
```
4. Scan the QR code on the screen with your device
   - This will open a new browser window and the QR code on the Gospel Zoom&trade; screen will dissapear
5. When ready, click 0 on the Gospel Zoom&trade; keyboard to start the webinar
6. Once the zoom webinar has launched, you should see a 4-digit "Handshake" code on the bottom left of the screen.
   - On your remote device, click on Options (or swipe from left to right) and select Handshake, type in your 4-digit code and click Save.
7. Done! You are now ready to control your webinar from your device.

__NOTE:__ The handshake code is randomly generated on the Gospel Zoom&trade; screen at the beggining of each webinar.

## Features

* no remote features work without a valid handshake for extra security
* turn on the preview toggle at top right and you'll see your computer screen
* press the buttons at the bottom to control zoom
    * press the end button twice to actually end the meeting
* webinar can only be started from the Gospel Zoom&trade; computer for extra security
