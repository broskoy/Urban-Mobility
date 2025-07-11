LOCATIONS = {
    # from
    'WoenselA':         (51.469183432325934, 5.4761373714842625),
    'Woensel1':         (51.469183432325934, 5.4761373714842625),
    'Woensel2':         (51.469183432325934, 5.4761373714842625),
    'Woensel3':         (51.469183432325934, 5.4761373714842625),
    'StrijpS':          (51.44130775717156, 5.4541546123041496),
    'Tongelre':         (51.44154061071015, 5.503195463318248),
    
    # to
    'Acht':             (51.479002191547735, 5.426839331811105),
    'Het Ven':          (51.44070550936473, 5.439773042666849),
    'tHoffke':          (51.44733309796622, 5.517770806528147),
    'Anschot1':         (51.483804602905984, 5.461756417413241),
    'Anschot2':         (51.47944519518102, 5.478198999270128),
    'Anschot3':         (51.489221464666876, 5.474747101878638)
}

# 1 Woensel ->  1 Acht
# 2 StrijpS -> 2 Het Ven
# 3 Tongelre -> 3 tHoffke
# 1 Woensel -> 4.1 Anschot Hondsruglaan
# 1 Woensel -> 4.2 Anschot Jumbo
# 1 Woensel -> 4.3 Anschot Albert Heijn


# 1 Woensel  | 51.469183432325934, 5.4761373714842625
# 2 StrijpS  | 51.44130775717156, 5.4541546123041496
# 3 Tongelre | 51.44154061071015, 5.503195463318248


# 1 Acht | 51.479002191547735, 5.426839331811105
# 2 Het Ven | 51.44070550936473, 5.439773042666849
# 3 tHoffke | 51.44733309796622, 5.517770806528147
# 4.1 Anschot Hondsruglaan | 51.483804602905984, 5.461756417413241
# 4.2 Anschot Jumbo | 51.47944519518102, 5.478198999270128
# 4.3 Anschot Albert Heijn | 51.489221464666876, 5.474747101878638


# Travel times (minutes) between parcel locker locations (symmetric)
TRAVEL_TIME = {
    'Woensel': {
        'Barrierke': 18,
        'Hondsruglaan ': 10,
        'AH': 11,
        'Jumbo': 7,
    },
    'Tongelreplein': {
        'Hofke': 5,
    },
    'Frederiklaan ': {
        'Hugo': 5,
    }
}