import simpy
import random
import math
from utility import *
from package import Package


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

    packages = []

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def add_package(self, package):
        print(package.id)

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
        # self.action = 
        env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(random.expovariate(1/60))

            # TODO: should call server for a unique number
            # Add number origin and detination
            package = Package()
            Store.package_number += 1 
            package.number = self.package_number
            package.origin = random.choice(list(LOCATIONS))
            package.destination = random.choice([l for l in LOCATIONS if l != package.origin])

            # Print the full request
            print(f'[{self.env.now:.1f} min] New package request: number {Store.package_number}, {package.origin} → {package.destination}')

            # Store staff delivers to hub
            yield self.env.timeout(10)
            print(f'[{self.env.now:.1f} min] Package {Store.package_number} dropped at {package.origin}')


# This class acts as the central server of the app
class Server: 
    
    package_number: int = 0

    # returns a unique package number
    def get_number(self):
        self.package_number += 1
        return self.package_number