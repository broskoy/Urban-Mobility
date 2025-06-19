import simpy
from locations import LOCATIONS
import drone  # access drone module directly
from bike import setup as setup_bikes

# Simulated period (8 hours)
SIM_TIME = 8 * 60  # minutes


def print_fly_times():
    print('WoenselA', 'Acht', drone.fly_time('WoenselA', 'Acht'))
    print('StrijpS', 'Het Ven', drone.fly_time('StrijpS', 'Het Ven'))
    print('Tongelre', 'tHoffke', drone.fly_time('Tongelre', 'tHoffke'))
    print('Woensel1', 'Anschot1', drone.fly_time('Woensel1', 'Anschot1'))
    print('Woensel2', 'Anschot2', drone.fly_time('Woensel2', 'Anschot2'))
    print('Woensel3', 'Anschot3', drone.fly_time('Woensel3', 'Anschot3'))


def add_stores(env):
    drone.Store(env, 'WoenselA', 'Acht')
    drone.Store(env, 'StrijpS', 'Het Ven')
    drone.Store(env, 'Tongelre', 'tHoffke')
    drone.Store(env, 'Woensel1', 'Anschot1')
    drone.Store(env, 'Woensel2', 'Anschot2')
    drone.Store(env, 'Woensel3', 'Anschot3')


def setup_drones(env):
    """
    Initialise drone hubs and stores in the shared SimPy environment.
    Replaces the missing setup() helper inside drone.py.
    """
    # reset static server state for repeatable runs
    drone.Server.hubs.clear()
    drone.Server.package_number = 0

    # create one Hub and one Store per location
    for loc in LOCATIONS.keys():
        drone.Server.hubs[loc] = drone.Hub(env, loc)

    return drone.Server


def run_multimodal_sim():
    env = simpy.Environment()

    # Initialise both transport modes
    bike_dispatcher = setup_bikes(env)
    # drone_server = setup_drones(env)

    env.run(until=SIM_TIME)

    # Optional: end‑of‑day summaries
    print("\n--- Bike finance ---")
    print(f"Revenue: {bike_dispatcher.total_revenue:.2f}")
    print(f"Cost:    {bike_dispatcher.total_cost:.2f}")
    print(f"Profit:  {bike_dispatcher.total_revenue - bike_dispatcher.total_cost:.2f}")


    
    # if hasattr(drone_server, "stats"):
    #     print("\n--- Drone stats ---")
    #     # drone_server.stats.pretty_print()

# Start of drone code

print_fly_times()

env = simpy.Environment()
server = drone.Server()

for location in LOCATIONS.keys():
    server.hubs[location] = drone.Hub(env, location)

add_stores(env)

env.run(until=SIM_TIME)

for location in LOCATIONS:
    print(location)
    print(f'deliveries:{drone.location_total_deliveries[location]}')
    if (drone.location_total_deliveries[location] == 0):
        print(0)
    else:
        print(f'average delay:{drone.location_total_delay[location] / drone.location_total_deliveries[location]}\n')


if __name__ == "__main__":
    run_multimodal_sim()