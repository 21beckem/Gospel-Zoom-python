#region   Imports
import datetime, time, subprocess, csv, os, webbrowser, sys
try:
    import pyautogui as gui
    from PIL import Image
    from cv2 import cv2
    from threading import Thread
    import numpy, urllib.parse
    from imutils.video import VideoStream
    from numpy import asarray
    from flask import Response, Flask, render_template, request
    import threading, imutils, mss, socket, eel, random
except ModuleNotFoundError as err:
    print("You don't have all the needed modules installed. Please go through the read me files. Press anything to exit")
    exit()
#endregion

#region   Zoom

__path__ = 'zoom_images/'

gui.FAILSAFE = False
class Zoom:
    running = False
    tries = 5
    betweenTries = 0.5
    def launchWebinar(startLink):
        link = 'https://zoom.us/switch_account?backUrl=' + urllib.parse.quote(startLink)
        #print(link)
        webbrowser.open(link)
        eel.sleep(3)
        Zoom.running =  Zoom.rawPersistantClick('signInBtn.png')
        return Zoom.running
    def startWebinar():
        if Zoom.rawPersistantClick('startWebinar.png'):
            if Zoom.rawPersistantClick('startBtn.png'):
                return True
        return False
    def resetMousePos():
        x = gui.size()[0] / 2
        y = 0#gui.size()[1] / 2
        gui.moveTo(x, y)
    def rawPersistantClick(imgName):
        for _ in range(Zoom.tries):
            var = gui.locateOnScreen(__path__ + imgName, confidence=0.9)
            if var != None:
                gui.click(var)
                Zoom.resetMousePos()
                return True
            eel.sleep(Zoom.betweenTries)
        return False
    def rawClick(imgName):
        var = gui.locateOnScreen(__path__ + imgName, confidence=0.9)
        if var != None:
            gui.click(var)
            Zoom.resetMousePos()
            return True
        return False
    def setVideo(onOff):
        imgName = 'videoOff.png' if onOff else 'videoOn.png'
        Zoom.rawPersistantClick(imgName)
    def setMic(onOff):
        imgName = 'micOff.png' if onOff else 'micOn.png'
        Zoom.rawPersistantClick(imgName)
    def toggleVideo():
        if not Zoom.rawClick('videoOff.png'):
            Zoom.rawClick('videoOn.png')
    def toggleMic():
        if not Zoom.rawClick('micOff.png'):
            Zoom.rawClick('micOn.png')
    def setVideoAndAudio_synced(onOff):
        imgName = 'videoOff.png' if onOff else 'videoOn.png'
        Zoom.rawClick(imgName)
        imgName = 'micOff.png' if onOff else 'micOn.png'
        Zoom.rawPersistantClick(imgName)
    def toggleVideoAndAudio_synced():
        onOff = Zoom.rawClick('videoOff.png')
        if not onOff:
            Zoom.rawClick('videoOn.png')
        imgName = 'micOff.png' if onOff else 'micOn.png'
        Zoom.rawPersistantClick(imgName)
    def endWebinar():
        if not Zoom.rawClick('endForAllBtn.png'):
            Zoom.rawClick('endBtn.png')
            cancelEndTh = Thread(target = Zoom.cancelEnd)
            cancelEndTh.start()
            Zoom.running = True
            return False
        else:
            Zoom.running = False
            return True
    def cancelEnd(timeout=2):
        eel.sleep(timeout)
        Zoom.rawClick('cancelEndBtn.png')
    def test():
        return True
#endregion

#region   Screenserver

ipv4 = socket.gethostbyname(socket.gethostname())
outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

Handshake = '0000';

eel.sleep(1)

def confirmShake():
    return Handshake == request.args.get('x')

@app.route('/startmeeting')
def startmeeting():
    if confirmShake():
        Zoom.startWebinar()
        return ('', 204)
    else:
        return ('', 400)
@app.route('/togglefeed')
def togglefeed():
    if confirmShake():
        Zoom.toggleVideoAndAudio_synced()
        return ('', 204)
    else:
        return ('', 400)
@app.route('/endmeeting')
def endmeeting():
    if confirmShake():
        Zoom.endWebinar()
        return ('', 204)
    else:
        return ('', 400)
@app.route("/")
def video_feed():
    if confirmShake():
        return Response(generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return ('', 400)
@app.route("/remote_connected")
def remote_connected():
    eel.remoteConnected()
    return ('', 204)


def generate():
	global outputFrame, lock
	while True:
		# make sure we actually geta capture
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", cv2.cvtColor(outputFrame, cv2.COLOR_BGR2RGB))
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


def get_frames():
    global outputFrame, lock
    while True:
        with mss.mss() as sct:
            rawImg = sct.grab(sct.monitors[1])
            img = Image.frombytes("RGB", rawImg.size, rawImg.bgra, "raw", "BGRX").resize((700, 394), Image.ANTIALIAS)
        with lock:
            outputFrame = asarray(img)

def startScreenServer():
    # start a thread that will perform motion detection
    t = threading.Thread(target=get_frames, daemon=True)
    t.start()
    # start the flask app
    app.run(host=ipv4, port=1830, debug=False, threaded=True, use_reloader=False)
#endregion

#region   Eel
eel.init('web')
def startEel():
    eel.start('index.html', mode='edge', block=False)
    # manage numpad
    wasRunning = False;
    eel.setIPconnectionQR('["' + socket.gethostbyname(socket.gethostname()) + '", 1830]')
    while True:
        if Zoom.running:
            if not wasRunning:
                wasRunning = True
            if keyboard.is_pressed('1'):
                Zoom.startWebinar()
            if keyboard.is_pressed('2'):
                Zoom.toggleVideoAndAudio_synced()
            if keyboard.is_pressed('3'):
                Zoom.endWebinar()
        else:
            if wasRunning:
                wasRunning = False
                eel.webinarEnded()
            if keyboard.is_pressed('0'):
                set_handshake()
                if Zoom.launchWebinar('https://zoom.us/s/96138303673'):
                    eel.sleep(5)
                else:
                    print('error while launching webinar')
        eel.sleep(0.05)

@eel.expose
def set_handshake():
    global Handshake;
    Handshake = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    eel.setHandshake(Handshake)
#endregion

import keyboard

def main():
    if Zoom.launchWebinar('https://zoom.us/s/96138303673'):
        eel.sleep(5)

        while True:
            eel.sleep(1)
            if not Zoom.running:
                break
    else:
        print('error while launching webinar')


if __name__ == '__main__':
    server = Thread(target=startScreenServer, daemon=True)
    server.start()
    startEel()