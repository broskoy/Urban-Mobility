import simpy
import random
import math
from locations import *

# Financial parameters
BIKER_PAY_RATE = 0.5  # wage per minute
PARCEL_FEE = 10 


NUM_BIKERS = 5 # number of cargo-bike riders
CAPACITY_RANGE = (2, 4) # parcels per bike
BIKE_SPEED = 200 # average riding speed meters/minute 
LOAD_TIME = 2  # minutes to load/unload
ARRIVAL_RATE = 1.0 / 60 # events per hour



# Lookup travel time (minutes) between locker locations FOR BIKES!
def ride_time(origin, dest):
    if origin == dest:
        return 0
    # direct lookup if exists
    if origin in TRAVEL_TIME and dest in TRAVEL_TIME[origin]:
        return TRAVEL_TIME[origin][dest]
    # fallback to symmetric lookup
    if dest in TRAVEL_TIME and origin in TRAVEL_TIME[dest]:
        return TRAVEL_TIME[dest][origin]
    # if no direct route defined, return a large default or zero
    return 0


# Biking
def biker(env, name, dispatcher):
    now_loc = random.choice(list(LOCATIONS))

    while True:
        req = yield dispatcher.get_request()
        origin, dest = req

        # Going to pick up the package
        travel_to_origin = ride_time(now_loc, origin)
        dispatcher.total_cost += travel_to_origin * BIKER_PAY_RATE
        print(f'[{env.now:.1f} min] {name} assigned to pickup at {origin}, heading from {now_loc}')
        yield env.timeout(travel_to_origin)
        
        # Loading the package
        print(f'[{env.now:.1f} min] {name} arrived at {origin} for pickup')
        load_duration = random.gauss(LOAD_TIME, 0.5)
        dispatcher.total_cost += load_duration * BIKER_PAY_RATE
        yield env.timeout(load_duration)

        # Go to destination
        travel_to_dest = ride_time(origin, dest)
        dispatcher.total_cost += travel_to_dest * BIKER_PAY_RATE
        print(f'[{env.now:.1f} min] {name} riding to {dest}')
        yield env.timeout(travel_to_dest)
        
        # Deliver the package
        print(f'[{env.now:.1f} min] {name} arrived at {dest} for drop-off')
        unload_duration = random.gauss(LOAD_TIME, 0.5)
        dispatcher.total_cost += unload_duration * BIKER_PAY_RATE
        yield env.timeout(unload_duration)

        # Record revenue and print summary after each delivery
        dispatcher.total_revenue += PARCEL_FEE
        print(f'[{env.now:.1f} min] {name} delivered parcel. '
              f'Total revenue: {dispatcher.total_revenue:.2f}, '
              f'Total cost: {dispatcher.total_cost:.2f}, '
              f'Net profit: {dispatcher.total_revenue - dispatcher.total_cost:.2f}')

        # Update position
        now_loc = dest
        dispatcher.free_biker(name)


# Requests
class Dispatcher:
    def __init__(self, env):
        self.env = env
        self.idle = []
        self.queue = simpy.Store(env)
        self.total_cost = 0.0
        self.total_revenue = 0.0

    def register(self, biker_name):
        self.idle.append(biker_name)

    def get_request(self):
        return self.queue.get()

    def free_biker(self, biker_name):
        self.idle.append(biker_name)

    def dispatch(self, req):
        if self.idle:
            b = self.idle.pop(0) # nearest policy to implement
            self.queue.put(req)
        else:
            self.queue.put(req)

# demand
def parcel_generator(env, dispatcher):
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE))

        # Add origin and detination 
        origin = random.choice(list(LOCATIONS))
        dest = random.choice([l for l in LOCATIONS if l != origin])
        print(f'[{env.now:.1f} min] New parcel request: {origin} → {dest}')
        dispatcher.dispatch((origin, dest))


def run_simulation(sim_duration_minutes):
    env = simpy.Environment()
    dispatcher = Dispatcher(env)
    # register and start bikers
    for i in range(NUM_BIKERS):
        name = f'Biker-{i+1}'
        dispatcher.register(name)
        env.process(biker(env, name, dispatcher))
    # start demand
    env.process(parcel_generator(env, dispatcher))
    # run until end of simulated day
    env.run(until=sim_duration_minutes)
    # end-of-day summary
    print('--- End of Day Summary ---')
    print(f'Total revenue: {dispatcher.total_revenue:.2f}')
    print(f'Total cost:    {dispatcher.total_cost:.2f}')
    print(f'Net profit:    {dispatcher.total_revenue - dispatcher.total_cost:.2f}')

if __name__ == '__main__':
    # simulate 24 hours (1440 minutes)
    run_simulation(24 * 60)
