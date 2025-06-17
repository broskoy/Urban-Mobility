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