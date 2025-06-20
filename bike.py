import simpy
import random
from locations import *

# Fixed origins mapping to match TRAVEL_TIME in locations.py exactly
ORIGINS = ['Woensel', 'Tongelreplein', 'Frederiklaan ']
DESTINATIONS = {
    'Woensel': ['Barrierke', 'Hondsruglaan ', 'AH', 'Jumbo'],
    'Tongelreplein': ['Hofke'],
    'Frederiklaan ': ['Hugo'],
}

# Function to generate biker assignments based on total number of bikers
def generate_biker_assignments(num_bikers):
    """
    Generate biker assignments maintaining 4:1:1 ratio for Woensel:Tongelreplein:Frederiklaan
    Every 6 bikers: 4 to Woensel, 1 to Tongelreplein, 1 to Frederiklaan
    """
    assignments = {}
    areas = ['Woensel', 'Woensel', 'Woensel', 'Woensel', 'Tongelreplein', 'Frederiklaan ']
    
    for i in range(num_bikers):
        biker_name = f'Biker-{i + 1}'
        # Use modulo to cycle through the pattern every 6 bikers
        area_index = i % 6
        assignments[biker_name] = areas[area_index]
    
    return assignments



# Financial parameters
BIKER_PAY_RATE = 0.25  # biker wage per minute
PARCEL_FEE = 5 # revenue earned per parcel

NUM_BIKERS = 8 # number of cargo-bike riders
CAPACITY_RANGE = (3, 6) # parcels per bike
LOAD_TIME = 1  # minutes to load/unload
WAIT_TIME = 5  # minutes to wait at pickup location for batching parcels
ARRIVAL_RATE = 1.0 / 2 # 1379 / 8 / 60

# Generate assignments based on NUM_BIKERS
BIKER_ASSIGNMENTS = generate_biker_assignments(NUM_BIKERS)


# Lookup travel time (minutes) between locker locations FOR BIKES!
def ride_time(origin, dest):
    if origin == dest:
        return 0
    
    # Direct lookup if exists in TRAVEL_TIME
    if origin in TRAVEL_TIME and dest in TRAVEL_TIME[origin]:
        return TRAVEL_TIME[origin][dest]
    
    # Fallback to symmetric lookup
    if dest in TRAVEL_TIME and origin in TRAVEL_TIME[dest]:
        return TRAVEL_TIME[dest][origin]
    
    # If neither origin nor dest is a base location (Woensel, Tongelreplein, Frederiklaan),
    # assume it's a delivery route between destinations and use 5 minutes
    base_locations = ['Woensel', 'Tongelreplein', 'Frederiklaan ']
    if origin not in base_locations and dest not in base_locations:
        return 5
    
    # If one is a base and the other isn't, but no route is defined, use 5 minutes
    # This handles cases where bikers need to return to base from any destination
    return 5


# Biking
def biker(env, name, dispatcher):
    # Each biker starts at their assigned origin location
    home_base = BIKER_ASSIGNMENTS[name]
    now_loc = home_base
    
    print(f'[{env.now:.1f} min] {name} starting at home base: {home_base}')

    while True:
        wait_start = env.now
        item = yield dispatcher.get_request_for(name)
        origin, dest = item["job"]
        idle_time = env.now - wait_start

        # pay for waiting before pickup
        dispatcher.total_cost += idle_time * BIKER_PAY_RATE

        # Travel to pickup location (should be same as home base for assigned bikers)
        travel_to_origin = ride_time(now_loc, origin)
        dispatcher.total_cost += travel_to_origin * BIKER_PAY_RATE
        if travel_to_origin > 0:
            print(f'[{env.now:.1f} min] {name} traveling to pickup at {origin} from {now_loc}')
            yield env.timeout(travel_to_origin)
        now_loc = origin
        print(f'[{env.now:.1f} min] {name} arrived at {origin} for pickup')

        # Dynamic batching: wait until full or max wait reached
        batch_start = env.now
        jobs_to_do = [(origin, dest)]
        while len(jobs_to_do) < dispatcher.remaining[name]:
            # collect any queued requests at this origin for this biker's area
            available = [req for req in dispatcher.backlog 
                        if req[0] == origin and req[0] == BIKER_ASSIGNMENTS[name]]
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

        # Return to home base after all deliveries
        return_time = ride_time(now_loc, home_base)
        dispatcher.total_cost += return_time * BIKER_PAY_RATE
        if return_time > 0:
            print(f'[{env.now:.1f} min] {name} returning to home base {home_base}')
            yield env.timeout(return_time)
        now_loc = home_base

        # If out of capacity, reload before next trip
        if dispatcher.remaining[name] == 0:
            reload_time = max(0, random.gauss(LOAD_TIME, 0.5))
            print(f'[{env.now:.1f} min] {name} out of capacity, reloading ({reload_time:.1f} min)')
            yield env.timeout(reload_time)
            dispatcher.remaining[name] = dispatcher.capacity[name]

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
        self.idle.append(biker_name)

    def get_request_for(self, biker_name):
        return self.queue.get(lambda item: item["courier"] == biker_name)

    def free_biker(self, biker_name):
        if self.remaining[biker_name] > 0:
            # Only assign jobs that match this biker's assigned area
            biker_area = BIKER_ASSIGNMENTS[biker_name]
            matching_requests = [req for req in self.backlog if req[0] == biker_area]
            
            if matching_requests:
                req = matching_requests[0]
                self.backlog.remove(req)
                self.queue.put({"courier": biker_name, "job": req})
            else:
                self.idle.append(biker_name)

    def dispatch(self, req):
        origin, dest = req
        
        # Find bikers assigned to this origin area
        available_bikers = [name for name in self.idle 
                           if BIKER_ASSIGNMENTS[name] == origin and self.remaining[name] > 0]
        
        if available_bikers:
            rider = available_bikers[0]  # Take first available biker for this area
            self.idle.remove(rider)
            self.queue.put({"courier": rider, "job": req})
        else:
            # no one free in the right area → stash request
            self.backlog.append(req)

# demand - now generates parcels only from areas where we have bikers
def parcel_generator(env, dispatcher):
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE))

        # Only generate parcels from origins where we have assigned bikers
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