import simpy
import random
import math
from locations import *
from package import Package


DRONES_PER_HUB = 1 # number of drones per hub
DRONE_SPEED = 200 # average riding speed meters/minute 
LOAD_TIME = 2  # minutes to load/unload


# This class handles the behaviour of a drone
class Drone:

    def __init__(self, env, hub):
        self.env = env
        self.hub = hub
        self.package = None
        self.action = env.process(self.run())


    def run(self):
        while True:
            # Take package
            self.package = yield self.hub.take_package()
            print(f'[{self.env.now:.1f} min] Drone taking package {self.package.number}')
            yield self.env.timeout(2)

            # Fly package
            print(f'[{self.env.now:.1f} min] Drone delivering')
            yield self.env.timeout(10)

            # Put package
            print(f'[{self.env.now:.1f} min] Drone putting package')
            yield self.env.timeout(2)

            # Fly back
            print(f'[{self.env.now:.1f} min] Drone returning')
            yield self.env.timeout(10)



# This class handles the behaviour of a hub
class Hub:

    def __init__(self, env, location):
        self.env = env
        self.location = location

        self.drones = []
        self.packages = simpy.Store(env)
        for i in range(DRONES_PER_HUB):
            self.drones.append(Drone(env, self))
        print(f'Hub created at {self.location}')

    # add package to hub queue
    def add_package(self, package):
        self.packages.put(package)
        print(f'[{self.env.now:.1f} min] Package {package.number} dropped at {package.origin}')

    # take package from hub queue
    def take_package(self):
        # package = yield self.packages.get()
        # print(f'[{self.env.now:.1f} min] Package {package.number} taken from {package.origin}')
        return self.packages.get()



# This class handles the behaviour of a store
class Store:

    # Start the run process everytime an instance is created.
    def __init__(self, env, server, location):
        self.env = env
        self.server = server
        self.location = location
        env.process(self.run())

    def run(self):
        while True:
            # wait for a new package randomly
            no_new_package_time = random.expovariate(1.0/300)
            yield self.env.timeout(no_new_package_time)

            # Add number origin and detination
            package = Package()
            package.number = self.server.get_number()
            package.origin = self.location
            package.destination = random.choice([l for l in LOCATIONS if l != package.origin])

            # Print the full request
            print(f'[{self.env.now:.1f} min] New package {package.number}: {package.origin} → {package.destination}')

            # Store staff delivers to hub
            walking_time = random.gauss(10, 2)
            yield self.env.timeout(walking_time)
            close_hub = self.server.get_close_hub(self.location)
            close_hub.add_package(package)



# This class acts as the central server of the app
class Server: 
    
    hubs = {}
    package_number: int = 0

    # returns a unique package number
    def get_number(self):
        self.package_number += 1
        return self.package_number
    
    def get_close_hub(self, location):
        return self.hubs[location]
