import simpy
from bike import *
from drone import *

SIM_TIME = 8 * 60 # simulated period (8 hours)

# Start of code

env = simpy.Environment()
# Drone(env)
# Hub(env)
Store(env)
env.run(until=SIM_TIME)



# env = simpy.Environment()
# disp = Dispatcher(env)
# # create bikers
# for i in range(NUM_BIKERS):
#     b = env.process(biker(env, f'Biker_{i}', disp))
#     disp.register(f'Biker_{i}')
# env.process(parcel_generator(env, disp))
# env.run(until=SIM_TIME)