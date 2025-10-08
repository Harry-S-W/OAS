import argparse
import os.path
from pathlib import Path
from oas.io import initialize_csvs
from oas.anchor.anchors import run as run_anchors
from oas.centering.centering import run as run_centering
from oas.curves.curves import export_curve_coefficients as run_curve_fitting
from oas.euclidean_distance.euclidean import run as run_euclidean_distance
from oas.pose_correction.pose import run as run_pose_correction

def main():
    p = argparse.ArgumentParser(description="OAS pipeline")
    p.add_argument("-m","--mode", required=True, choices=["init","anchors","centering","curves", "euclidean"])
    p.add_argument("-f","--file", help="Input landmarks CSV (required for anchors & centering)")
    p.add_argument("-o","--output-dir", metavar="DIR", default="outputs")
    p.add_argument("-p","--pose", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--end", type=int)
    args = p.parse_args()

    out_dir = Path(args.output_dir); out_dir.mkdir(parents=True, exist_ok=True)
    file_name = os.path.basename(args.file).split('.')[0]

    if args.mode == "init":
        out_path = initialize_csvs(file_name, out_dir, force=args.force)

        # ANCHOR MODULE

        run_anchors(args.file, out_path, pose_corr=args.pose, force=args.force)

        # RUNNING CENTERING MODULE

        run_centering(args.file, out_path, force=args.force, pose_corr=args.pose)

        # RUNNING POSE CORRECTION

        if args.pose == True:
            run_pose_correction(out_path, out_path, force=args.force)

        # RUNNING EUCLIDEAN DISTANCE CALC

        run_euclidean_distance(out_path, out_path, force=args.force)

        # RUNNING CURVE FITTING

        run_curve_fitting(out_path, out_path, force=args.force)

        #run_anchors(args.file, out_dir, force=args.force, start=args.start, end=args.end)
        # centred = out_dir / "centred_landmarks.csv"

        """if not centred.exists() or centred.stat().st_size < 50:
            print("\n Next: run centering to normalise landmarks.")
            print(f"   python3 oas.py -m centering -f \"{args.file}\" -o \"{out_dir}\"\n")

        if not args.file: p.error("--file is required for mode=centering")
        run_centering(args.file, out_dir, force=args.force, start=args.start, end=args.end)
        print("\n Next: run curves to calculate curves and curve area.")
        print(f"   python3 oas.py -m curves -f \"{out_dir}\"/centred_landmarks.csv -o \"{out_dir}\"\n")

        if not centred.exists() or centred.stat().st_size == 0:
            p.error("centred_landmarks.csv missing/empty — run --mode centering first.")
        export_curve_coefficients(centred, out_dir)

        print(f"OAS Has successfully ran! Please check {out_dir}")"""

    elif args.mode == "anchors":
        if not args.file: p.error("--file is required for mode=anchors")
        run_anchors(args.file, out_dir, force=args.force, start=args.start, end=args.end)
        centred = out_dir / "centred_landmarks.csv"
        if not centred.exists() or centred.stat().st_size < 50:
            print("\n Next: run centering to normalise landmarks.")
            print(f"   python3 oas.py -m centering -f \"{args.file}\" -o \"{out_dir}\"\n")

    elif args.mode == "centering":
        if not args.file: p.error("--file is required for mode=centering")
        run_centering(args.file, out_dir, force=args.force, start=args.start, end=args.end)
        print("\n Next: run curves to calculate curves and curve area.")
        print(f"   python3 oas.py -m curves -f \"{out_dir}\"/centred_landmarks.csv -o \"{out_dir}\"\n")

    elif args.mode == "curves":
        centred = out_dir / "centred_landmarks.csv"
        if not centred.exists() or centred.stat().st_size == 0:
            p.error("centred_landmarks.csv missing/empty — run --mode centering first.")
        export_curve_coefficients(centred, out_dir)

    elif args.mode == "euclidean":
        landmarks = out_dir / "pose_correction.csv"
        if not landmarks.exists() or landmarks.stat().st_size == 0:
            p.error(f"{landmarks} missing/empty - run --mode curves first")

        run_euclidean_distance(args.file, out_dir, force=args.force, start=args.start, end=args.end)

"""

HOW TO USE CLI:

When running locally from command terminal, use:

> source .venv/bin/activate

Then use: 

> python -m oas.cli -m (mode) -f (input file) -o (output file) -f (force) -start (compute at row int) -end (finish at row int)

CLI testing command

python -m oas.cli -m init -f "data/test-data/v15044gf0000d1dlc67og65r2deqmhd0.csv" --force --pose

"""

if __name__ == "__main__":
    main()