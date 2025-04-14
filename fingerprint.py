import librosa
import numpy as np

SAMPLE_RATE = 22050
FAN_VALUE = 15
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200
PEAK_NEIGHBORHOOD_SIZE = 20

def load_audio(path):
    y, sr = librosa.load(path, sr=SAMPLE_RATE, mono=True)
    return y

def get_spectrogram_peaks(y):
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=512))
    local_max = (S == librosa.util.peak_pick(S, PEAK_NEIGHBORHOOD_SIZE, PEAK_NEIGHBORHOOD_SIZE,
                                             PEAK_NEIGHBORHOOD_SIZE, PEAK_NEIGHBORHOOD_SIZE, 0.5, 5))
    peaks = np.argwhere(local_max)
    times = peaks[:, 1]
    freqs = peaks[:, 0]
    return list(zip(freqs, times))

def generate_hashes(peaks, fan_value=FAN_VALUE):
    fingerprints = []
    for i in range(len(peaks)):
        f1, t1 = peaks[i]
        for j in range(1, fan_value):
            if i + j >= len(peaks):
                break
            f2, t2 = peaks[i + j]
            delta_t = t2 - t1
            if MIN_HASH_TIME_DELTA <= delta_t <= MAX_HASH_TIME_DELTA:
                h = hash((f1, f2, delta_t))
                fingerprints.append(((f1, f2, delta_t), t1))
    return fingerprints