LOCATIONS = {
    # from
    'Woensel':          (51.447, 5.450),
    'StrijpS':          (51.430, 5.450),
    'Tongelre':         (51.460, 5.477),
    
    # to
    'Acht':             (51.4781, 5.4273),
    'Het Ven':          (51.4407, 5.4397),
    'tHoffke':          (51.4473, 5.5177),
    'Anschot1':         (51.4892, 5.4747),
    'Anschot2':         (51.4892, 5.4747),
    'Anschot3':         (51.4892, 5.4747)
}

# 1 Woensel ->  1 Acht
# 2 StrijpS -> 2 Het Ven
# 3 Tongelre -> 3 tHoffke
# 1 Woensel -> 4.1 Anschot Hondsruglaan
# 1 Woensel -> 4.2 Anschot Jumbo
# 1 Woensel -> 4.3 Anschot Albert Heijn

# 1 Woensel  | 
# 2 StrijpS  |
# 3 Tongelre |
# 1 Woensel  |
# 1 Woensel  |
# 1 Woensel  |

# 1 Acht | 51.478120394486126, 5.427358991573096
# 2 Het Ven | 51.44070550936473, 5.439773042666849
# 3 tHoffke | 51.44733309796622, 5.517770806528147
# 4.1 Anschot Hondsruglaan | 
# 4.2 Anschot Jumbo | 
# 4.3 Anschot Albert Heijn | 51.489221464666876, 5.474747101878638


# Travel times (minutes) between parcel locker locations (symmetric)
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