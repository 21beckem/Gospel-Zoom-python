from obswebsocket import obsws, requests
from pathlib import Path
import subprocess, time
class OBS:
    host = 'localhost'
    port = 4444
    password = ''
    ws = None
    connected = False
    scenes = []
    def connect(thisPass):
        OBS.password = thisPass
        OBS.ws = obsws(OBS.host, OBS.port, OBS.password)
        OBS.ws.connect()
        OBS.connected = True
        OBS.getScenes()
        return OBS.connected
    def getCurrentScene():
        if OBS.connected:
            return OBS.ws.call(requests.GetCurrentScene()).getName()
    def getScenes():
        if OBS.connected:
            scenes = OBS.ws.call(requests.GetSceneList())
            sceneNames = []
            for s in scenes.getScenes():
                sceneNames.append(s['name'])
                OBS.scenes = scenes
            return sceneNames
        return ['error']
    def setScene(sceneName):
        if OBS.connected:
            OBS.ws.call(requests.SetCurrentScene(sceneName))
    def nextScene():
        if OBS.connected:
            currentI = OBS.scenes.index(OBS.getCurrentScene())
            currentI = (currentI + 1) % len(OBS.scenes)
            OBS.setScene(OBS.scenes[currentI])

thisDir = Path(__file__).parent
OBSexe_dir = thisDir.joinpath('obs-studio/bin/64bit/')
OBSprocess = subprocess.Popen(OBSexe_dir.joinpath('obs64.exe'), cwd=OBSexe_dir)
exit()
time.sleep(5)
print('OBS Started')
print(OBS.connect('secret'))
scenes = OBS.getScenes()

print(scenes)
time.sleep(1)
for i in range(10):
    OBS.nextScene()
    time.sleep(1)
