# Audio Fingerprinting Project

A minimal audio‐fingerprinting system that can identify a short AIFF/WAV audio clip by matching it against a pre‐built database of full tracks. This project demonstrates:

- Building a fingerprint database from a folder of audio files  
- Recognizing query clips with a hashed‐peak‐pair approach  
- Measuring runtime performance of both indexing and recognition  
- Automated tests for correctness


## Table of Contents

1. [Features](#features)  
2. [Directory Structure](#directory-structure)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [1. Build the Fingerprint Database](#1-build-the-fingerprint-database)  
   - [2. Recognize a Query Clip](#2-recognize-a-query-clip)  
   - [3. Benchmark Timings](#3-benchmark-timings)  
6. [Testing](#testing)  
7. [How It Works](#how-it-works)  
8. [Configuration Parameters](#configuration-parameters)  
9. [Troubleshooting](#troubleshooting)  
10. [License](#license)  


## Features

- **Offline Indexing**: Fingerprints every `.wav`, `.aif`, or `.aiff` file in a directory.  
- **Fast Lookup**: Uses a hash → list mapping for O(1) average‐time fingerprint matching.  
- **Robust Recognition**: Votes on matching time‐offsets to select the best song match.  
- **Performance Measurement**: Built‐in script to time both indexing and recognition.  
- **Automated Tests**: Pytest suite for unit tests and end-to-end validation.


## Directory Structure

audio-fingerprinting/ 
├── audio-files/ 
# Full‐length .aiff/.wav files are stored here 
│ ├── full-audiotracks/ 
# Short sample .aif/.wav clips are stored here 
│ └── test-samples/ 
# CLI to build & recognize fingerprints 
├── main.py 
# Script to benchmark build & recognition times 
├── runtime.py 
# Pytest suite for automated testing 
├── tests.py 
└── README.md 
