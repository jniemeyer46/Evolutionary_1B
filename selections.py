from copy import deepcopy
import random

def uniformRandomParent(locations, fitness_values, kParents):
	parents = []

	for i in range(int(kParents)):
		parent = random.randrange(0, len(locations))
		parents.append(locations[parent])

	return parents


# returns a list of parents using fitness proportionate selection portion of the EA
def fitnessSelection(locations, fitness_values, kParent):
	total_fitness = 0
	fitness_prob = []
	parents = []

	# Get absolute fitness of population
	for i in fitness_values:
		total_fitness += i
		
	# obtain FPS probability for each individual
	for num in fitness_values:
		fitness_prob.append(num/total_fitness)

	for i in range(0, int(kParent)):
		parents.append(random_probability_pick(locations, fitness_prob))

	return parents


# returns a parent chosen based on their probability of being chosen
def random_probability_pick(some_list, probabilities):
	x = random.uniform(0, 1)
	cumulative_probability = 0.0
	for parent, probability in zip(some_list, probabilities):
	    cumulative_probability += probability
	    #print(some_list[probability])
	    if x < cumulative_probability:
	    	break

	return parent


# returns a list of parents using k-tournament selection with replacement
def parentTournament(locations, fitness_values, kParent):
	parents = []

	for num in range(0, int(kParent)):
		highest_index = 0

		tournament_pool, tournament_fitness_pool = deepcopy(createParentTourney(locations, fitness_values, kParent))
		
		for index in range(0, len(tournament_fitness_pool)):
			if tournament_fitness_pool[index] > tournament_fitness_pool[highest_index] and index < len(locations):
				highest_index = index

		parents.append(locations[highest_index])

	return parents


def createParentTourney(locations, fitness_values, kParent):
	Tourney_participants = []
	Tourney_participants_fitness_values = []

	for i in range(0, int(kParent)):
		rand_location = random.randrange(0, len(locations))
		Tourney_participants.append(locations[rand_location])
		Tourney_participants_fitness_values.append(fitness_values[rand_location])

	return Tourney_participants, Tourney_participants_fitness_values


def uniformRandomSurvival(locations, fitness_values, kOffspring):
	offspring = []
	offspring_fitness = []

	for i in range(int(kOffspring)):
		randOffspring = random.randrange(0, len(locations))
		offspring.append(locations[randOffspring])
		offspring_fitness.append(fitness_values[randOffspring])

	return offspring, offspring_fitness


def offspringTournament(locations, fitness_values, kOffspring):
	offspring = []
	offspring_fitness = []

	for num in range(0, int(kOffspring)):
		highest_index = 0

		tournament_pool, tournament_fitness_pool = deepcopy(createParentTourney(locations, fitness_values, kOffspring))

		for index in range(0, len(tournament_fitness_pool)):
			if tournament_fitness_pool[index] > tournament_fitness_pool[highest_index] and index < len(locations):
				highest_index = index

		offspring.append(locations[highest_index])
		del locations[highest_index]
		offspring_fitness.append(fitness_values[highest_index])
		del fitness_values[highest_index]

	return offspring, offspring_fitness


def createOffspringTourney(locations, fitness_values, kOffspring):
	Tourney_participants = []
	Tourney_participants_fitness_values = []

	for i in range(0, int(kOffspring)):
		rand_location = random.randrange(0, len(locations))
		Tourney_participants.append(locations[rand_location])
		Tourney_participants_fitness_values.append(fitness_values[rand_location])

	return Tourney_participants, Tourney_participants_fitness_values






