from pathlib import Path
import pandas as pd
from tqdm import tqdm
import math
from oas.anchor.anchor_point import Anchor
from oas.schemas import ANCHOR_COLS
from oas.io import ensure_dir, header_if_empty


def _get_pose_row(df: pd.DataFrame, row: int):
    """Return (Rx,Ry,Rz) for this row. Accepts either pose_R* or bare R* column names."""
    def pick(col_a, col_b):
        if col_a in df.columns: return df.loc[row, col_a]
        if col_b in df.columns: return df.loc[row, col_b]
        return math.nan
    Rx = pick("pose_Rx", "Rx")
    Ry = pick("pose_Ry", "Ry")
    Rz = pick("pose_Rz", "Rz")
    return float(Rx) if pd.notna(Rx) else math.nan, \
           float(Ry) if pd.notna(Ry) else math.nan, \
           float(Rz) if pd.notna(Rz) else math.nan

def run(input_file: str, output_dir: Path, *, force: bool=False, start: int=0, end: int|None=None) -> None:
    output_dir = ensure_dir(output_dir)
    out_csv = output_dir / "anchors.csv"

    # prompt before appending unless --force
    if out_csv.exists() and out_csv.stat().st_size > 0 and not force:
        print("Anchors.csv has data. Append? (y/N): ", end="")
        if input().strip().lower() != "y":
            print("Aborting."); return

    # Write header once (now includes pose columns)
    header_if_empty(out_csv, ANCHOR_COLS)

    df = pd.read_csv(input_file)
    A = Anchor(df, filtering=True)

    total = len(df)
    if end is None or end > total:
        end = total
    if start < 0:
        start = 0
    if start >= end:
        print("Nothing to do: start >= end.")
        return

    for row in tqdm(range(start, end), desc="Anchors", unit="frame"):
        try:
            d = A.get_all_anchors(row)
            Rx, Ry, Rz = _get_pose_row(df, row)

            rec = {
                "frame": int(row),
                "pose_Rx": Rx, "pose_Ry": Ry, "pose_Rz": Rz,
                "x_outer": d["x_outer"][0], "x_outer_uncertainty": d["x_outer"][1],
                "x_inner": d["x_inner"][0], "x_inner_uncertainty": d["x_inner"][1],
                "y_outer": d["y_outer"][0], "y_outer_uncertainty": d["y_outer"][1],
                "y_inner": d["y_inner"][0], "y_inner_uncertainty": d["y_inner"][1],
                "x_anchor": d["x_anchor"][0], "x_anchor_uncertainty": d["x_anchor"][1],
                "y_anchor": d["y_anchor"][0], "y_anchor_uncertainty": d["y_anchor"][1],
            }

            # Append one row, no header (already written)
            pd.DataFrame([rec], columns=ANCHOR_COLS).to_csv(out_csv, mode="a", header=False, index=False)

        except Exception as e:
            print(f"Error on row {row}: {e}")

    print("Anchors →", out_csv.resolve())
