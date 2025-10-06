GENERAL_COLS = [
    'frame','x_outer','x_outer_uncertainty','x_inner','x_inner_uncertainty',
    'y_outer','y_outer_uncertainty','y_inner','y_inner_uncertainty',
    'x_anchor','x_anchor_uncertainty','y_anchor','y_anchor_uncertainty'
]

CENTRED_COLS = (
    ["frame"]
    + [f"x_{i}" for i in range(48, 68)]
    + [f"y_{i}" for i in range(48, 68)]
)

DISTANCE_COLS = (
    ["frame"]
    + [f"d_{i}" for i in range(48, 68)]
)

CURVE_COEFF_COLS = [
    "frame","region","degree",
    "Ax","Bx","Cx","Dx","Ay","By","Cy","Dy",
    "X0","Y0","X1","Y1","X2","Y2","X3","Y3",
]

ANCHOR_COLS = [
"frame",
                "pose_Rx", "pose_Ry", "pose_Rz",
                "x_outer", "x_outer_uncertainty",
                "x_inner", "x_inner_uncertainty",
                "y_outer", "y_outer_uncertainty",
                "y_inner", "y_inner_uncertainty",
                "x_anchor", "x_anchor_uncertainty",
                "y_anchor", "y_anchor_uncertainty"
]