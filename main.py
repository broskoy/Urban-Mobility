import simpy
from bike import *
from drone import *

SIM_TIME = 8 * 60 # simulated period (8 hours)




# Start of drone code

def create_stores():
    for location in LOCATIONS.keys():
        Store(env, server, location)

def create_hubs():
    for location in LOCATIONS.keys():
        Hub(env, location)

env = simpy.Environment()
server = Server()
create_hubs()
create_stores()
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