import csv
import random
from prettytable import PrettyTable
import streamlit as st  # Streamlit for displaying output on GitHub Pages

# Function to read the CSV file and convert it to the desired format
def read_csv_to_dict(file_path):
    program_ratings = {}

    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]  # Convert the ratings to floats
            program_ratings[program] = ratings

    return program_ratings

# Path to the CSV file
file_path = 'pages/program_ratings.csv'  # Make sure the CSV is in the same directory

def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

def initialize_pop(programs, time_slots):
    if not programs:
        return [[]]
    all_schedules = []
    for i in range(len(programs)):
        for schedule in initialize_pop(programs[:i] + programs[i + 1:], time_slots):
            all_schedules.append([programs[i]] + schedule)
    return all_schedules

def finding_best_schedule(all_schedules):
    best_schedule = []
    max_ratings = 0

    for schedule in all_schedules:
        total_ratings = fitness_function(schedule)
        if total_ratings > max_ratings:
            max_ratings = total_ratings
            best_schedule = schedule

    return best_schedule

# Defining genetic algorithm functions (crossover, mutation, etc.)

def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(initial_schedule, generations=100, population_size=50, crossover_rate=0.8, mutation_rate=0.2, elitism_size=2):
    population = [initial_schedule]
    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for generation in range(generations):
        new_population = []
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    return population[0]

# Main function for running the code
def main():
    program_ratings_dict = read_csv_to_dict(file_path)
    ratings = program_ratings_dict
    all_programs = list(ratings.keys())
    all_time_slots = list(range(6, 24))  # time slots
    all_possible_schedules = initialize_pop(all_programs, all_time_slots)

    best_schedule = finding_best_schedule(all_possible_schedules)
    genetic_schedule = genetic_algorithm(best_schedule)

    # Display results using PrettyTable and Streamlit
    table = PrettyTable()
    table.field_names = ["Time Slot", "Program"]
    for time_slot, program in enumerate(genetic_schedule):
        start_time = f"{all_time_slots[time_slot]:02d}:00"
        end_time = f"{all_time_slots[time_slot] + 1:02d}:00"
        time_range = f"{start_time} - {end_time}"
        table.add_row([time_range, program])

    st.write("Final Optimal TV Schedule:")
    st.write(table)
    st.write(f"Total Ratings: {fitness_function(genetic_schedule)}")

if __name__ == "__main__":
    main()
