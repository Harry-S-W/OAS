#!/usr/bin/env python3
import argparse
from pathlib import Path

from oas.data import initialize_csvs  # append_anchor_frame not needed yet
# from oas.centering import center_all_frames  # for later

def main():
    p = argparse.ArgumentParser(description="OAS pipeline")
    p.add_argument("--mode", required=True, choices=["init", "anchors", "centering"])
    p.add_argument("--file", help="Input landmarks CSV (for anchors/centering)")
    p.add_argument("--output-dir", default="outputs", help="Output directory")
    args = p.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "init":
        initialize_csvs(out_dir)

    elif args.mode == "anchors":
        if not args.file:
            p.error("--file is required for anchors")
        print("--mode anchors --- Not operational in OAS 1.0.0 - Please use --mode init")
        # append_anchor_frame(args.file, out_dir)

    elif args.mode == "centering":
        if not args.file:
            p.error("--file is required for centering")
        print("--mode centering --- Not operational in OAS 1.0.0 - Please use --mode init")
        # center_all_frames(args.file, out_dir)

if __name__ == "__main__":
    main()
