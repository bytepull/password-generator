#!/usr/bin/python3

pip install -r requirements.txt -U
pyinstaller --onefile --windowed --name='Password Generator' --icon 'icon.icns' main.py