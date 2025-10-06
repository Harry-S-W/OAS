"""



"""

from pathlib import Path
import pandas as pd
from typing import List
from tqdm import tqdm
import math
from oas.euclidean_distance.euclidean_distance import EuclideanDistance
from oas.schemas import DISTANCE_COLS
from oas.io import ensure_dir, header_if_empty

def run(input_file: str, output_dir: Path, *, force: bool=False, start: int=0, end: int|None=None) -> None:
    output_dir = ensure_dir(output_dir)
    out_csv = output_dir / "distance.csv"

    if out_csv.exists() and out_csv.stat().st_size > 0 and not force:
        print(f"{out_csv} has data. Append? (y/N): ", end="")
        if input().strip().lower() != "y":
            print("Aborting."); return

    header_if_empty(out_csv, DISTANCE_COLS)

    df = pd.read_csv(input_file)
    D = EuclideanDistance(df, filtering=True)

    total = len(df)
    if end is None or end > total:
        end = total
    if start < 0:
        start = 0
    if start >= end:
        print("Nothing to do: start >= end.")
        return

    for row in tqdm(range(start, end), desc="Euclidean Distance", unit="frame"):
        try:
            d = D.euclideanDistanceCalc(row)

            rec = {"frame": row}
            rec.update({f"d_{i}": d[i - 48] for i in range(48, 68)})

            pd.DataFrame([rec]).to_csv(out_csv, mode="a", header=False, index=False)

        except Exception as e:
            print(f"Error on row {row}: {e}")