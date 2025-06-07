LOCATIONS = {
    'Acht':             (5.450, 51.447),
    'Het Ven':          (5.483, 51.442),
    'Tongelre':         (5.477, 51.460),
    'Strijps Centrum':  (5.450, 51.430),
    'Centrum':          (5.480, 51.440)
}

# Travel times (minutes) between parcel locker locations (symmetric)
# Fill it out
TRAVEL_TIME = {
    'Winkelcentrum Woensel': {
        't Barrierke': 18,
        'Hondsruglaan 116': 10,
        'Ouverture 214': 11,
        'Belgiëplein 21': 7
    },
    't Barrierke': {
        'Winkelcentrum Woensel': 18,
        'Frederiklaan nr 108-110': 18
    },
    'Hondsruglaan 116': {
        'Winkelcentrum Woensel': 10
    },
    'Ouverture 214': {
        'Winkelcentrum Woensel': 11
    },
    'Belgiëplein 21': {
        'Winkelcentrum Woensel': 7
    },
    'Klein Tongelreplein': {
        "Cafetaria 't Hofke": 5
    },
    "Cafetaria 't Hofke": {
        'Klein Tongelreplein': 5
    },
    'Frederiklaan nr 108-110': {
        'Hugo de Grootplein': 5,
        't Barrierke': 18
    },
    'Hugo de Grootplein': {
        'Frederiklaan nr 108-110': 5
    }
}