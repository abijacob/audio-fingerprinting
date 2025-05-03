import os
import pickle
from collections import defaultdict, Counter

import numpy as np
import librosa

#Spectrogram & Peak Detection
def compute_spectrogram(y, n_fft=4096, hop_length=512):
    return np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))

def detect_peaks(S, amp_min=10):
    peaks = []
    F, T = S.shape
    for t in range(1, T-1):
        for f in range(1, F-1):
            v = S[f, t]
            if v < amp_min:
                continue
            if v == S[f-1:f+2, t-1:t+2].max():
                peaks.append((t, f))
    return peaks

#Hash Generation
def hash_function(f1, delta_f, dt):
    #pack into 32-bit int
    return (f1 & 0xFFFF) << 16 | (delta_f & 0xFF) << 8 | (dt & 0xFF)

def generate_hashes(peaks, fan_value=5, max_dt=50):
    hashes = []
    for i in range(len(peaks)):
        t1, f1 = peaks[i]
        cnt = 0
        for (t2, f2) in peaks[i+1:]:
            dt = t2 - t1
            if dt <= 0 or dt > max_dt:
                continue
            h = hash_function(f1, f2 - f1, dt)
            hashes.append((h, t1))
            cnt += 1
            if cnt >= fan_value:
                break
    return hashes

#Database Construction
def build_db(music_folder, db_path, amp_min=10, fan_value=5, max_dt=50):
    AUDIO_EXT = ('.wav', '.aif', '.aiff')
    db = defaultdict(list)
    for root, _, files in os.walk(music_folder):
        for fn in files:
            if not fn.lower().endswith(AUDIO_EXT):
                continue
            song_id = os.path.splitext(fn)[0]
            path = os.path.join(root, fn)
            print(f"  → Fingerprinting {song_id}")
            y, _ = librosa.load(path, sr=8000, mono=True)
            S = compute_spectrogram(y)
            peaks = detect_peaks(S, amp_min)
            for h, t in generate_hashes(peaks, fan_value, max_dt):
                db[h].append((song_id, t))
    with open(db_path, 'wb') as f:
        pickle.dump(dict(db), f)
    print(f"Database built and saved to {db_path}")

#Query Recognition
def recognize(query_path, db_path, amp_min=10, fan_value=5, max_dt=50):
    with open(db_path, 'rb') as f:
        db = pickle.load(f)
    y, _ = librosa.load(query_path, sr=8000, mono=True)
    S = compute_spectrogram(y)
    peaks = detect_peaks(S, amp_min)
    q_hashes = generate_hashes(peaks, fan_value, max_dt)

    votes = Counter()
    for h, t_q in q_hashes:
        for song_id, t_ref in db.get(h, []):
            votes[(song_id, t_ref - t_q)] += 1

    if not votes:
        return None, 0.0
    (best_song, _), best_count = votes.most_common(1)[0]
    return best_song, best_count / len(q_hashes)

#CLI Entrypoint
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd', required=True)

    b = sub.add_parser('build_db')
    b.add_argument('--music_folder', required=True,
                   help="Path to audio-files/full-audiotracks")
    b.add_argument('--db_path', required=True,
                   help="Output path for fingerprints.pkl")

    r = sub.add_parser('recognize')
    r.add_argument('--query_path', required=True,
                   help="Path to test-samples/*.aif clip")
    r.add_argument('--db_path', required=True,
                   help="Path to existing fingerprints.pkl")

    args = p.parse_args()
    if args.cmd == 'build_db':
        build_db(args.music_folder, args.db_path)
    else:
        song, conf = recognize(args.query_path, args.db_path)
        if song:
            print(f"Recognized: {song} (confidence {conf:.1%})")
        else:
            print("No match found.")
