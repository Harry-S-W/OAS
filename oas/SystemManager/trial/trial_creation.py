"""
This file is to create participant folders
"""

import os

class TrialCreation:
    def __init__(self):
        pass

    def creating_trial_directory(self, participant_dir: str, ID: str = None):
        # I am gonna make it so they can submit a string of trials and then make a bunch of participant folders that way

        trial = [i.strip() for i in ID.split(",")]

        trial_directories = []

        for trial_id in trial:

            trial_dir = os.path.join(participant_dir, trial_id)
            try:
                os.mkdir(trial_dir)
                trial_directories.append(participant_dir)

            except RuntimeError as e:
                if os.path.exists(participant_dir):
                    print(
                        f"Trial {trial_id} already exists in this project")
                else:
                    print("Unknown error in creating participant directory."
                          f"{e}")

        return trial_directories
