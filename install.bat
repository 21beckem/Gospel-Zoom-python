@ECHO OFF
cd /D "%~dp0"

net session >nul 2>&1
if not %errorLevel% == 0 (
    start "" cmd /c "echo. & echo. & echo. & echo ERROR: You must run the installer as admin. & echo. & echo. & echo( & echo Press any key to exit . . . &pause >nul"
    ::echo ERROR: You must run the installer as admin.
    ::pause >nul
    exit /b
)

set PYTHON_VERSION=3.10.0
echo.
:::   /$$$$$$                                          /$$       /$$$$$$$$                                  
:::  /$$__  $$                                        | $$      |_____ $$                                   
::: | $$  \__/  /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$ | $$           /$$/   /$$$$$$   /$$$$$$  /$$$$$$/$$$$ 
::: | $$ /$$$$ /$$__  $$ /$$_____/ /$$__  $$ /$$__  $$| $$          /$$/   /$$__  $$ /$$__  $$| $$_  $$_  $$
::: | $$|_  $$| $$  \ $$|  $$$$$$ | $$  \ $$| $$$$$$$$| $$         /$$/   | $$  \ $$| $$  \ $$| $$ \ $$ \ $$
::: | $$  \ $$| $$  | $$ \____  $$| $$  | $$| $$_____/| $$        /$$/    | $$  | $$| $$  | $$| $$ | $$ | $$
::: |  $$$$$$/|  $$$$$$/ /$$$$$$$/| $$$$$$$/|  $$$$$$$| $$       /$$$$$$$$|  $$$$$$/|  $$$$$$/| $$ | $$ | $$
:::  \______/  \______/ |_______/ | $$____/  \_______/|__/      |________/ \______/  \______/ |__/ |__/ |__/
:::                               | $$                                                                      
:::                               | $$                                                                      
:::                               |__/                                                                      
:::                          _____ _   _  _____ _______       _      _      ______ _____  
:::                         |_   _| \ | |/ ____|__   __|/\   | |    | |    |  ____|  __ \ 
:::                           | | |  \| | (___    | |  /  \  | |    | |    | |__  | |__) |
:::                           | | | . ` |\___ \   | | / /\ \ | |    | |    |  __| |  _  / 
:::                          _| |_| |\  |____) |  | |/ ____ \| |____| |____| |____| | \ \ 
:::                         |_____|_| \_|_____/   |_/_/    \_\______|______|______|_|  \_\
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
echo.
echo ------------------------------------------------------------------
echo Installing local PY interpreter...
echo ------------------------------------------------------------------

curl -L -O https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

if not exist python\ ( 
    mkdir python
)
python-%PYTHON_VERSION%-amd64.exe /passive Include_tcltk=0 Include_test=0 InstallLauncherAllUsers=0 Include_launcher=0 Include_doc=0 Shortcuts=0 

del python-%PYTHON_VERSION%-amd64.exe
echo done!

echo.

echo ------------------------------------------------------------------
echo Installing Python Dependencies...
echo ------------------------------------------------------------------

py -m pip install --upgrade pip
pip install -r requirements.txt
echo done!

echo.
echo.
echo ------------------------------------------------------------------
echo Installing Audio Cable...
echo ------------------------------------------------------------------
echo.

curl -L -O https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip
if not exist virtualaudiocable\ ( 
    mkdir virtualaudiocable
)
tar -xf VBCABLE_Driver_Pack43.zip -C virtualaudiocable\
del VBCABLE_Driver_Pack43.zip
virtualaudiocable\VBCABLE_Setup_x64.exe
echo done!

py make_OBS.py