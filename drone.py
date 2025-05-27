import simpy
import random
import math
from utility import *


DRONES_PER_HUB = 1 # number of drones per hub
DRONE_SPEED = 200 # average riding speed meters/minute 
LOAD_TIME = 2  # minutes to load/unload


# This class handles the behaviour of a drone
class Drone:

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def charge(self):
        yield self.env.timeout(3)

    def run(self):
        while True:
            print(f'[{self.env.now:.1f} min] doin stuff')
            yield self.env.timeout(10)
            print(f'[{self.env.now:.1f} min] not doin stuff')
            yield self.env.timeout(20)

            # req = yield dispatcher.get_request()
            # origin, dest = req

            # # Loading the package
            # print(f'[{env.now:.1f} min] {name} arrived at {origin} for pickup')
            # yield env.timeout(random.gauss(LOAD_TIME, 0.5))

            # # Going to destination
            # print(f'[{env.now:.1f} min] {name} riding to {dest}')
            # yield env.timeout(ride_time(origin, dest))
            
            # # Delivering the package
            # print(f'[{env.now:.1f} min] {name} arrived at {dest} for drop-off')
            # yield env.timeout(random.gauss(LOAD_TIME, 0.5))

            # # Update position
            # now_loc = dest
            # dispatcher.free_biker(name)



# This class handles the behaviour of a hub
class Hub:

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(20)
            print('Start parking and charging at %d' % self.env.now)
            yield self.env.timeout(20)
            print('Start driving at %d' % self.env.now)



# This class handles the behaviour of a store
class Store:

    package_number: int = 0

    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(random.expovariate(1/60))

            # Update package number
            Store.package_number += 1

            # Add origin and detination 
            origin = random.choice(list(LOCATIONS))
            destination = random.choice([l for l in LOCATIONS if l != origin])

            # Print the full request
            print(f'[{self.env.now:.1f} min] New package request: id {Store.package_number}, {origin} → {destination}')

            # Store staff delivers to hub
            yield self.env.timeout(10)
            print(f'[{self.env.now:.1f} min] Package {Store.package_number} dropped at {origin}')