import time
import threading
import numpy as np
import ffmpeg
import pyaudiowpatch as pyaudio
from pycaw.pycaw import AudioUtilities

SAMPLE_PATH = "audioSample.mp3"
TARGET_RATE = 44100


def load_sample_as_array(path: str, target_rate: int = TARGET_RATE) -> np.ndarray:
    # Decode an audio file to a mono float32 numpy array via ffmpeg.
    out, _ = (
        ffmpeg
        .input(path)
        .output("pipe:", format="f32le", acodec="pcm_f32le", ac=1, ar=target_rate)
        .run(capture_stdout=True, capture_stderr=True)
    )
    return np.frombuffer(out, dtype=np.float32)


def is_roblox_running() -> bool:
    # Use pycaw to check whether Roblox has an active audio session.
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == "RobloxPlayerBeta.exe":
            return True
    return False


def audioIsForEnding(sensitivity: float, liveAudio: np.ndarray, sampleAudio: np.ndarray) -> bool:
    n = len(sampleAudio)
    if n == 0 or len(liveAudio) < n:
        return False

    live64 = liveAudio.astype(np.float64)
    sample64 = sampleAudio.astype(np.float64)

    # sum(live_window * sample) for every valid alignment offset
    cross = np.correlate(live64, sample64, mode="valid")

    # rolling sum(live_window^2) for every valid alignment offset
    live_sq_cumsum = np.cumsum(np.insert(live64 ** 2, 0, 0.0))
    live_sq_sum = (live_sq_cumsum[n:] - live_sq_cumsum[:-n])[: len(cross)]

    sample_energy = float(np.sum(sample64 ** 2))

    # residual = live_window + sample (sample already inverted)
    # residual_energy = sum(live^2) + 2*sum(live*sample) + sum(sample^2)
    residual_energy = np.maximum(live_sq_sum + 2.0 * cross + sample_energy, 0.0)

    best_idx = int(np.argmin(residual_energy))
    best_residual_rms = float(np.sqrt(residual_energy[best_idx] / n))

    return best_residual_rms < sensitivity


def get_loopback_device(p: "pyaudio.PyAudio"):
    """Find the loopback-capable version of the default output device."""
    wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

    if not default_speakers.get("isLoopbackDevice", False):
        for loopback in p.get_loopback_device_info_generator():
            if default_speakers["name"] in loopback["name"]:
                return loopback
        raise RuntimeError("No loopback device found matching default output.")
    return default_speakers


def monitor_roblox_audio(
    sensitivity: float = 0.05,
    sample_path: str = SAMPLE_PATH,
    poll_interval: float = 0.5,
    frame_seconds: float = 0.05,
    on_ending=None,
    stop_event: "threading.Event | None" = None,
):
    sample = load_sample_as_array(sample_path)
    sample_seconds = len(sample) / TARGET_RATE
    alignment_slop = 0.3  # extra seconds of buffer to search for best alignment
    buffer_seconds = sample_seconds + alignment_slop
    buffer_len = int(buffer_seconds * TARGET_RATE)

    p = pyaudio.PyAudio()
    device = get_loopback_device(p)
    rate = int(device["defaultSampleRate"])
    channels = device["maxInputChannels"]
    frame_frames = max(int(frame_seconds * rate), 1)

    stream = p.open(
        format=pyaudio.paFloat32,
        channels=channels,
        rate=rate,
        frames_per_buffer=frame_frames,
        input=True,
        input_device_index=device["index"],
    )

    # Rolling buffer of recent live audio, resampled to TARGET_RATE, mono.
    live_buffer = np.zeros(0, dtype=np.float64)

    print("Listening... (Ctrl+C to stop)")
    try:
        while stop_event is None or not stop_event.is_set():
            if not is_roblox_running():
                # Drop stale audio so it can't be compared against once
                # Roblox restarts later.
                live_buffer = np.zeros(0, dtype=np.float64)
                time.sleep(poll_interval)
                continue

            raw = stream.read(frame_frames, exception_on_overflow=False)
            frame = np.frombuffer(raw, dtype=np.float32)

            # If captured audio is multi-channel, collapse to mono to
            # match the mono sample.
            if channels > 1:
                frame = frame.reshape(-1, channels).mean(axis=1)

            # Resample this frame to TARGET_RATE if the device rate differs.
            if rate != TARGET_RATE:
                frame = np.interp(
                    np.linspace(0, len(frame), int(len(frame) * TARGET_RATE / rate)),
                    np.arange(len(frame)),
                    frame,
                )

            live_buffer = np.concatenate([live_buffer, frame])
            if len(live_buffer) > buffer_len:
                live_buffer = live_buffer[-buffer_len:]

            # Not enough audio accumulated yet to compare against the sample.
            if len(live_buffer) < len(sample):
                continue

            # Check happens every frame now, against the rolling buffer.
            if audioIsForEnding(sensitivity, live_buffer, sample):
                print("Detected ending audio!")
                if on_ending is not None:
                    on_ending()
                # Clear the buffer so the same audio can't immediately
                # re-trigger a match on the very next frame.
                live_buffer = np.zeros(0, dtype=np.float64)

    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def test(sensitivity: float = 0.01):
    sample = load_sample_as_array(SAMPLE_PATH)
    live = -sample
    assert audioIsForEnding(sensitivity, live, sample)
    print("success")

if __name__ == "__main__":
    test()