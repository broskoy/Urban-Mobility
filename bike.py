import simpy
import random
import math


NUM_BIKERS = 5 # number of cargo-bike riders
CAPACITY_RANGE = (2, 4) # parcels per bike
BIKE_SPEED = 200 # average riding speed meters/minute 
ARRIVAL_RATE = 1.0 # λ per hour (poisson) — editable (DEMAND)
SERVICE_TIME = 2  # minutes to load/unload
LOCATIONS = {
    'Acht':             (5.450, 51.447),
    'Het Ven':          (5.483, 51.442),
    'Tongelre':         (5.477, 51.460),
    'Strijps Centrum':  (5.450, 51.430),
    'Centrum':          (5.480, 51.440)
}


# Compute ride time between two coords (REPLACE BY GOOGLE MAPS)
def ride_time(origin, dest):
    dx = LOCATIONS[origin][0] - LOCATIONS[dest][0]
    dy = LOCATIONS[origin][1] - LOCATIONS[dest][1]
    meters = math.hypot(dx, dy) * 111000
    return meters / BIKE_SPEED # convert to minutes


# Biking
def biker(env, name, dispatcher):
    now_loc = random.choice(list(LOCATIONS))

    while True:
        req = yield dispatcher.get_request()
        origin, dest = req

        # Going to pick up the package
        print(f'[{env.now:.1f} min] {name} assigned to pickup at {origin}, heading from {now_loc}')
        yield env.timeout(ride_time(now_loc, origin))
        
        # Loading the package
        print(f'[{env.now:.1f} min] {name} arrived at {origin} for pickup')
        yield env.timeout(random.gauss(SERVICE_TIME, 0.5))  # load

        # Go to destination
        print(f'[{env.now:.1f} min] {name} riding to {dest}')
        yield env.timeout(ride_time(origin, dest))
        
        # Deliver the package
        print(f'[{env.now:.1f} min] {name} arrived at {dest} for drop-off')
        yield env.timeout(random.gauss(SERVICE_TIME, 0.5))  # unload

        # Update position
        now_loc = dest
        dispatcher.free_biker(name)


# Requests
class Dispatcher:
    def __init__(self, env):
        self.env = env
        self.idle = []
        self.queue = simpy.Store(env)

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
        yield env.timeout(random.expovariate(ARRIVAL_RATE/60))

        # Add origin and detination 
        origin = random.choice(list(LOCATIONS))
        dest = random.choice([l for l in LOCATIONS if l != origin])
        print(f'[{env.now:.1f} min] New parcel request: {origin} → {dest}')
        dispatcher.dispatch((origin, dest))


