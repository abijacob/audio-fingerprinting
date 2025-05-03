# Audio Fingerprinting Project

A minimalist Python implementation of an audio‑fingerprinting system.
Given a short **AIFF/WAV** query clip, the program matches it against a database of full‑length tracks and returns the best match plus a confidence score.


## Table of Contents

1. [Features](#features)
2. [Directory Structure](#directory-structure)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)

   1. [Build the Fingerprint Database](#51-build-the-fingerprint-database)
   2. [Recognize a Query Clip](#52-recognize-a-query-clip)
   3. [Benchmark Timings](#53-benchmark-timings)
6. [Testing](#testing)
7. [How It Works](#how-it-works)
8. [Configuration Parameters](#configuration-parameters)
9. [Troubleshooting](#troubleshooting)
10. [License](#license)


## Features

* **Offline Indexing** – fingerprints every `.wav`, `.aif`, or `.aiff` file in a folder.
* **Fast Lookup** – hash → list map enables O(1) average‑time fingerprint matching.
* **Robust Recognition** – votes on consistent time‑offsets to pick the correct track.
* **Performance Measurement** – built‑in script times both indexing and recognition.
* **Automated Tests** – Pytest suite covers unit and end‑to‑end scenarios.


## Directory Structure

audio-recognition-project/
└── audio-fingerprinting/
    ├── audio-files/
    │   ├── full-audiotracks/    # full tracks (.aiff/.wav)
    │   └── test-samples/        # short query clips (.aif/.wav)
    ├── main.py                  # CLI to build & recognize fingerprints
    ├── runtime.py               # benchmark script
    ├── tests.py                 # automated tests
    ├── run_commands.sh          # quickstart script (optional)
    └── README.md                # this file


## Requirements

* Python **3.8 or newer**
* `pip` package manager
* Tested on macOS & Ubuntu (should also work on Windows)


## Installation

# 1) Clone repository
git clone <repository_url>
cd audio-recognition-project/audio-fingerprinting

# 2) (Optional) create and activate virtualenv
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

# 3) Install dependencies
pip install numpy scipy librosa soundfile pytest


## Usage

### 5.1 Build the Fingerprint Database

python3 main.py build_db \
  --music_folder audio-files/full-audiotracks \
  --db_path fingerprints.pkl

Creates **`fingerprints.pkl`**, a pickled hash table of all track fingerprints.


### 5.2 Recognize a Query Clip

python3 main.py recognize \
  --query_path audio-files/test-samples/test-sample1.aiff \
  --db_path fingerprints.pkl

Example output:

Recognized: HonSalo-Glitch (confidence 78.5%)


### 5.3 Benchmark Timings

python3 runtime.py \
  --music_folder audio-files/full-audiotracks \
  --db_path fingerprints.pkl \
  --query_path audio-files/test-samples/test-sample1.aiff

Sample console:

→ Timing DB build...
DB build time: 2.73 s

→ Timing recognition...
Recognition time: 0.04 s → HonSalo-Glitch (78.5%)


## Testing

Run all automated tests:

pytest tests.py

You should see something like:

tests.py ...                                                [100%]


## How It Works

1. **Spectrogram** – STFT converts time‑domain audio to magnitude spectrogram.
2. **Peak Detection** – local maxima above `amp_min` are extracted as robust landmarks.
3. **Hash Generation** – each anchor peak is paired with nearby peaks to create 32‑bit hashes `(f_anchor, Δf, Δt)`.
4. **Indexing** – hashes are stored in a dict: `hash → [(song_id, time_anchor), …]`.
5. **Recognition** – fingerprint the query, look up each hash, vote on `(song_id, time_shift)`, and select the highest vote.


## Configuration Parameters

| Parameter    | Purpose                                           | Default |
| ------------ | ------------------------------------------------- | ------- |
| `n_fft`      | FFT window length (samples)                       | 4096    |
| `hop_length` | Hop between frames (samples)                      | 512     |
| `amp_min`    | Peak‑detection amplitude threshold                | 10      |
| `fan_value`  | Max neighbor peaks paired per anchor peak         | 5       |
| `max_dt`     | Max time difference between paired peaks (frames) | 50      |

Modify these in **`main.py`** if you need different settings.


## Troubleshooting

| Issue                                      | Fix                                                                                                          |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **“No format specified …” writing `.aif`** | Use `.aiff` or `.wav`; SoundFile infers format from extension.                                               |
| **“No match found.”**                      | Lower `amp_min` or raise `fan_value` / `max_dt`; ensure the query clip comes from one of the indexed tracks. |
| Slow performance on large libraries        | Persist the hash table to Redis/LevelDB and shard by hash prefix.                                            |


## License

Released under the **MIT License** – see `LICENSE` for details.
