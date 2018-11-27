

"""
    SOUTH CALIFORNIA EDISON
    TOU 8 RATE
    OPTION B
    WITHOUT CPP
    (~ DEC 2018 )
    
    ** HOLIDAY
        1/1 : New Year's Day
        3rd Monday in Feb : Washington's Birthday
        last Monday in May : Memorial Day
        7/4 : Independence Day
        1st Monday in Sep : Labor Day
        11/11 : Veterans Day
        4th Thurs in Nov : Thanksgiving Day
        12/25 : Christmas
"""

TOU8_OPTION_B = {
    # TOU
    'SEASON': ['WINTER', 'WINTER', 'WINTER', 'WINTER',\
               'WINTER', 'SUMMER', 'SUMMER', 'SUMMER',\
               'SUMMER', 'WINTER', 'WINTER', 'WINTER'],
    'HOLIDAY': ["New Year's Day", "Washington's Birthday", "Memorial Day", "Independence Day",\
                     "Labor Day", "Veterans Day", "Thanksgiving", "Christmas Day"],
    # Demand Charge
    'FR': 19.02,
    'DC_ON_S': 21.42,
    'DC_ON_W': 0,
    'DC_MIDS': 4.12,
    'DC_MIDW': 0,
    # Non-Bypassable Charge Rate
    'NBC': 0.025,
    # Default Charge
    'CC': 658.17,
    'DLV': 0.02078,
    # Energy Charge
    'ON_S': 0.08131,
    'MIDS': 0.05477,
    'OFFS': 0.03663,
    #
    'ON_W': 0,
    'MIDW': 0.05294,
    'OFFW': 0.04214
}

TOU8_OPTION_R = {
    # TOU
    'SEASON': ['WINTER', 'WINTER', 'WINTER', 'WINTER',\
               'WINTER', 'SUMMER', 'SUMMER', 'SUMMER',\
               'SUMMER', 'WINTER', 'WINTER', 'WINTER'],
    'HOLIDAY': ["New Year's Day", "Washington's Birthday", "Memorial Day", "Independence Day",\
                     "Labor Day", "Veterans Day", "Thanksgiving", "Christmas Day"],
    # Demand Charge
    'FR': 16.64,
    'DC_ON_S': 0,
    'DC_ON_W': 0,
    'DC_MIDS': 0,
    'DC_MIDW': 0,
    # Non-Bypassable Charge Rate
    'NBC': 0.025,
    # Default Charge
    'CC': 658.17,
    'DLV': 0.02679,
    # Energy Charge
    'ON_S': 0.31354,
    'MIDS': 0.08843,
    'OFFS': 0.03663,
    #
    'ON_W': 0,
    'MIDW': 0.05294,
    'OFFW': 0.04214
}