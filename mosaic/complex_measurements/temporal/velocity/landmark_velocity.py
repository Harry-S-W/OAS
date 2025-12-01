"""
this script just measures the velocity of landmarks tracking the mouth
"""
from pathlib import Path
import pandas as pd
from mosaic.config import LANDMARK_PAIRS

class LandmarkVelocity:
    def __init__(self, src: str | Path | pd.DataFrame):
        if isinstance(src, (str, Path)):
            self.landmarks = pd.read_csv(src)
        elif isinstance(src, pd.DataFrame):
            self.landmarks = src
        else:
            raise TypeError("landmarks must be a CSV path or a pandas DataFrame")

    @staticmethod
    def _getting_data(src, row: int) -> dict | TypeError:
        if isinstance(row, int):
            pass
        elif  isinstance(row, str):
            row = int(row)
        else:
            return TypeError(f"row must be an int or str - not {type(row)}")

        df = src.set_index("frame")

        data = {}

        df_row = df.loc[row]
        for X_, Y_ in LANDMARK_PAIRS:
            x = df_row[X_]
            y = df_row[Y_]
            data.update({X_: x, Y_: y})

        return data

    def landmark_velocity(self, row: int) -> dict | TypeError:
        """
        in this function we get the velocity by comparing the current frame/row to the frame/row that came before it

        on row/frame 1 we can just return 0 because there is nothing to compare
        """
        if isinstance(row, int):
            pass
        elif  isinstance(row, str):
            row = int(row)
        else:
            return TypeError(f"row must be an int or str - not {type(row)}")

        current_row = self._getting_data(self.landmarks, row)
        if row == 1:
            return 0
        else:
            previous_row = self._getting_data(self.landmarks, row - 1)

        # I think it is best to return a dict of velocity like {x_48: 0.2, y_48: 0.73.....} sort of thing

        velocity = {}

        for X_, Y_ in LANDMARK_PAIRS:
            curr_x = current_row[X_]
            curr_y = current_row[Y_]

            prev_x = previous_row[X_]
            prev_y = previous_row[Y_]

            velocity_x = curr_x - prev_x
            velocity_y = curr_y - prev_y

            velocity.update({X_: velocity_x, Y_: velocity_y})

        return velocity



