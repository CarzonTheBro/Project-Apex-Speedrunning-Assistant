import ffmpeg
import livesplitInterface
import outroAudioInterpreter
from ui import PASAWindow
from pycaw.pycaw import AudioUtilities



def main():
    outroAudioInterpreter.test(1)
    # rblxAudio = outroAudioInterpreter.monitor_roblox_audio()
    sample = ffmpeg.input("audioSample.mp3")
    
    #checks if it's for the ending or not
    outroAudioInterpreter.audioIsForEnding(0.3, rblxAudio, sample)
    app = PASAWindow()
    app.run()


if __name__ == "__main__":
    main()