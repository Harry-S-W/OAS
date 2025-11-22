"""

FOR NOW, it just makes the uncertainty for x/y = +/- 0.5px

"""

import pandas as pd
from pathlib import Path

class XYUncertainty:
    def __init__(self, value: float = 0.5):
        self.value = float(value)

    def build_updates(self, frames_index: pd.Index):
        updates = pd.DataFrame(index=frames_index)
        for i in range(48, 68):
            updates[f"x_{i}_unc"] = self.value
            updates[f"y_{i}_unc"] = self.value
        return updates
