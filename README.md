# OROMOTOR ASYMMETRY SYSTEM (OAS)
This is not a comprehensive readme file but simply shows the order of how OAS processes facial landmarks.

## OAS PROCESS:

```mermaid
flowchart TD
    1[OpenFace Landmarks] --> 2[Anchor Calculation]
    2 --> 3[Landmark Centering]
    3 -.-> 4[Optional Pose Correction]
    3 --> 5[Landmark Euclidean Distance Calculation]
    4 -.-> 5
    5 --> 6[Landmark Angle Calculation]
    6 --> 7[Curves]
    7 --> 8[Lip Curve Fitting]
    7 --> 9[Lip Curve Integration -- aka Mouth Area Calculation]
    8 --> 10[Wide CSV Output]
    9 --> 10
    3 --> 10
    4 -.-> 10
    5 --> 10
    6 --> 10
    