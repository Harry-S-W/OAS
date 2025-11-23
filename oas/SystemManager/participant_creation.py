"""
This file is to create participant folders
"""

import os

class ParticipantCreation:
    def __init__(self):
        pass

    def creating_participant_directory(self, project_dir: str, ID: str = None):
        participant_dir = os.path.join(project_dir, "participants", ID)
        try:
            os.mkdir(participant_dir)
            os.mkdir(participant_dir+"/trials")
            os.mkdir(participant_dir + "/calibration")
            return participant_dir

        except OSError as e:
            if os.path.exists(participant_dir):
                print(
                    f"Participant {ID} already exists in this project")
            else:
                print("Unknown error in creating participant directory."
                      f"{e}")
