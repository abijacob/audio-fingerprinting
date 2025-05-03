import time
import argparse
from main import build_db, recognize

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--music_folder', required=True)
    p.add_argument('--db_path', required=True)
    p.add_argument('--query_path', required=True)
    args = p.parse_args()

    print("→ Timing DB build...")
    t0 = time.perf_counter()
    build_db(args.music_folder, args.db_path)
    t1 = time.perf_counter()
    print(f"DB build time: {t1-t0:.3f} s\n")

    print("→ Timing recognition...")
    t2 = time.perf_counter()
    song, conf = recognize(args.query_path, args.db_path)
    t3 = time.perf_counter()
    print(f"Recognition time: {t3-t2:.3f} s → {song} ({conf:.1%})")
