"""
This is the most important command file as it runs openface

It has calibration as an option
"""

from oas.core_measurements.landmarks.landmarks import run as run_landmarks
from oas.core_measurements.anchor.anchors import run as run_anchors
from oas.core_measurements.angles.angles import run as run_angles
from oas.core_measurements.area.bio_based_area.bio_area_run import run as run_bio_area
from oas.core_measurements.area.quadrant_based_area.quadrant_area_run import run as run_quad_area
from oas.core_measurements.centering.centering import run as run_centering
from oas.core_measurements.curves.curves import export_curve_coefficients as run_curve_fitting
from oas.core_measurements.euclidean_distance.euclidean import run as run_euclidean_distance
from oas.core_measurements.pose_correction.pose import run as run_pose_correction
from oas.io import initialize_csvs

import os
from pathlib import Path
from oas.Session.session_manager import SessionManagement

class TrialRun:
    def __init__(self):
        # to get trial path we have to confirm they are in a trial
        self.session = SessionManagement

        self.session.require_trial()
        self.trial_path = self.session._read_session().get("currentTrial")
        print("RUNNING TRIAL THINGY THING")

    @staticmethod
    def _check_calibration(trial_path=None):
        """I think for now caliration will be an optional thing where we will check for calibratuon and inform the user
        that if they do not calibrate, X and Y SD will be set at 0.5

        for now, so I can get back to coding OAS, it will not check calibration and will assume 0.5px for x/y SD"""

        return "CALIBRATED"

    @staticmethod
    def _run_oas(trial_path):

        """
        I NEED TO ADD THE OPTION TO HAVE POSE AND FORCE BUT FOR NOW I WILL HAVE THEM AS CONST TRUE
        trial_path = outpath

        also the input file is hard coded just so I can test it

        """

        file = "/Users/harrywoodhouse/Desktop/OAS/OAS-Engine/data/test-data/v15044gf0000d1dlc67og65r2deqmhd0.csv"
        file_name = os.path.basename(file).split('.')[0]
        trial_path = Path(trial_path)
        out_path = initialize_csvs(file_name, trial_path, force=True)

        # ANCHOR MODULE

        run_anchors(file, out_path, pose_corr=True, force=True)

        # RUNNING LANDMARK UNCERTAINTY

        run_landmarks(file, out_path, force=True)

        # RUNNING CENTERING MODULE

        run_centering(file, out_path, force=True, pose_corr=True)

        # RUNNING POSE CORRECTION

        #if args.pose == True:
        run_pose_correction(out_path, out_path, force=True)

        # RUNNING EUCLIDEAN DISTANCE CALC

        run_euclidean_distance(out_path, out_path, force=True)

        # RUNNING ANGLE CALC

        run_angles(out_path, out_path, force=True)

        # RUNNING CURVE FITTING

        run_curve_fitting(out_path, out_path, force=True)

        # RUNNING QUADRANT BASED AREA

        run_quad_area(out_path, out_path, force=True)

        # RUNNING BIO BASED AREA

        run_bio_area(out_path, out_path, force=True)






