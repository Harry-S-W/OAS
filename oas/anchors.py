from pathlib import Path
import pandas as pd
from tqdm import tqdm
from .anchor_point import Anchor
from .schemas import GENERAL_COLS
from .io import ensure_dir, header_if_empty

def run(input_file: str, output_dir: Path, *, force: bool=False, start: int=0, end: int|None=None) -> None:
    output_dir = ensure_dir(output_dir)
    out_csv = output_dir / "anchors.csv"

    # prompt before appending unless --force
    if out_csv.exists() and out_csv.stat().st_size > 0 and not force:
        print("⚠️ output.csv has data. Append? (y/N): ", end="")
        if input().strip().lower() != "y":
            print("Aborting."); return

    header_if_empty(out_csv, GENERAL_COLS)

    df = pd.read_csv(input_file)
    A = Anchor(df, filtering=True)          # <-- refactored Anchor (no row in __init__)
    end = len(df) if end is None or end > len(df) else end

    for row in tqdm(range(start, end), desc="Anchors", unit="frame"):
        try:
            d = A.get_all_anchors(row)
            rec = {
                'frame': row,
                'x_outer': d['x_outer'][0], 'x_outer_uncertainty': d['x_outer'][1],
                'x_inner': d['x_inner'][0], 'x_inner_uncertainty': d['x_inner'][1],
                'y_outer': d['y_outer'][0], 'y_outer_uncertainty': d['y_outer'][1],
                'y_inner': d['y_inner'][0], 'y_inner_uncertainty': d['y_inner'][1],
                'x_anchor': d['x_anchor'][0], 'x_anchor_uncertainty': d['x_anchor'][1],
                'y_anchor': d['y_anchor'][0], 'y_anchor_uncertainty': d['y_anchor'][1],
            }
            pd.DataFrame([rec]).to_csv(out_csv, mode="a", header=False, index=False)
        except Exception as e:
            print(f"Error on row {row}: {e}")

    print("Anchors →", out_csv.resolve())

