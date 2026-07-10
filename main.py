import ffmpeg
import livesplitInterface
import outroAudioInterpreter
from ui import PASAWindow
from pycaw.pycaw import AudioUtilities

def monitor_roblox_audio():
    # Get all active audio sessions in Windows
    sessions = AudioUtilities.GetAllSessions()
    
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "RobloxPlayerBeta.exe":
            return session

# Example usage targeting Google Chrome
rblxAudio = monitor_roblox_audio()

def main():
    sample = ffmpeg.input("./audioSample.mp3")
    #checks if it's for the ending or not
    outroAudioInterpreter.audioIsForEnding(rblxAudio,sample)
    app = PASAWindow()
    app.run()


if __name__ == "__main__":
    main()