from pathlib import Path
import math
from typing import Tuple, List, Optional
import pandas as pd
from tqdm import tqdm

from oas.anchor.anchor_point import Centering
from oas.schemas import CENTRED_COLS
from oas.io import ensure_dir, header_if_empty

"""
For some reason I coded the centering function in the anchors file - so find that function in oas/anchor/anchor_point.py
"""

def _unpack_xy(pt) -> Tuple[float, float]:
    if pt is None:
        return math.nan, math.nan
    try:
        return float(pt[0]), float(pt[1])
    except Exception:
        return math.nan, math.nan

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
"""ADD POSE TO CENTERING CSV OUTPUT"""

def run(
    input_file: str,
    output_dir: Path,
    *,
    force: bool = False,
    start: int = 0,
    end: Optional[int] = None,
) -> None:
    output_dir = ensure_dir(output_dir)
    anchors_csv = output_dir / "anchors.csv"
    centred_csv = output_dir / "centred_landmarks.csv"

    if not anchors_csv.exists() or anchors_csv.stat().st_size == 0:
        raise FileNotFoundError("output.csv missing/empty — run anchors first.")

    if centred_csv.exists() and centred_csv.stat().st_size > 0 and not force:
        print("centred_landmarks.csv has data. Append? (y/N): ", end="")
        if input().strip().lower() != "y":
            print("Aborting."); return

    header_if_empty(centred_csv, CENTRED_COLS)

    in_df = pd.read_csv(input_file)  # load once
    anchors_df = pd.read_csv(anchors_csv)
    total = len(in_df)
    if end is None or end > total:
        end = total

    for row in tqdm(range(start, end), desc="Centering", unit="frame"):
        try:
            xa = float(anchors_df.loc[row, "x_anchor"])
            ya = float(anchors_df.loc[row, "y_anchor"])
            Rx, Ry, Rz = _get_pose_row(in_df, row)

            # pass DataFrame, not filename
            pts = Centering(in_df, row, True).center_with_anchor(xa, ya) # list of (x,y)
            xs: List[float] = []
            ys: List[float] = []
            for i in range(20):  # landmarks 48..67
                x, y = _unpack_xy(pts[i] if i < len(pts) else None)
                xs.append(x); ys.append(y)

            rec = {"frame": int(row), "pose_Rx": Rx, "pose_Ry": Ry, "pose_Rz": Rz}
            rec.update({f"x_{i}": xs[i - 48] for i in range(48, 68)})
            rec.update({f"y_{i}": ys[i - 48] for i in range(48, 68)})

            pd.DataFrame([rec]).to_csv(centred_csv, mode="a", header=False, index=False)

        except Exception as e:
            print(f"Error on row {row}: {e}")

    print(f"Centered → {centred_csv.resolve()}")