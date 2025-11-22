"""

My best sort of attempt to get the standard deviation of x/y as they how they are measured is beyond the OAS system

I am gonna do it by having a sort of "calibration" section for OAS where the participant will sit still for ~5 seconds
so we can see the jitter of x and y values because this about tracking noise.

We then get the standard deviation of those ~5 seconds for x and y and that gives us delta y and delta x.

I think I will make the length custom so other people can determine how long they want their calibration for. I will
probably make a mini sort of menu thing in the CLI so at the start of -m "init" it will ask you to define the calibration
phase.
"""

import pandas as pd
from pathlib import Path
import os
import subprocess
import shutil
from oas.config import LANDMARK_PAIRS

class XYUncertainty:
    """
    Plan is:
        1. Receive a video content path
        2. Analyze that video in openface
        3. Make a list of all x/y values from 48-68
        4. Calculate the standard deviation of each x and y value from 48-68
        5. Return a dict of the x/y column name and the x/y SD
    """
    def __init__(self, input: str, output: pd.DataFrame):
        if os.path.exists(input):
            self.input = input
        else:
            raise FileNotFoundError(f"{input} is not a valid file. If it is not in a local directory, ensure you use the "
                                    f"absolute path. ")
        if input != str:
            raise TypeError(f"{input} Must be a str.")

        if isinstance(output, (str, Path)):
            self.landmarks = pd.read_csv(output)
        elif isinstance(output, pd.DataFrame):
            self.landmarks = output
        else:
            raise TypeError("src must be a CSV path or a pandas DataFrame")

    @staticmethod
    def _run_openface(video_path, outpur_path, name: str=None):
        openface_path = "/Users/harrywoodhouse/OpenFace/build/bin/FeatureExtraction" # I will make this a custom dir and keep it as like a sort of project metadata
        if name is None:
            name, _ = os.path.splitext(video_path)
        else:
            name = name +"_CALIBRATION"
        output_dir = os.path.join(outpur_path, name)
        os.makedirs(output_dir, exist_ok=True)

        # Copy video locally to output dir
        local_video_path = os.path.join(output_dir, video_path)
        shutil.copy(video_path, local_video_path)

        command = [
            openface_path,
            "-f", local_video_path,
            "-out_dir", output_dir,
            "-of", video_path,
            "-aus",
            "-pose",
            "-2Dfp",
            "-tracked"
        ]

        print(f"Running Calibration on {video_path} --> {output_dir}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode()
        stderr = result.stderr.decode()
        log_text = stdout + stderr

        if result.returncode != 0:
            raise RuntimeError(f"OpenFace failed:\n{result.stderr.decode()}")

        return output_dir, log_text


    @staticmethod
    def _get_x_y():
        pass




    """def build_updates(self, frames_index: pd.Index):
        updates = pd.DataFrame(index=frames_index)
        for i in range(48, 68):
            updates[f"x_{i}_unc"] = self.value
            updates[f"y_{i}_unc"] = self.value
        return updates"""

