import random

def fitnessSelection(locations, fitness_values, kParent):
	total_fitness = 0
	fitness = []
	parents = []

	# Get absolute fitness of population
	for i in fitness_values:
		total_fitness += i
		
	# obtain FPS probability for each individual
	for num in fitness_values:
		fitness.append(num/total_fitness)

	for i in range(0, int(kParent)):
		parents.append(random_pick(locations, fitness))

	return parents


def parentTourney():
	pass


def random_pick(some_list, probabilities):
	x = random.uniform(0, 1)
	cumulative_probability = 0.0
	for parent, probability in zip(some_list,probabilities):
	    cumulative_probability += probability
	    #print(some_list[probability])
	    if x < cumulative_probability:
	    	break

	return parent