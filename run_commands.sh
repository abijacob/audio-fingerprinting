# run_commands.sh
#
# Quickstart for Audio Fingerprinting Project:
# 1) Install deps
# 2) Run tests
# 3) Build the fingerprint DB
# 4) Recognize a sample clip
# 5) Benchmark timings
#
# Usage:
#   chmod +x run_commands.sh
#   ./run_commands.sh

set -e

echo "=== 1) (Optional) Create & activate venv ==="
echo "python3 -m venv venv"
echo "source venv/bin/activate  # macOS/Linux"
echo "venv\\Scripts\\activate    # Windows"
echo

echo "=== 2) Install dependencies ==="
pip install numpy scipy librosa soundfile pytest
echo

echo "=== 3) Run automated tests ==="
pytest tests.py
echo

echo "=== 4) Build fingerprint database ==="
python3 main.py build_db \
  --music_folder audio-files/full-audiotracks \
  --db_path fingerprints.pkl
echo

echo "=== 5) Recognize a test clip ==="
python3 main.py recognize \
  --query_path audio-files/test-samples/test-sample1.aiff \
  --db_path fingerprints.pkl
echo

echo "=== 6) Benchmark build & recognition times ==="
python3 runtime.py \
  --music_folder audio-files/full-audiotracks \
  --db_path fingerprints.pkl \
  --query_path audio-files/test-samples/test-sample1.aiff
echo

echo "All steps completed successfully!"
