import random
print("Ayush R Kallingal\n1WN24CS057")
# ============================================================
# GENETIC ALGORITHM - DRIVING ECONOMY ANALYZER
# ============================================================

POP_SIZE = 60
MAX_GENERATIONS = 100

CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1


# ============================================================
# USER INPUT
# ============================================================

print("=" * 65)
print("       GENETIC ALGORITHM - DRIVING ECONOMY ANALYZER")
print("=" * 65)

distance = float(input("Distance to travel (km): "))
road_condition = float(input("Road condition (1-10): "))
traffic_condition = float(input("Traffic condition (1-10): "))
vehicle_load = float(input("Additional load (kg): "))
base_mileage = float(input("Vehicle base mileage (km/L): "))
weather = float(input("Weather severity (1-10): "))
terrain = float(input("Terrain difficulty (1-10): "))

print("\n--- YOUR DRIVING PARAMETERS ---")

user_speed = float(input("Your speed (km/h): "))
user_acceleration = float(
    input("Your acceleration (m/s²): ")
)

user_ac = float(input("Your AC usage (0-100%): "))
user_braking = float(
    input("Your braking (m/s²): ")
)
user_idle = float(
    input("Your idle time (minutes): ")
)


# ============================================================
# FUEL CONSUMPTION MODEL
# ============================================================

def calculate_fuel(speed, acceleration, braking, ac, idle):

    # Base fuel consumption
    base_consumption = 1 / base_mileage

    # Speed penalty
    speed_penalty = (
        0.00015 * (speed - 50) ** 2
    )

    # Acceleration penalty
    acceleration_penalty = (
        0.025 * acceleration ** 2
    )

    # Braking penalty
    braking_penalty = (
        0.015 * braking ** 2
    )

    # Traffic
    traffic_penalty = (
        0.0025 * traffic_condition
    )

    # Road
    road_penalty = (
        0.002 * (10 - road_condition)
    )

    # Load
    load_penalty = (
        0.00001 * vehicle_load
    )

    # Weather
    weather_penalty = (
        0.0015 * weather
    )

    # Terrain
    terrain_penalty = (
        0.003 * terrain
    )

    # AC
    ac_penalty = (
        0.0004 * ac
    )

    # Idle
    idle_penalty = (
        0.003 * idle
    )

    fuel_per_km = (
        base_consumption
        + speed_penalty
        + acceleration_penalty
        + braking_penalty
        + traffic_penalty
        + road_penalty
        + load_penalty
        + weather_penalty
        + terrain_penalty
        + ac_penalty
        + idle_penalty
    )

    return fuel_per_km * distance


# ============================================================
# GENETIC ALGORITHM
# ============================================================

# Individual:
# [speed, acceleration, braking, AC, idle_time]


def create_individual():

    return [
        random.uniform(30, 100),   # speed
        random.uniform(0.1, 4.0),  # acceleration
        random.uniform(0.1, 4.0),  # braking
        random.uniform(0, 100),    # AC
        random.uniform(0, 15)       # idle
    ]


def fitness(individual):

    speed = individual[0]
    acceleration = individual[1]
    braking = individual[2]
    ac = individual[3]
    idle = individual[4]

    fuel = calculate_fuel(
        speed,
        acceleration,
        braking,
        ac,
        idle
    )

    # Lower fuel = better fitness
    return 1 / (1 + fuel)


def selection(population):

    tournament = random.sample(
        population,
        3
    )

    return max(
        tournament,
        key=fitness
    )


def crossover(parent1, parent2):

    child1 = parent1.copy()
    child2 = parent2.copy()

    for i in range(len(parent1)):

        if random.random() < 0.5:

            child1[i] = parent2[i]
            child2[i] = parent1[i]

    return child1, child2


def mutation(individual):

    # Speed
    if random.random() < MUTATION_RATE:

        individual[0] += random.uniform(-5, 5)

        individual[0] = max(
            30,
            min(100, individual[0])
        )

    # Acceleration
    if random.random() < MUTATION_RATE:

        individual[1] += random.uniform(
            -0.5, 0.5
        )

        individual[1] = max(
            0.1,
            min(4.0, individual[1])
        )

    # Braking
    if random.random() < MUTATION_RATE:

        individual[2] += random.uniform(
            -0.5, 0.5
        )

        individual[2] = max(
            0.1,
            min(4.0, individual[2])
        )

    # AC
    if random.random() < MUTATION_RATE:

        individual[3] += random.uniform(
            -10, 10
        )

        individual[3] = max(
            0,
            min(100, individual[3])
        )

    # Idle
    if random.random() < MUTATION_RATE:

        individual[4] += random.uniform(
            -2, 2
        )

        individual[4] = max(
            0,
            min(15, individual[4])
        )


# ============================================================
# GENETIC ALGORITHM
# ============================================================

def genetic_algorithm():

    population = [
        create_individual()
        for _ in range(POP_SIZE)
    ]

    best_solution = None

    for generation in range(MAX_GENERATIONS):

        current_best = max(
            population,
            key=fitness
        )

        if (
            best_solution is None
            or fitness(current_best)
            > fitness(best_solution)
        ):
            best_solution = current_best.copy()

        new_population = []

        while len(new_population) < POP_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            if random.random() < CROSSOVER_RATE:

                child1, child2 = crossover(
                    parent1,
                    parent2
                )

            else:

                child1 = parent1.copy()
                child2 = parent2.copy()

            mutation(child1)
            mutation(child2)

            new_population.append(child1)

            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        population = new_population

    return best_solution


# ============================================================
# RUN GA
# ============================================================

print("\nRunning Genetic Algorithm...")

best = genetic_algorithm()


# ============================================================
# OPTIMAL VALUES
# ============================================================

optimal_speed = best[0]
optimal_acceleration = best[1]
optimal_braking = best[2]
optimal_ac = best[3]
optimal_idle = best[4]

optimal_fuel = calculate_fuel(
    optimal_speed,
    optimal_acceleration,
    optimal_braking,
    optimal_ac,
    optimal_idle
)

optimal_mileage = distance / optimal_fuel


# ============================================================
# USER'S VALUES
# ============================================================

user_fuel = calculate_fuel(
    user_speed,
    user_acceleration,
    user_braking,
    user_ac,
    user_idle
)

user_mileage = distance / user_fuel


# ============================================================
# COMPARISON
# ============================================================

speed_difference = abs(
    user_speed - optimal_speed
)

acceleration_difference = abs(
    user_acceleration - optimal_acceleration
)

fuel_difference = (
    user_fuel - optimal_fuel
)

fuel_percentage = (
    fuel_difference / optimal_fuel
) * 100


# ============================================================
# FINAL RESULT
# ============================================================

print("\n")
print("=" * 65)
print("                 DRIVING ANALYSIS")
print("=" * 65)

print("\n--- GENETIC ALGORITHM OPTIMUM ---")

print(
    f"Optimal Speed          : "
    f"{optimal_speed:.2f} km/h"
)

print(
    f"Optimal Acceleration   : "
    f"{optimal_acceleration:.2f} m/s²"
)

print(
    f"Optimal Braking        : "
    f"{optimal_braking:.2f} m/s²"
)

print(
    f"Optimal AC Usage       : "
    f"{optimal_ac:.2f}%"
)

print(
    f"Optimal Idle Time      : "
    f"{optimal_idle:.2f} minutes"
)

print(
    f"Optimal Fuel           : "
    f"{optimal_fuel:.2f} L"
)

print(
    f"Optimal Mileage        : "
    f"{optimal_mileage:.2f} km/L"
)


print("\n--- YOUR DRIVING ---")

print(
    f"Your Speed             : "
    f"{user_speed:.2f} km/h"
)

print(
    f"Your Acceleration      : "
    f"{user_acceleration:.2f} m/s²"
)

print(
    f"Your Fuel Consumption  : "
    f"{user_fuel:.2f} L"
)

print(
    f"Your Mileage           : "
    f"{user_mileage:.2f} km/L"
)


print("\n--- ANALYSIS ---")

print(
    f"Speed Difference       : "
    f"{speed_difference:.2f} km/h"
)

print(
    f"Acceleration Difference: "
    f"{acceleration_difference:.2f} m/s²"
)

print(
    f"Extra Fuel Used        : "
    f"{fuel_difference:.2f} L"
)


# ============================================================
# ECONOMY DECISION
# ============================================================

if fuel_percentage <= 5:

    print("\nRESULT: ECONOMIC")
    print(
        "Your driving parameters are close "
        "to the GA-optimized strategy."
    )

elif fuel_percentage <= 15:

    print("\nRESULT: MODERATELY ECONOMIC")
    print(
        "Your driving is reasonably efficient, "
        "but there is room for improvement."
    )

else:

    print("\nRESULT: NOT ECONOMIC")
    print(
        "Your driving parameters consume "
        "significantly more fuel than the "
        "optimized strategy."
    )

print("=" * 65)