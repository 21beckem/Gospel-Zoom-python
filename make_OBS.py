from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import subprocess, os

OBS_version = '27.1.3'
OBS_websocket_version = '4.9.1'

#region install OBS Studio
resp = urlopen("https://cdn-fastly.obsproject.com/downloads/OBS-Studio-" + OBS_version + "-Full-x64.zip")
zipfile = ZipFile(BytesIO(resp.read()))
zipfile.extractall(path = 'obs-studio/')
#endregion

#region install OBS Websocket
resp = urlopen("https://github.com/obsproject/obs-websocket/releases/download/" + OBS_websocket_version + "/obs-websocket-" + OBS_websocket_version + "-Windows.zip")
zipfile = ZipFile(BytesIO(resp.read()))
zipfile.extractall(path = 'obs-studio/')
#endregion

#region make profile file
os.makedirs('obs-studio/config/obs-studio/basic/scenes')
f = open("obs-studio/config/obs-studio/basic/scenes/Untitled.json", "x")
f.write('''{"AuxAudioDevice1":{"balance":0.5,"deinterlace_field_order":0,"deinterlace_mode":0,"enabled":true,"flags":0,"hotkeys":{"libobs.mute":[],"libobs.push-to-mute":[],"libobs.push-to-talk":[],"libobs.unmute":[]},"id":"wasapi_input_capture","mixers":255,"monitoring_type":0,"muted":false,"name":"Mic/Aux","prev_ver":453050371,"private_settings":{},"push-to-mute":false,"push-to-mute-delay":0,"push-to-talk":false,"push-to-talk-delay":0,"settings":{"device_id":"default"},"sync":0,"versioned_id":"wasapi_input_capture","volume":1.0},"DesktopAudioDevice1":{"balance":0.5,"deinterlace_field_order":0,"deinterlace_mode":0,"enabled":true,"flags":0,"hotkeys":{"libobs.mute":[],"libobs.push-to-mute":[],"libobs.push-to-talk":[],"libobs.unmute":[]},"id":"wasapi_output_capture","mixers":255,"monitoring_type":0,"muted":false,"name":"Desktop Audio","prev_ver":453050371,"private_settings":{},"push-to-mute":false,"push-to-mute-delay":0,"push-to-talk":false,"push-to-talk-delay":0,"settings":{"device_id":"default"},"sync":0,"versioned_id":"wasapi_output_capture","volume":1.0},"current_program_scene":"black","current_scene":"black","current_transition":"Fade","groups":[],"modules":{"auto-scene-switcher":{"active":false,"interval":300,"non_matching_scene":"","switch_if_not_matching":false,"switches":[]},"captions":{"enabled":false,"lang_id":1033,"provider":"mssapi","source":""},"decklink_captions":{"source":""},"output-timer":{"autoStartRecordTimer":false,"autoStartStreamTimer":false,"pauseRecordTimer":true,"recordTimerHours":0,"recordTimerMinutes":0,"recordTimerSeconds":30,"streamTimerHours":0,"streamTimerMinutes":0,"streamTimerSeconds":30},"scripts-tool":[]},"name":"sacrament meeting","preview_locked":false,"quick_transitions":[{"duration":300,"fade_to_black":false,"hotkeys":[],"id":1,"name":"Cut"},{"duration":300,"fade_to_black":false,"hotkeys":[],"id":2,"name":"Fade"},{"duration":300,"fade_to_black":true,"hotkeys":[],"id":3,"name":"Fade"}],"saved_projectors":[],"scaling_enabled":false,"scaling_level":0,"scaling_off_x":0.0,"scaling_off_y":0.0,"scene_order":[{"name":"main"},{"name":"black"}],"sources":[{"balance":0.5,"deinterlace_field_order":0,"deinterlace_mode":0,"enabled":true,"flags":0,"hotkeys":{"OBSBasic.SelectScene":[]},"id":"scene","mixers":0,"monitoring_type":0,"muted":false,"name":"black","prev_ver":453050371,"private_settings":{},"push-to-mute":false,"push-to-mute-delay":0,"push-to-talk":false,"push-to-talk-delay":0,"settings":{"custom_size":false,"id_counter":0,"items":[]},"sync":0,"versioned_id":"scene","volume":1.0},{"balance":0.5,"deinterlace_field_order":0,"deinterlace_mode":0,"enabled":true,"flags":0,"hotkeys":{"OBSBasic.SelectScene":[]},"id":"scene","mixers":0,"monitoring_type":0,"muted":false,"name":"main","prev_ver":453050371,"private_settings":{},"push-to-mute":false,"push-to-mute-delay":0,"push-to-talk":false,"push-to-talk-delay":0,"settings":{"custom_size":false,"id_counter":0,"items":[]},"sync":0,"versioned_id":"scene","volume":1.0}],"transition_duration":300,"transitions":[]}''')
f.close()

os.makedirs('obs-studio/config/obs-studio/basic/profiles/Untitled')
f = open("obs-studio/config/obs-studio/basic/profiles/Untitled/basic.ini", "x")
f.write('''[General]
Name=Gospel Zoom

[Video]
BaseCX=1920
BaseCY=1080
OutputCX=1920
OutputCY=1080
FPSType=0
FPSCommon=30

[Panels]
CookieId=4FC74477850E36A2

[Output]
Mode=Simple

[SimpleOutput]
RecQuality=Stream

[Audio]
MonitoringDeviceName=CABLE Input (VB-Audio Virtual Cable)
MonitoringDeviceId={0.0.0.00000000}.{258da8ef-4732-4816-b5a2-f2aef648c40a}
''')
f.close()
#endregion

thisDir = Path(__file__).parent
OBSexe_dir = thisDir.joinpath('obs-studio/bin/64bit/')
OBSprocess = subprocess.Popen(OBSexe_dir.joinpath('obs64.exe'), cwd=OBSexe_dir)