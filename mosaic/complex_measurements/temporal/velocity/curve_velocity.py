"""
Takes the velocity of the change in curvature using the curve points and coeffs


WHAT WE CAN DO:

To see how much the curve just moves overall, we can calculate the current curve and the curve before it and
calculate the area in between the two curves

Then, to calculate how much the curve changes, we can compare the slop of each curve and get the difference
"""

from pathlib import Path
import pandas as pd

class CurveVelocity:
    def __init__(self, src: str | Path | pd.DataFrame, curve_data) -> str | None:
        if isinstance(src, str):
            try:
                self.landmarks = pd.read_csv(src)
                return
            except TypeError as e:
                return f"File must be a csv format\n{e}"
        elif isinstance(src, Path):
            try:
                self.landmarks = pd.read_csv(src)
                return
            except TypeError as e:
                return f"File must be a csv format\n{e}"

        elif isinstance(src, pd.DataFrame):
            self.landmarks = src

        self.curve_vals = curve_data


    def _getting_data(self, row):
        if isinstance(row, int):
            pass
        elif isinstance(row, str):
            row = int(row)
        else:
            return TypeError(f"row must be an int or str - not {type(row)}")

        df = self.landmarks.set_index("frame")
        df_row = df.loc[row]

        data = {}
        for i in self.curve_vals:
            curve_val = df_row[i]
            data.update({i: curve_val})

        return data


    def curve_area_calculation(self, curve_data):
        """
        This function essentially takes the curve in the current frame and the curve from the previous frame and
        calculates the area inbetween the two curves. This is then used to see how the curve has increased over
        time.

        Mapping overtime, we can see how active the curves are over time. A hilly graph means the curve moved a lot
        and a flatter graph means the curve didn't move much at all
        """
        pass

    def curve_slope_calculator(self, curve_data):
        """
        This calculates the slop of the curve

        Mapping over time we could see how curvy the curve is over time - a hillier graph means that curve was more curvey
        over time or saw increases/decreases in curviness and a flatter graph indicates the curve didn't change its curvature very much
        """
        pass

    def mid_curve(self, curve_data):
        """
        This calculates how the curve has moved from the previous frame to the current by
        subtracting the previous curve from the current.

        When mapping over time, we can see how much the curve changes and see if it changes a lot or a littl (still
        working on th logic for this)
        """
        pass
