"""
Centers landmarks and applies roll, yaw, and pitch correction
"""
import pandas as pd
import numpy as np
import math


class LandmarkCorrection:
    def __init__(self, file: pd.DataFrame or str, pitch: bool=False, yaw: bool=False, roll: bool=False):
        if file == str:
            self.data = pd.read_csv(file)
        elif file == pd.DataFrame:
            self.data = file
        else:
            raise ValueError("ERROR: file MUST be a string or pd.DataFrame (csv)")
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def _yaw_correction(self):
        pass
    def _pitch_correction(self):
        pass
    def _roll_correction(self):
        pass

    def landmarks(self):
        pass
