import os
import pickle
from fingerprint import load_audio, get_spectrogram_peaks, generate_hashes

SONG_DIR = "songs"
DB_PATH = "db/fingerprints.pkl"

database = {}

for file in os.listdir(SONG_DIR):
    if not file.endswith(".mp3"):
        continue
    path = os.path.join(SONG_DIR, file)
    print(f"Processing {file}...")
    y = load_audio(path)
    peaks = get_spectrogram_peaks(y)
    hashes = generate_hashes(peaks)
    song_id = file
    for h, offset in hashes:
        if h not in database:
            database[h] = []
        database[h].append((song_id, offset))

with open(DB_PATH, 'wb') as f:
    pickle.dump(database, f)