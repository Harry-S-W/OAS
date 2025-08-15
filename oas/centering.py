from pathlib import Path
import math
from typing import Tuple, List, Optional
import pandas as pd
from tqdm import tqdm

from .anchor_point import Centering
from .schemas import CENTRED_COLS
from .io import ensure_dir, header_if_empty

def _unpack_xy(pt) -> Tuple[float, float]:
    if pt is None:
        return math.nan, math.nan
    try:
        return float(pt[0]), float(pt[1])
    except Exception:
        return math.nan, math.nan

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
        print("⚠️ centred_landmarks.csv has data. Append? (y/N): ", end="")
        if input().strip().lower() != "y":
            print("Aborting."); return

    header_if_empty(centred_csv, CENTRED_COLS)

    anchors_df = pd.read_csv(anchors_csv)
    in_df = pd.read_csv(input_file)
    total = len(in_df)
    if end is None or end > total:
        end = total

    for row in tqdm(range(start, end), desc="Centering", unit="frame"):
        try:
            xa = float(anchors_df.loc[row, "x_anchor"])
            ya = float(anchors_df.loc[row, "y_anchor"])

            pts = Centering(input_file, row, True).center_with_anchor(xa, ya)  # list of (x,y)
            xs: List[float] = []
            ys: List[float] = []
            for i in range(20):  # landmarks 48..67
                x, y = _unpack_xy(pts[i] if i < len(pts) else None)
                xs.append(x); ys.append(y)

            rec = {"frame": int(row)}
            rec.update({f"x_{i}": xs[i - 48] for i in range(48, 68)})
            rec.update({f"y_{i}": ys[i - 48] for i in range(48, 68)})

            pd.DataFrame([rec]).to_csv(centred_csv, mode="a", header=False, index=False)

        except Exception as e:
            print(f"Error on row {row}: {e}")

    print(f"Centered → {centred_csv.resolve()}")