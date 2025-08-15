import argparse
import os.path
from pathlib import Path
from oas.io import initialize_csvs
from oas.anchors import run as run_anchors
from oas.centering import run as run_centering
from oas.curves import export_curve_coefficients

def main():
    p = argparse.ArgumentParser(description="OAS pipeline")
    p.add_argument("-m","--mode", required=True, choices=["init","anchors","centering","curves"])
    p.add_argument("-f","--file", help="Input landmarks CSV (required for anchors & centering)")
    p.add_argument("-o","--output-dir", metavar="DIR", default="outputs")
    p.add_argument("--force", action="store_true")
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--end", type=int)
    args = p.parse_args()

    out_dir = Path(args.output_dir); out_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "init":
        #initialize_csvs(out_dir, force=args.force)

        run_anchors(args.file, out_dir, force=args.force, start=args.start, end=args.end)
        centred = out_dir / "centred_landmarks.csv"
        if not centred.exists() or centred.stat().st_size < 50:
            print("\n Next: run centering to normalise landmarks.")
            print(f"   python3 oas.py -m centering -f \"{args.file}\" -o \"{out_dir}\"\n")

        if not args.file: p.error("--file is required for mode=centering")
        run_centering(args.file, out_dir, force=args.force, start=args.start, end=args.end)
        print("\n Next: run curves to calculate curves and curve area.")
        print(f"   python3 oas.py -m curves -f \"{out_dir}\"/centred_landmarks.csv -o \"{out_dir}\"\n")

        if not centred.exists() or centred.stat().st_size == 0:
            p.error("centred_landmarks.csv missing/empty — run --mode centering first.")
        export_curve_coefficients(centred, out_dir)

        print(f"OAS Has successfully ran! Please check {out_dir}")

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

if __name__ == "__main__":
    main()