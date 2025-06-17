import simpy
from locations import LOCATIONS
import drone  # access drone module directly
from bike import setup as setup_bikes

# Simulated period (8 hours)
SIM_TIME = 8 * 60  # minutes

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
    """Launch bikes and drones in one shared SimPy environment."""
    env = simpy.Environment()

    # Initialise both transport modes
    bike_dispatcher = setup_bikes(env)
    drone_server = setup_drones(env)

    env.run(until=SIM_TIME)

    # Optional: end‑of‑day summaries
    print("\n--- Bike finance ---")
    print(f"Revenue: {bike_dispatcher.total_revenue:.2f}")
    print(f"Cost:    {bike_dispatcher.total_cost:.2f}")
    print(f"Profit:  {bike_dispatcher.total_revenue - bike_dispatcher.total_cost:.2f}")

    if hasattr(drone_server, "stats"):
        print("\n--- Drone stats ---")
        # drone_server.stats.pretty_print()


# 1 Woensel ->  1 Acht
# 2 StrijpS -> 2 Het Ven
# 3 Tongelre -> 3 tHoffke
# 1 Woensel -> 4.1 Anschot Hondsruglaan
# 1 Woensel -> 4.2 Anschot Jumbo
# 1 Woensel -> 4.3 Anschot Albert Heijn


# Start of drone code

env = simpy.Environment()
server = drone.Server()

for location in LOCATIONS.keys():
    server.hubs[location] = drone.Hub(env, location)

drone.Store(env, 'Woensel', 'Acht')
drone.Store(env, 'StrijpS', 'Het Ven')
drone.Store(env, 'Tongelre', 'tHoffke')
drone.Store(env, 'Woensel', 'Anschot3')

env.run(until=SIM_TIME)

# Staret of bike code

# env = simpy.Environment()
# disp = Dispatcher(env)
# # create bikers
# for i in range(NUM_BIKERS):
#     b = env.process(biker(env, f'Biker_{i}', disp))
#     disp.register(f'Biker_{i}')
# env.process(parcel_generator(env, disp))
# env.run(until=SIM_TIME)


# Optional: end‑of‑day summaries
# print("\n--- Bike finance ---")
# print(f"Revenue: {bike_dispatcher.total_revenue:.2f}")
# print(f"Cost:    {bike_dispatcher.total_cost:.2f}")
# print(f"Profit:  {bike_dispatcher.total_revenue - bike_dispatcher.total_cost:.2f}")

# if hasattr(drone_server, "stats"):
#     print("\n--- Drone stats ---")
#     drone_server.stats.pretty_print()


# if __name__ == "__main__":
#     run_multimodal_sim()