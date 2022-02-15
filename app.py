#region   Imports
import datetime, time, subprocess, csv, os, webbrowser, sys, json
try:
    import pyautogui as gui
    from PIL import Image
    from cv2 import cv2
    from threading import Thread
    from numpy import asarray
    from flask import Response, Flask, render_template, request, send_file
    import threading, imutils, mss, socket, eel, random, numpy, urllib.parse, keyboard, asyncio, pyppeteer
except ModuleNotFoundError as err:
    print("You don't have all the needed modules installed. Please go through the read me files.")
    exit()
#endregion
def getConfig():
    global config
    f = open('config.json')
    config = json.load(f)
    f.close()
    neededKeys = ["webinarId", "remotePort", "backspace_to_shutdown"]
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
    center_click_before = True
    ending_internal = False
    def launchWebinar(startLink):
        asyncio.run(Zoom.async_launchWebinar(startLink))
    async def async_launchWebinar(startLink):
        browser = await pyppeteer.launch(headless=False, userDataDir='webdata/', autoClose=False)
        page = await browser.newPage()
        link = 'https://zoom.us/switch_account?backUrl=' + urllib.parse.quote(startLink)
        await page.goto(link)
        
        await page.evaluate('''() => {
        document.getElementById('email').value = "''' + config['zoom_email'] + '''";
        document.getElementById('password').value = "''' + config['zoom_password'] + '''";
        document.forms[0].querySelector('button').click();
        }''')
        time.sleep(5)
        await browser.close()
        Zoom.running =  True
        return Zoom.running
    def resetMousePos(click=False, center=False):
        x = (gui.size()[0] / 2) if center else gui.size()[0]
        y = gui.size()[1] / 2
        gui.moveTo(x, y)
        if click:
            gui.click()
    def toggleVideo():
        if Zoom.center_click_before:
            Zoom.resetMousePos(click=True, center=True)
        gui.hotkey('alt', 'v')
        Zoom.resetMousePos()
    def toggleMic():
        if Zoom.center_click_before:
            Zoom.resetMousePos(click=True, center=True)
        gui.hotkey('alt', 'a')
        Zoom.resetMousePos()
    def toggleAudioAndVideo():
        oldCickBefore = Zoom.center_click_before
        Zoom.toggleMic()
        Zoom.center_click_before = False
        Zoom.toggleVideo()
        Zoom.center_click_before = oldCickBefore
    def endWebinar():
        if Zoom.center_click_before:
            Zoom.resetMousePos(click=True, center=True)
        if Zoom.ending_internal:
            gui.hotkey('enter')
            Zoom.ending_internal = False
            Zoom.running = False
        else:
            gui.hotkey('alt', 'q')
            Zoom.ending_internal = True
            cancelEndTh = Thread(target = Zoom.cancelEnd)
            cancelEndTh.start()
        Zoom.resetMousePos()
    def cancelEnd(timeout=2):
        eel.sleep(timeout)
        if Zoom.running:
            gui.hotkey('esc')
            Zoom.ending_internal = False
#endregion

#region   Screenserver

ipv4 = socket.gethostbyname(socket.gethostname())
outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

Handshake = None;
userShake = '0'
userGettingScreenFeed = False

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
        userGettingScreenFeed = True
        return Response(generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return ('', 400)
@app.route('/favicon.ico')
def web_Favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')
@app.route('/churchZoomIcon')
def web_IconImage():
    userGettingScreenFeed = False
    return send_file('churchZoomIcon.png', mimetype='image/png')
@app.route('/')
def web_index():
    eel.remoteConnected()
    return render_template('index.html')


def generate():
    global outputFrame, lock, Handshake, userShake
    while True:
        if not Handshake == userShake or not userGettingScreenFeed:
            userGettingScreenFeed = False
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
    eel.start('index.html', mode=False, port=1820, block=False)
    webbrowser.open_new('http://localhost:1820/index.html')
    # manage numpad
    eel.sleep(3)
    keyboard.press_and_release('F11')
    Zoom.resetMousePos()
    wasRunning = False;
    eel.setIPconnectionQR('["' + socket.gethostbyname(socket.gethostname()) + '", ' + str(config['remotePort']) + ']')
    while True:
        if Zoom.running:
            if not wasRunning:
                wasRunning = True
            if keyboard.is_pressed('2'):
                Zoom.toggleAudioAndVideo()
            if keyboard.is_pressed('3'):
                Zoom.endWebinar()
        else:
            if wasRunning:
                wasRunning = False
                eel.sleep(0.5)
                eel.webinarEnded()
                Zoom.resetMousePos(click=True)
                Handshake = None;
            if config['backspace_to_shutdown'] and keyboard.is_pressed('backspace'):
                os.system("shutdown /s /t 1")
            if keyboard.is_pressed('0'):
                set_handshake()
                if Zoom.launchWebinar('https://zoom.us/s/' + config['webinarId']) or True:
                    Zoom.resetMousePos()
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
