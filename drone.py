import simpy
import random
import math
from locations import *
from package import Package


DRONES_PER_HUB = 4 # number of drones per hub
DRONE_SPEED = 200 # average riding speed meters/minute 
DRONE_LOAD_TIME = 1  # minutes to load/unload
PACKAGE_RATE = 1.0 / 60 # expected packages per minute


# returns the time it takes a drone to travel
def fly_time(origin, dest):

    dx = LOCATIONS[origin][0] - LOCATIONS[dest][0]
    dy = LOCATIONS[origin][1] - LOCATIONS[dest][1]

    meters = math.hypot(dx, dy) * 111000 # convert from global coordinates
    return meters / DRONE_SPEED # convert to minutes


# This class handles the behaviour of a drone
class Drone:

    def __init__(self, env, hub):
        self.env = env
        self.from_hub = hub
        self.package = None
        self.action = env.process(self.run())
        print(f'Drone created at {self.from_hub.location}')


    def run(self):
        while True:
            # Take package
            self.package = yield self.from_hub.take_pending_package()
            # print(f'[{self.env.now:.1f} min] Drone taking ({self.package.number})')
            yield self.env.timeout(DRONE_LOAD_TIME)

            # Fly package
            # print(f'[{self.env.now:.1f} min] Drone delivering ({self.package.number})')
            deliver_time = fly_time(self.package.origin, self.package.destination)
            yield self.env.timeout(deliver_time)

            # Put package
            # print(f'[{self.env.now:.1f} min] Drone putting ({self.package.number})')
            to_hub = Server.get_hub(self.package.destination)
            to_hub.add_complete_package(self.package)
            yield self.env.timeout(DRONE_LOAD_TIME)

            # Fly back
            # print(f'[{self.env.now:.1f} min] Drone returning')
            return_time = fly_time(self.package.origin, self.package.destination)
            yield self.env.timeout(return_time)



# This class handles the behaviour of a hub
class Hub:

    def __init__(self, env, location):
        self.env = env
        self.location = location
        self.pending_packages = simpy.Store(env)
        self.complete_packages = simpy.Store(env)
        self.drones = []
        for i in range(DRONES_PER_HUB):
            self.drones.append(Drone(env, self))
        print(f'Hub created at {self.location}')

    # add package to hub pending queue
    def add_pending_package(self, package):
        self.pending_packages.put(package)
        print(f'[{self.env.now:.1f} min] Package ({package.number}) added at {self.location}')

    # add package to hub complete queue
    def add_complete_package(self, package):
        self.complete_packages.put(package)
        delivery_delay = self.env.now - package.created_time
        print(f'[{self.env.now:.1f} min] Package ({package.number}) added at {self.location}, delay: {delivery_delay:.1f}')

    # take package from hub pending queue
    def take_pending_package(self):
        return self.pending_packages.get()

    # take package from hub complete queue
    def take_complete_package(self):
        return self.complete_packages.get()



# This class handles the behaviour of a store
class Store:

    # Start the run process everytime an instance is created.
    def __init__(self, env, location, destination):
        self.env = env
        self.location = location
        self.destination = destination
        env.process(self.run())

    def run(self):
        while True:
            # wait for a new package randomly
            no_new_package_time = random.expovariate(PACKAGE_RATE)
            yield self.env.timeout(no_new_package_time)

            # Add number origin and detination
            package = Package()
            package.number = Server.get_number()
            package.origin = self.location
            package.destination = self.destination
            package.created_time = self.env.now

            # Print the full request
            print(f'[{self.env.now:.1f} min] New package ({package.number}): {package.origin} → {package.destination}')

            # Store staff delivers to hub
            walking_time = random.gauss(10, 2)
            yield self.env.timeout(walking_time)
            close_hub = Server.get_hub(self.location)
            close_hub.add_pending_package(package)



# This class acts as the central server of the app
class Server: 
    
    hubs = {}
    package_number: int = 0

    # returns a unique package number
    @staticmethod
    def get_number():
        Server.package_number += 1
        return Server.package_number
    
    @staticmethod
    def get_hub(location):
        return Server.hubs[location]
