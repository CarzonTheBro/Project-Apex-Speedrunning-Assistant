import ffmpeg
from pycaw.pycaw import AudioUtilities

def audioIsForEnding(sensitivity, gameAudio, sampleAudio):
    overlayedAudio = ffmpeg.filter([gameAudio,sampleAudio], 'amix', duration='shortest')
    if(overlayedAudio.volume < sensitivity):
        return True
    else:
        return False
    
def test(sensitivity):
    sample = ffmpeg.input("audioSample.mp3")
    assert audioIsForEnding(sensitivity, sample, sample)

def monitor_roblox_audio():
    # Get all active audio sessions in Windows
    sessions = AudioUtilities.GetAllSessions()
    
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "RobloxPlayerBeta.exe":
            return session

