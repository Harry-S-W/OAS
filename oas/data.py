from pathlib import Path
import pandas as pd
from tqdm import tqdm
from .anchor.anchor_point import Anchor  # your class

GENERAL_COLS = [
    'frame','x_outer','x_outer_uncertainty','x_inner','x_inner_uncertainty',
    'y_outer','y_outer_uncertainty','y_inner','y_inner_uncertainty',
    'x_anchor','x_anchor_uncertainty','y_anchor','y_anchor_uncertainty'
]

CENTRED_COLS = (
    ["frame"]
    + [f"x_{i}" for i in range(48, 68)]
    + [f"y_{i}" for i in range(48, 68)]
)
# if you prefer interleaved x,y columns like before, rebuild this list accordingly

CURVE_COEFF_COLS = [
    "frame","region","degree",
    "Ax","Bx","Cx","Dx","Ay","By","Cy","Dy",
    "X0","Y0","X1","Y1","X2","Y2","X3","Y3",
]

def initialize_csvs(output_dir: Path, force: bool = False) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "outputs": output_dir / "outputs.csv",
        "centred": output_dir / "centred_landmarks.csv",
        "curves": output_dir / "curves.csv",
    }

    existing = [p for p in paths.values() if p.exists()]

    if existing and not force:
        print("The following files already exist and will be overwritten:")
        for p in existing:
            print(f"   - {p.name}")
        proceed = input("Do you want to continue? (y/N): ").strip().lower()
        if proceed != "y":
            print("Aborting — no files overwritten.")
            return
    elif existing and force:
        # make overwrite explicit & visible
        for p in existing:
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    # (Re)create with headers
    pd.DataFrame(columns=GENERAL_COLS).to_csv(paths["outputs"], index=False)
    pd.DataFrame(columns=CENTRED_COLS).to_csv(paths["centred"], index=False)
    pd.DataFrame(columns=CURVE_COEFF_COLS).to_csv(paths["curves"], index=False)

def _nonempty(fp: Path) -> bool:
    return fp.exists() and fp.stat().st_size > 0


def append_anchor_frame(input_file: str, output_dir: Path, *, force: bool = False,
                        start: int = 0, end: int | None = None) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "output.csv"

    # If output.csv already has content and user didn't force, warn
    if _nonempty(out_path) and not force:
        print("output.csv already exists and has data.")
        ans = input("Append to it? (y/N): ").strip().lower()
        if ans != "y":
            print("Aborting — nothing written.")
            return

    # If the file does NOT exist or is empty, we'll write headers on first write
    write_headers = not _nonempty(out_path)
    if write_headers and not out_path.exists():
        # ensure consistent column order if this is the very first write
        pd.DataFrame(columns=GENERAL_COLS).to_csv(out_path, index=False)
        write_headers = False  # already wrote the header line above

    df_in = pd.read_csv(input_file)
    A = Anchor(df_in, filtering=True)
    total = len(df_in)
    if end is None or end > total:
        end = total

    for row in tqdm(range(len(df_in)), desc="Anchors", unit="frame"):
        try:
            data = A.get_all_anchors(row)  # <- pass row here
            record = {
                'frame': row,
                'x_outer': data['x_outer'][0], 'x_outer_uncertainty': data['x_outer'][1],
                'x_inner': data['x_inner'][0], 'x_inner_uncertainty': data['x_inner'][1],
                'y_outer': data['y_outer'][0], 'y_outer_uncertainty': data['y_outer'][1],
                'y_inner': data['y_inner'][0], 'y_inner_uncertainty': data['y_inner'][1],
                'x_anchor': data['x_anchor'][0], 'x_anchor_uncertainty': data['x_anchor'][1],
                'y_anchor': data['y_anchor'][0], 'y_anchor_uncertainty': data['y_anchor'][1],
            }
            pd.DataFrame([record]).to_csv(out_path, mode="a", header=False, index=False)
        except Exception as e:
            print(f"Error on row {row}: {e}")

    print(f"Anchors appended to {out_path.resolve()}")
