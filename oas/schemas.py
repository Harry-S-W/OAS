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








'''
CSV FORMATTER FOR TOTAL OAS OUTPUT 

___

___

'''

# CUBIC CURVE FORMATTER:


CUBIC_CURVES = {
    "UR": ["A","B","C","D"],
    "UL": ["A","B","C","D"],
    "LR": ["A","B","C","D"],
    "LL": ["A","B","C","D"]
}

def cubic_curve_col_func():
    cubic_curve_cols = []
    for quad in ("UR", "UL", "LR", "LL"):
        cubic_curve_cols += [f"{quad}_{ax}{coord}"
                             for ax in "ABCD"
                             for coord in ("x", "y")]
        cubic_curve_cols += [f"{quad}_X{i}" for i in range(4)]
        cubic_curve_cols += [f"{quad}_Y{i}" for i in range(4)]

    return cubic_curve_cols

# CUBIC CURVE UNCERTAINTY FORMATTER

def cubic_curve_col_unc():
    cubic_curve_uncertainty_cols = []
    for quad in ("UR", "UL", "LR", "LL"):
        cubic_curve_uncertainty_cols += [f"{quad}_{ax}{coord}_unc"
                                         for ax in "ABCD"
                                         for coord in ("x", "y")]
        cubic_curve_uncertainty_cols += [f"{quad}_X{i}_unc" for i in range(4)]
        cubic_curve_uncertainty_cols += [f"{quad}_Y{i}_unc" for i in range(4)]

    return cubic_curve_uncertainty_cols

# QUADRATIC CURVES FORMATTER

QUADRATIC_CURVES = {
    "UR": ["A","B","C"],
    "UL": ["A","B","C"],
    "LR": ["A","B","C"],
    "LL": ["A","B","C"]
}

def quadratic_curve_col_func():
    quadratic_curve_cols = []
    for quad in ("IUR", "IUL", "ILR", "ILL"):
        quadratic_curve_cols += [f"{quad}_{ax}{coord}"
                                 for ax in "ABC"
                                 for coord in ("x", "y")]
        quadratic_curve_cols += [f"{quad}_X{i}" for i in range(3)]
        quadratic_curve_cols += [f"{quad}_Y{i}" for i in range(3)]

    return quadratic_curve_cols

# QUADRATIC CURVE UNCERTAINTY FORMATTER

def quadratic_curve_col_unc():
    quadratic_curve_uncertainty_cols = []
    for quad in ("IUR","IUL","ILR","ILL"):
        quadratic_curve_uncertainty_cols += [f"{quad}_{ax}{coord}_unc"
                             for ax in "ABC"
                             for coord in ("x","y")]
        quadratic_curve_uncertainty_cols += [f"{quad}_X{i}_unc" for i in range(3)]
        quadratic_curve_uncertainty_cols += [f"{quad}_Y{i}_unc" for i in range(3)]

    return quadratic_curve_uncertainty_cols

WIDE_CSV_STRUCTURE = (
    ["frame", "pose_correction", "x_anchor", "x_unc", "y_anchor", "y_unc", # int, bool, px, px, px, px
    "pose_Rx", "pose_Ry", "pose_Rz"] # rad, rad, rad
    +[f"x_{i}" for i in range(48, 68)] # px
    +[f"y_{i}" for i in range(48, 68)] # px
    +[f"d_{i}" for i in range(48, 68)] # px
    +[f"theta_{i}" for i in range(48, 68)] # rad

    # uncertainty for x,y,d,theta

    + [f"x_{i}_unc" for i in range(48, 68)] # px
    + [f"y_{i}_unc" for i in range(48, 68)] # px
    + [f"d_{i}_unc" for i in range(48, 68)] # px
    + [f"theta_{i}_unc" for i in range(48, 68)] # rad

    # curves (lots of columns - maybe try to find a better way to store

    # CUBIC/QUADRATIC CURVES

    + cubic_curve_col_func() # int
    + quadratic_curve_col_func() # int

    # CUBIC/QUADRATIC CURVES UNCERTAINTY

    + cubic_curve_col_unc() # int
    + quadratic_curve_col_unc() # int


    # MOUTH AREA

    + ["O_Q1", "O_Q2", "O_Q3", "O_Q4"] # Outer area (entire mouth but based on outer landmarks/curves) - px
    + ["I_Q1", "I_Q2", "I_Q3", "I_Q4"] # Inner area (Based on inner landmarks/curves so sort of the open area of the mouth) - px

    # MOUTH AREA UNCERTAINTY

    + ["O_Q1_unc", "O_Q2_unc", "O_Q3_unc", "O_Q4_unc"] # px
    + ["I_Q1_unc", "I_Q2_unc", "I_Q3_unc", "I_Q4_unc"] # px

)

