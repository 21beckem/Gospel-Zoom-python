#region   Imports
import datetime, time, subprocess, csv, os, webbrowser, sys, json
try:
    import pyautogui as gui
    from PIL import Image
    from cv2 import cv2
    from threading import Thread
    from numpy import asarray
    from flask import Response, Flask, render_template, request, send_file
    import threading, imutils, mss, socket, eel, random, numpy, urllib.parse, keyboard
except ModuleNotFoundError as err:
    print("You don't have all the needed modules installed. Please go through the read me files.")
    exit()
#endregion
def getConfig():
    global config
    f = open('config.json')
    config = json.load(f)
    f.close()
    neededKeys = ["webinarId", "browser", "buttonConfidence", "remotePort"]
    for key in neededKeys:
        if not key in config:
            return False
    return True
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
    def resetMousePos(click=False):
        x = gui.size()[0]# / 2
        y = gui.size()[1] / 2
        gui.moveTo(x, y)
        if click:
            gui.click()
    def rawPersistantClick(imgName):
        for _ in range(Zoom.tries):
            var = gui.locateOnScreen(__path__ + imgName, confidence=config['buttonConfidence'])
            if var != None:
                gui.click(var)
                Zoom.resetMousePos()
                return True
            eel.sleep(Zoom.betweenTries)
        return False
    def rawClick(imgName):
        var = gui.locateOnScreen(__path__ + imgName, confidence=config['buttonConfidence'])
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

Handshake = None;
userShake = '0'

eel.sleep(1)

def confirmShake():
    global Handshake, userShake
    userShake = request.args.get('x')
    return Handshake == userShake

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
@app.route("/feed")
def video_feed():
    if confirmShake():
        return Response(generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return ('', 400)
@app.route('/favicon.ico')
def web_Favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')
@app.route('/churchZoomIcon')
def web_IconImage():
    return send_file('churchZoomIcon.png', mimetype='image/png')
@app.route('/')
def web_index():
    eel.remoteConnected()
    return render_template('index.html')


def generate():
    global outputFrame, lock, Handshake, userShake
    while True:
        if not Handshake == userShake:
            yield send_file('churchZoomIcon.png', mimetype='image/png')
            break
        # make sure we actually geta capture
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", cv2.cvtColor(outputFrame, cv2.COLOR_BGR2RGB))
            if not flag:
                continue
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
    app.run(host=ipv4, port=config['remotePort'], debug=False, threaded=True, use_reloader=False)
#endregion

#region   Eel
eel.init('web')
def startEel():
    eel.start('index.html', mode=config['browser'], block=False)
    #os.system('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
    #webbrowser.open_new('www.google.com')
    # manage numpad
    eel.sleep(3)
    keyboard.press_and_release('F11')
    Zoom.resetMousePos()
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
                eel.sleep(0.5)
                eel.webinarEnded()
                Zoom.resetMousePos(click=True)
                Handshake = None;
            if keyboard.is_pressed('0'):
                set_handshake()
                if Zoom.launchWebinar('https://zoom.us/s/' + config['webinarId']) or True:
                    eel.sleep(9)
                    Zoom.resetMousePos(click=True)
                    gui.hotkey('ctrl', 'w')
                    eel.sleep(0.05)
                    gui.hotkey('alt', 'tab')
                else:
                    print('error while launching webinar')
                    eel.webinarEnded()
        eel.sleep(0.05)

@eel.expose
def set_handshake():
    global Handshake;
    Handshake = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    eel.setHandshake(Handshake)
#endregion

if __name__ == '__main__':
    if getConfig():
        server = Thread(target=startScreenServer, daemon=True)
        server.start()
        startEel()
    else:
        print("Oh no, something's wrong with your config.json. Or it doesn't exist...  read the README")
