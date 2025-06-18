import simpy
import random
from locations import *

# Restricted origins and their valid destinations
ORIGINS = ['Woensel', 'Strijp', 'Tongelre']
DESTINATIONS = {
    'Woensel': ['HuAchtgo', 'Hondsruglaan', 'Jumbo', 'AH'],
    'Strijp': ['HetVen'],
    'Tongelre': ['tHoffke'],
}

# Financial parameters
BIKER_PAY_RATE = 0.25  # wage per minute
PARCEL_FEE = 5


NUM_BIKERS = 1 # number of cargo-bike riders
CAPACITY_RANGE = (3, 6) # parcels per bike
LOAD_TIME = 1  # minutes to load/unload
WAIT_TIME = 5  # minutes to wait at pickup location for batching parcels
ARRIVAL_RATE = 10000 * 6 / 60 * 0.5 # (4 * 6) / 60 # 6 - is the amount of areas TO ADJUST?



# Lookup travel time (minutes) between locker locations FOR BIKES! TODO
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
    return 30


# Biking
def biker(env, name, dispatcher):

    now_loc = random.choice(list(LOCATIONS))

    while True:
        wait_start = env.now
        item = yield dispatcher.get_request_for(name)
        origin, dest = item["job"]
        idle_time = env.now - wait_start

        # pay for waiting before pickup
        dispatcher.total_cost += idle_time * BIKER_PAY_RATE

        # Travel to pickup location
        travel_to_origin = ride_time(now_loc, origin)
        dispatcher.total_cost += travel_to_origin * BIKER_PAY_RATE
        print(f'[{env.now:.1f} min] {name} assigned to pickup at {origin}, heading from {now_loc}')
        yield env.timeout(travel_to_origin)
        now_loc = origin
        print(f'[{env.now:.1f} min] {name} arrived at {origin} for pickup')

        # Dynamic batching: wait until full or max wait reached
        batch_start = env.now
        jobs_to_do = [(origin, dest)]
        while len(jobs_to_do) < dispatcher.remaining[name]:
            # collect any queued requests at this origin
            available = [req for req in dispatcher.backlog if req[0] == origin]
            if available:
                req = available.pop(0)
                dispatcher.backlog.remove(req)
                jobs_to_do.append(req)
                continue
            # if max wait exceeded, depart
            if env.now - batch_start >= WAIT_TIME:
                break
            yield env.timeout(1)
        # pay for batching wait
        waited = env.now - batch_start
        dispatcher.total_cost += waited * BIKER_PAY_RATE

        # Load all parcels
        for _, _ in jobs_to_do:
            load_duration = max(0, random.gauss(LOAD_TIME, 0.5))
            dispatcher.total_cost += load_duration * BIKER_PAY_RATE
            yield env.timeout(load_duration)
            dispatcher.remaining[name] -= 1

        # Deliver each parcel sequentially
        for _, dropoff in jobs_to_do:
            travel_to_dest = ride_time(now_loc, dropoff)
            dispatcher.total_cost += travel_to_dest * BIKER_PAY_RATE
            print(f'[{env.now:.1f} min] {name} riding to {dropoff}')
            yield env.timeout(travel_to_dest)
            now_loc = dropoff
            print(f'[{env.now:.1f} min] {name} arrived at {dropoff} for drop-off')
            unload_duration = max(0, random.gauss(LOAD_TIME, 0.5))
            dispatcher.total_cost += unload_duration * BIKER_PAY_RATE
            yield env.timeout(unload_duration)
            dispatcher.total_revenue += PARCEL_FEE
            print(f'[{env.now:.1f} min] {name} delivered parcel. '
                  f'Total revenue: {dispatcher.total_revenue:.2f}, '
                  f'Total cost: {dispatcher.total_cost:.2f}, '
                  f'Net profit: {dispatcher.total_revenue - dispatcher.total_cost:.2f}')

        # If out of capacity, reload before next trip
        if dispatcher.remaining[name] == 0:
            reload_time = max(0, random.gauss(LOAD_TIME, 0.5))
            print(f'[{env.now:.1f} min] {name} out of capacity, reloading ({reload_time:.1f} min)')
            yield env.timeout(reload_time)
            dispatcher.remaining[name] = dispatcher.capacity[name]

        # Return to pickup origin after deliveries
        return_time = ride_time(now_loc, origin)
        dispatcher.total_cost += return_time * BIKER_PAY_RATE
        print(f'[{env.now:.1f} min] {name} returning to {origin}')
        yield env.timeout(return_time)
        now_loc = origin

        dispatcher.free_biker(name)
        


# Requests
class Dispatcher:
    def __init__(self, env):
        self.env = env
        self.idle = []
        self.queue = simpy.FilterStore(env)  # allows per‑courier filtering
        self.backlog = []                   # requests waiting for any courier
        self.total_cost = 0.0
        self.total_revenue = 0.0
        self.capacity = {}
        self.remaining = {}

    def register(self, biker_name):
        cap = random.randint(*CAPACITY_RANGE)
        self.capacity[biker_name] = cap
        self.remaining[biker_name] = cap
        # keep location update later; we only track idle status here
        self.idle.append(biker_name)

    def get_request_for(self, biker_name):
        return self.queue.get(lambda item: item["courier"] == biker_name)

    def free_biker(self, biker_name):
        if self.remaining[biker_name] > 0:
            if self.backlog:
                req = self.backlog.pop(0)
                self.queue.put({"courier": biker_name, "job": req})
            else:
                self.idle.append(biker_name)

    def dispatch(self, req):
        # purge riders that ran out of space
        self.idle = [r for r in self.idle if self.remaining[r] > 0]

        if self.idle:
            rider = self.idle.pop(0)         # FIFO; TODO: nearest‑rider heuristic
            self.queue.put({"courier": rider, "job": req})
        else:
            # no one free → stash request
            self.backlog.append(req)

# demand
def parcel_generator(env, dispatcher):
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE))

        # Add origin and detination 
        origin = random.choice(ORIGINS)
        dest = random.choice(DESTINATIONS[origin])
        print(f'[{env.now:.1f} min] New parcel request: {origin} → {dest}')
        dispatcher.dispatch((origin, dest))

def setup(env, num_bikers: int = NUM_BIKERS):

    dispatcher = Dispatcher(env)

    # Register riders and launch their processes
    for i in range(num_bikers):
        name = f'Biker-{i + 1}'
        dispatcher.register(name)
        env.process(biker(env, name, dispatcher))

    # Launch demand process
    env.process(parcel_generator(env, dispatcher))
    return dispatcher
