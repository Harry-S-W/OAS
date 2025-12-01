"""
Measures the change in asymmetric change acceleration (basically how fast the mouth moves asymmetrically)

This file does a few things
    1. Measures the velocity of individual landmarks
    2. Measure the velocity of lip curvature
    3. Measure the velocity of area (both types)

- Very useful for detecting things like motor planning errors
"""

from pathlib import Path
from typing import List, Optional
import pandas as pd


from mosaic.complex_measurements.temporal.velocity.landmark_velocity import LandmarkVelocity
from mosaic.config import OUTER_QUAD_AREA, INNER_QUAD_AREA, OUTER_BIO_AREA, INNER_BIO_AREA, INNER_BEZIER_CURVES, OUTER_BEZIER_CURVES

class run:
    def __init__(self):
        pass


    def run_landmark_velocity(self, input_file: str, output_file: Path, *, force: bool=False, start: int=0, end: Optional[int]=None):
        """
        This function just runs the velocity code for landmark, area, and curves
        """

        df = pd.read_csv(input_file)

        # LANDMARK VELOCITY:
        landmarks = LandmarkVelocity(df)

        # will finish

    def run_curve_velocity(self):
        pass

    def run_area_velocity(self):
        pass

