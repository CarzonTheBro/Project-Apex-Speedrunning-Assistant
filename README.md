# Project-Apex-Speedrunning-Assistant (PASA)
The PASA is an open-source program to help you time your speedruns accurately.
This was made by 2 high schoolers on a bored few days

NOTE: Currently Windows Only
Note: Currently very early in development
Note: bugs... maybe many

## What we will NOT ADD
- Prompts to the user about positions
- Outlining Enemies
- Highlighting Audio Sources
- No dynamic overlays during gameplay
### WE DO NOT CONDONE HACKING OR EXPLOITING WITH THIS SOFTWARE

## Todo list for the contributers
- rewrite outroAudioInterpreter.py and make it more integrated with main.py
- fix the ~500ms lag for starting
- add in radio buttons in the gui for GPU support
- ...
- make this into an executable
- so much work sob

## 1. Downloading

- Download the repository as a ZIP
- Extract contents
- Run main.py

## 2. Start LiveSplit's TCP Server

Steps to start a TCP Server on LiveSplit:
1. Start LiveSplit
2. Right Click on LiveSplit
3. Press "Control"
4. Press "Start TCP Server"

## 3. Using GUI

What should happen is the following:
- Live Split Interface connects with Live Split
- GUI should display

Navigating the UI is intuitive and simple. Simply, press buttons, and find out!
- Start/Stop Monitoring
  - This allows you to start monitoring the game for cues for starting, death, and end
- Debug
  - This brings you up to the menu with various debug options, allowing you to test each of the modules, ensiring that they work.
- Settings
  - This brings you to configuration of where the OCR will try to read "Cam" (or whatever is specified in config.json) or "Killed" (or whatever is in config.json) have fun! (this is the most annoying part)


## 4. Actually Monitoring the Game

1. Start up the Program
2. Debug each module individually
3. Adjust settings as needed
4. Click "Start Monitoring"
5. Give the program a little bit to boot up OCR (about 1-5 seconds)
6. If all is well, then the program should start the livesplit timer within 500 ms of the "Cam Started" text disappearing
7. Dead? Don't Worry! The program resets the timer for your next attempt
8. Reached Evacuation? Perfect! The program stops the timer