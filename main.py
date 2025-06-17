import simpy
from bike import *
from drone import *

SIM_TIME = 8 * 60 # simulated period (8 hours)


# 1 Woensel ->  1 Acht
# 2 StrijpS -> 2 Het Ven
# 3 Tongelre -> 3 tHoffke
# 1 Woensel -> 4.1 Anschot Hondsruglaan
# 1 Woensel -> 4.2 Anschot Jumbo
# 1 Woensel -> 4.3 Anschot Albert Heijn


# Start of drone code

env = simpy.Environment()
server = Server()

for location in LOCATIONS.keys():
    server.hubs[location] = Hub(env, location)

Store(env, 'Woensel', 'Acht')
Store(env, 'StrijpS', 'Het Ven')
Store(env, 'Tongelre', 'tHoffke')
Store(env, 'Woensel', 'Anschot3')

env.run(until=SIM_TIME)

# Staret of bike code

# env = simpy.Environment()
# disp = Dispatcher(env)
# # create bikers
# for i in range(NUM_BIKERS):
#     b = env.process(biker(env, f'Biker_{i}', disp))
#     disp.register(f'Biker_{i}')
# env.process(parcel_generator(env, disp))
# env.run(until=SIM_TIME)