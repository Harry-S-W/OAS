""""
Anchor Pairs:
    X BASED:
    [
        ("x_50", "x_52"),
        ("x_49", "x_53")
    ]

    Y BASED:
    [
        ("y_50", "y_58"),
        ("y_51", "y_57")
    ]

FOR CONSISTENCY: ORDER GOES AS FOLLOWING:
    TOP --> BOTTOM
    LEFT --> RIGHT
    FROM *CAMERA* PERSPECTIVE
"""

X_OUTER_BASED_ANCHOR_PAIRS = [
    ("x_50", "x_52"),
    ("x_49", "x_53"),
    ("x_48", "x_54"),
    ("x_59", "x_55"),
    ("x_58", "x_56")
]

X_INNER_BASED_ANCHOR_PAIRS = [
    ("x_61", "x_63"),
    ("x_60", "x_64"),
    ("x_67", "x_65")
]

Y_OUTER_BASED_ANCHOR_PAIRS = [
    ("y_49", "y_59"),
    ("y_50", "y_58"),
    ("y_51", "y_57"),
    ("y_52", "y_56"),
    ("y_53", "y_55")
]

Y_INNER_BASED_ANCHOR_PAIRS = [
    ("y_61", "y_67"),
    ("y_62", "y_66"),
    ("y_63", "y_65")
]

"""
Curvature Coordinate Lists
ORDER: OUTER -> INNER
"""

UPPER_OUTER_RIGHT_COORDS = [
    ("x_48", "y_48"),
    ("x_49", "y_49"),
    ("x_50", "y_50"),
    ("x_51", "y_51")
]

UPPER_OUTER_LEFT_COORDS = [
    ("x_54", "y_54"),
    ("x_53", "y_53"),
    ("x_52", "y_52"),
    ("x_51", "y_51")
]

LOWER_OUTER_RIGHT_COORDS = [
    ("x_48", "y_48"),
    ("x_59", "y_59"),
    ("x_58", "y_58"),
    ("x_57", "y_57")
]

LOWER_OUTER_LEFT_COORDS = [
    ("x_54", "y_54"),
    ("x_55", "y_55"),
    ("x_56", "y_56"),
    ("x_57", "y_57")
]

UPPER_INNER_RIGHT_COORDS = [
    ("x_60", "y_60"),
    ("x_61", "y_61"),
    ("x_62", "y_62")
]

UPPER_INNER_LEFT_COORDS = [
    ("x_64", "y_64"),
    ("x_63", "y_63"),
    ("x_62", "y_62")
]

LOWER_INNER_RIGHT_COORDS = [
    ("x_60", "y_60"),
    ("x_67", "y_67"),
    ("x_66", "y_66")
]

LOWER_INNER_LEFT_COORDS = [
    ("x_64", "y_64"),
    ("x_65", "y_65"),
    ("x_66", "y_66")
]

"""
ALL MOUTH LANDMARKS PAIRS

ORDER: STARTING FROM LEFT IMAGE COMMISSURE (TRUE POSITION: RIGHT) - CLOCKWISE AND THEN REPEATS FOR INNER POINTS
"""

LANDMARK_PAIRS = [
    ("x_48", "y_48"),
    ("x_49", "y_49"),
    ("x_50", "y_50"),
    ("x_51", "y_51"),
    ("x_52", "y_52"),
    ("x_53", "y_53"),
    ("x_54", "y_54"),
    ("x_55", "y_55"),
    ("x_56", "y_56"),
    ("x_57", "y_57"),
    ("x_58", "y_58"),
    ("x_59", "y_59"),
    ("x_60", "y_60"),
    ("x_61", "y_61"),
    ("x_62", "y_62"),
    ("x_63", "y_63"),
    ("x_64", "y_64"),
    ("x_65", "y_65"),
    ("x_66", "y_66"),
    ("x_67", "y_67")
]

"""
ANCHOR PAIRS
"""

ANCHOR_PAIRS = [

]