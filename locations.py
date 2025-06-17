LOCATIONS = {
    'Acht':             (5.450, 51.447),
    'Het Ven':          (5.483, 51.442),
    'Tongelre':         (5.477, 51.460),
    'Strijps':          (5.450, 51.430),
    'Centrum':          (5.480, 51.440)
}


# Travel times (minutes) between parcel locker locations (symmetric)
# Fill it out
TRAVEL_TIME = {
    'Acht': {
        'Hugo': 20,
        'Tongelre': 30,
        'AH': 12,
        'AJ': 15,
        'AAH': 14,
    },
    'Hugo': {
        'Tongelre': 25,
        'AH': 23,
        'AJ': 24,
        'AAH': 18,
    },
    'Tongelre': {
        'AH': 26,
        'AJ': 21,
        'AAH': 26,
    },
    'AH': {
        'AJ': 6,
        'AAH': 4,
    },
    'AJ': {
        'AAH': 5,
    },
}