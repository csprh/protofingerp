import pickle
from collections import Counter
from fingerprint import load_audio, get_spectrogram_peaks, generate_hashes

DB_PATH = "db/fingerprints.pkl"
QUERY_FILE = "queries/unknown_sample.mp3"

with open(DB_PATH, 'rb') as f:
    database = pickle.load(f)

y = load_audio(QUERY_FILE)
query_peaks = get_spectrogram_peaks(y)
query_hashes = generate_hashes(query_peaks)

matches = []

for h, q_time in query_hashes:
    if h in database:
        for song_id, db_time in database[h]:
            time_diff = db_time - q_time
            matches.append((song_id, round(time_diff, -1)))

if matches:
    counter = Counter(matches)
    best_match, votes = counter.most_common(1)[0]
    print(f"Best match: {best_match[0]} with {votes} votes at offset {best_match[1]}")
else:
    print("No match found.")