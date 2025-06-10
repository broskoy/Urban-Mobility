import simpy
from bike import *
from drone import *

SIM_TIME = 8 * 60 # simulated period (8 hours)




# Start of drone code

env = simpy.Environment()
server = Server()

server.hubs['Acht'] = Hub(env, 'Acht')
Store(env, server, 'Acht')

# for location in LOCATIONS.keys():
#     server.hubs[location] = Hub(env, location)
#     Store(env, server, location)

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