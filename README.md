# screen-holder

python script that auto move mouse and click to hold the windows screen

脚本在每天晚上9点后开始定时检测是否有鼠标和键盘操作，如果没有，则移动鼠标并触发右键，避免自动关机

# build exe

```bash
pipenv shell

pipenv install psutil pyautogui pynput pyinstaller

# build in pipenv shell -w 隐藏控制台 -F 打包成一个exe，会有两个process,其中一个是pyinstaller的bootstrap进程
pyinstaller.exe -Fw --icon=icon.ico --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" ./screen-holder.py

```
