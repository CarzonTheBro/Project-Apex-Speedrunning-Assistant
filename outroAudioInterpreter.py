import ffmpeg
import ffmpeg.audio

def audioIsForEnding(sensitivity, gameAudio, sampleAudio):
    
    overlayedAudio = ffmpeg.filter([gameAudio,sampleAudio], 'amix', duration='shortest')
    if(overlayedAudio.volume < sensitivity):
        return True
    else:
        return False
def test(sensitivity):
    sample = ffmpeg.audio("./audioSample.mp3")
    assert audioIsForEnding(sensitivity, sample, sample)