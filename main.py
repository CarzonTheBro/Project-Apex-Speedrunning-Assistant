import ffmpeg
import livesplitInterface
import outroAudioInterpreter
from ui import PASAWindow

"""sample = ffmpeg.audio("./audioSample.mp3")"""

def main():
    app = PASAWindow()
    app.run()


if __name__ == "__main__":
    main()