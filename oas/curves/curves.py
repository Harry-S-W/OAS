# oas/curves.py
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

from oas.curves.curve_fitting import CurveFitting
from oas.schemas import CURVE_COEFF_COLS
from oas.io import ensure_dir, header_if_empty


def _nonempty(p: Path) -> bool:
    return p.exists() and p.stat().st_size > 0


def export_curve_coefficients(
    centred_csv: Path | str,
    output_dir: Path,
    *,
    force: bool = False,
    start: int = 0,
    end: Optional[int] = None,
) -> None:
    """
    For each frame in centred_landmarks.csv, compute per-region polynomial coefficients
    and append rows to curves.csv with columns from CURVE_COEFF_COLS.
    """
    output_dir = ensure_dir(Path(output_dir))
    centred_csv = Path(centred_csv)
    if not centred_csv.exists() or centred_csv.stat().st_size == 0:
        raise FileNotFoundError("centred_landmarks.csv missing/empty — run centering first.")

    out_csv = output_dir / "curves.csv"

    # prompt if appending to existing non-empty unless forced
    if _nonempty(out_csv) and not force:
        print("⚠️ curves.csv already has data. Append? (y/N): ", end="")
        if input().strip().lower() != "y":
            print("Aborting."); return

    # ensure header exactly once
    header_if_empty(out_csv, CURVE_COEFF_COLS)

    df = pd.read_csv(centred_csv)
    total = len(df)
    if end is None or end > total:
        end = total
    if start < 0:
        start = 0
    if start >= end:
        print("Nothing to do: start >= end.")
        return

    records: List[Dict[str, object]] = []

    for row in tqdm(range(start, end), desc="Curves", unit="frame"):
        try:
            cf = CurveFitting(df, row=row, t=0.0)  # t unused for coeff export

            # keep iteration order stable with cf._REGIONS keys
            for region, (_, deg) in cf._REGIONS.items():
                cx, cy, pts = cf._coeffs_with_pts(region)

                # pack function_type & degree
                if deg == 3:
                    ftype = "cubic"
                    Ax, Bx, Cx, Dx = (float(cx[0]), float(cx[1]), float(cx[2]), float(cx[3]))
                    Ay, By, Cy, Dy = (float(cy[0]), float(cy[1]), float(cy[2]), float(cy[3]))
                    Pcoords = _pad_points(pts, target=4)  # P0,Q1,Q2,P3 (4 points)
                elif deg == 2:
                    ftype = "quadratic"
                    # quadratic power-basis: 3 coeffs
                    Ax, Bx, Cx, Dx = (float(cx[0]), float(cx[1]), float(cx[2]), None)
                    Ay, By, Cy, Dy = (float(cy[0]), float(cy[1]), float(cy[2]), None)
                    Pcoords = _pad_points(pts, target=4)  # P0,Q,P2,None -> still fill X3/Y3=None
                else:
                    raise ValueError(f"Unsupported degree {deg} for region {region}")

                rec: Dict[str, object] = {
                    "frame": int(row),
                    "region": region,
                    "degree": int(deg),
                    "Ax": Ax, "Bx": Bx, "Cx": Cx, "Dx": Dx,
                    "Ay": Ay, "By": By, "Cy": Cy, "Dy": Dy,
                    # control/reference points used to fit
                    "X0": Pcoords[0][0], "Y0": Pcoords[0][1],
                    "X1": Pcoords[1][0], "Y1": Pcoords[1][1],
                    "X2": Pcoords[2][0], "Y2": Pcoords[2][1],
                    "X3": Pcoords[3][0], "Y3": Pcoords[3][1],
                }
                records.append(rec)

        except Exception as e:
            print(f"Error on row {row}: {e}")

    if records:
        pd.DataFrame.from_records(records, columns=CURVE_COEFF_COLS).to_csv(
            out_csv, mode="a", header=False, index=False
        )
    print(f"Curve coefficients appended to {out_csv.resolve()}")


def _pad_points(pts: np.ndarray, target: int = 4) -> List[Tuple[Optional[float], Optional[float]]]:
    out: List[Tuple[Optional[float], Optional[float]]] = []
    for i in range(target):
        if i < len(pts):
            out.append((float(pts[i][0]), float(pts[i][1])))
        else:
            out.append((None, None))
    return out

