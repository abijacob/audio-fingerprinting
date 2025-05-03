import numpy as np
import soundfile as sf
from main import compute_spectrogram, detect_peaks, generate_hashes, build_db, recognize

def test_spectrogram_shape():
    #1-second 440Hz tone
    y = np.sin(2 * np.pi * 440 * np.linspace(0,1,8000))
    S = compute_spectrogram(y)
    assert S.ndim == 2
    assert S.shape[0] == 4096//2 + 1

def test_peak_and_hash_empty():
    #all-zero spectrogram yields no peaks or hashes
    S = np.zeros((20,20))
    peaks = detect_peaks(S, amp_min=1)
    assert peaks == []
    hashes = generate_hashes(peaks, fan_value=1, max_dt=5)
    assert hashes == []

def test_end_to_end(tmp_path):
    #create two AIFF files: 440Hz vs 880Hz
    t = np.linspace(0,1,8000)
    tone1 = 0.5 * np.sin(2 * np.pi * 440 * t)
    tone2 = 0.5 * np.sin(2 * np.pi * 880 * t)

    #set up dirs
    full = tmp_path/'audio-files'/'full-audiotracks'
    test = tmp_path/'audio-files'/'test-samples'
    full.mkdir(parents=True)
    test.mkdir()
    #write AIFFs
    sf.write(str(full/'tone1.aiff'), tone1, 8000)
    sf.write(str(full/'tone2.aiff'), tone2, 8000)
    #copy tone1 as query clip
    sf.write(str(test/'tone1_clip.aiff'), tone1, 8000)

    dbpath = tmp_path/'fingerprints.pkl'
    build_db(str(full), str(dbpath), amp_min=1, fan_value=1, max_dt=10)
    song, conf = recognize(str(test/'tone1_clip.aiff'), str(dbpath),
                            amp_min=1, fan_value=1, max_dt=10)
    assert song == 'tone1'
    assert conf > 0

if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
