from Container import Container
from copy import deepcopy
import sys
import string
import random
import time
import Length
import rotate
import shapeManipulation
import selections


def main():
	container = Container()

	#obtain configs in a list format
	config = open(sys.argv[1]).read().splitlines()

	# obtain the problem file and throw it into a list object
	container.shapes = open(sys.argv[2]).read().splitlines()

	# Variables that will be used to set the 2d array of material
	container.maxWidth = container.shapes[0].split(" ")[0]
	container.maxLength = Length.getLength(container.shapes)
	#number of shapes in the problem file
	container.numShapes = container.shapes[0].split(" ")[1]

	# delete the width and number of shapes from the shape list
	del container.shapes[0]

	# User wants the Random Search run
	if sys.argv[3] == "Random":
		# makes sure only the config settings for the Random Search are used
		config = config[0:8]

		# setting up variables using config file
		for rules in config:
			info = rules.split(" ")
			if info[0] == "fitness_evaluations:":
				container.evaluations = info[1]
			elif info[0] == "runs:":
				container.numRuns = info[1]
			elif info[0] == "prob_log:":
				container.prob_log_file = info[1]
			elif info[0] == "prob_solution:":
				container.prob_solution_file = info[1]
			elif info[0] == "seed:" and sys.argv[4] == "newSeed":
				container.seed = eval(info[1])
			elif info[0] == "seed:" and sys.argv[4] == "lastSeed":
				obtain_seed = open(container.prob_log_file).read().splitlines()
				for lines in obtain_seed:
					line = lines.split(" ")
					if line[0] == "Random":
						container.seed = line[3]
						break

		# Seeds the random function using a saved value that is put into the log file
		random.seed(container.seed)

		# opening the log file 
		result_log = open(container.prob_log_file, 'w')
		# formatting the result log with Result Log at the top
		result_log.write("Result Log \n")
		result_log.write("Problem Instance Path = ../%s \n" % sys.argv[2])
		result_log.write("Random Seed = %s \n" % container.seed)
		result_log.write("Parameters used = {'fitness evaluations': %s, 'number of runs': %s, 'problem solution location': '%s'}\n\n"
						% (container.evaluations, container.numRuns, container.prob_solution_file))

		# runs through the program as many times as the config files says to
		for run in range(1, int(container.numRuns) + 1):
			# highest fitness calculation thus far this run
			highest_fitness = 0

			# Titles each section with Run i, where i is the run number (1-30)
			result_log.write("Run " + str(run) + "\n")

			# run through the given amount of times given by fitness evaluation
			for fitness in range(1, int(container.evaluations)+1):
				# holders for length of material used
				LargestX = 0
				SmallestX = 156

				# clears the solution list each evaluation
				container.solution_locations.clear()

				# the material sheet being used to cut out shapes
				container.materialSheet = [[0 for x in range(0, int(container.maxWidth))] for y in range(0, int(container.maxLength))]

				# for every shape in the file, choose a position
				for shape in container.shapes:
					valid = False

					# Keep obtaining a new position until it fits on the material
					while not valid:
						# generate random position and rotation
						x_cord = random.randrange(0, int(container.maxLength))
						y_cord = random.randrange(0, int(container.maxWidth))
						rotation = random.randrange(0,4)

						# Rotate the shape if needed
						if rotation != 0:
							shape = rotate.rotate_shape(rotation, shape)

						# Check whether the shape fits on the material in the current position
						valid = shapeManipulation.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)
							
						# if the move was valid and was placed
						if valid:
							shapeManipulation.placeShape(container.materialSheet, x_cord, y_cord, shape)
							# store the location in a tuple if it worked
							placementLocation = (x_cord, y_cord, rotation)
							# append it to the list
							container.solution_locations.append(placementLocation)

				# obtains the smallest and largest position in the material array
				for i in range(len(container.materialSheet)):
					if 1 in container.materialSheet[i]:
						if i < SmallestX:
							SmallestX = i
						elif i > LargestX:
							LargestX = i

				# Determines the Length of the material used by this iteration
				usedLength = ((LargestX - SmallestX) + 1)
				current_fitness = fitnessCalc(container.maxLength, usedLength)

				# Determines if the current fitness is higher than the highest fitness this run
				# if it is, writes it to the log file
				if highest_fitness < current_fitness:
					highest_fitness = current_fitness
					result_log.write(str(fitness + 1 ) + "	" + str(current_fitness) + "\n")

				# If the current solution is the best, replace the current solution with the new solution
				if container.solution_fitness < current_fitness:
					# set the new solution fitness value
					container.solution_fitness = current_fitness

					# Write the shape configuration to the solution file
					solution_file = open(container.prob_solution_file, 'w')

					solution_file.write("Solution File \n\n")
					for i in range(len(container.solution_locations)):
						solution_file.write(str(container.solution_locations[i])[1:-1] + "\n")
										
			# formatting the result log with a space after each run block
			result_log.write("\n")

		result_log.close()
		solution_file.close()

	# User wants the EA run
	elif sys.argv[3] == "EA":
		# setting up variables using config file
		for rules in config:

			# Gets rid of the Random Search Configurations
			if rules == "::::Random Search::::":
				del config[0:8]

			# split the rules into words
			info = rules.split(" ")

			if info[0] == "μ:":
				container.populationSize = info[1]
			elif info[0] == "λ:":
				container.offspringSize = info[1]
			elif info[0] == "runs:":
				container.numRuns = info[1]
			elif info[0] == "seed:" and sys.argv[4] == "newSeed":
				container.seed = eval(info[1])
			elif info[0] == "seed:" and sys.argv[4] == "lastSeed":
				obtain_seed = open(container.prob_log_file).read().splitlines(3)
				for lines in obtain_seed:
					line = lines.split(" ")
					if line[0] == "Random":
						container.seed = line[3]
						break
			elif info[0] == "mutation_rate:":
				container.mutationRate = info[1]
			elif info[0] == "fitness_evaluations:":
				container.evaluations = info[1]
			elif info[0] == "prob_log:":
				container.prob_log_file = info[1]
			elif info[0] == "number_of_evals_till_termination:":
				container.numEvalsTerminate = info[1]
			elif info[0] == "tournament_size_for_parent_selection:":
				container.kParent = info[1]
			elif info[0] == "tournament_size_for_survival_selection:":
				container.kOffspring = info[1]
			elif info[0] == "n_for_termination_convergence_criterion:":
				container.n = info[1]
			elif info[0] == "prob_solution:":
				container.prob_solution_file = info[1]
			elif info[0] == "Initialization:":
				if info[1] == "Uniform_Random:" and info[2] == '1':
					# sets flag for uniform random
					container.uniformRandom = 1
			elif info[0] == "Parent_Selection:":
				if info[1] == "Fitness_Proportional_Selection:" and info[2] == '1,':
					# sets flag for fitness selection
					container.fitnessSelection = 1
				elif info[3] == "k-Tournament_Selection_with_replacement:" and info[4] == '1':
					# sets flag for parent tournament
					container.parentTournament = 1
			elif info[0] == "Survival_Selection:":
				if info[1] == "Truncation:" and info[2] == '1,':
					container.truncation = 1
				elif info[3] == "k-Tournament_Selection_without_replacement:" and info[4] == '1':
					container.offspringTournament = 1
			elif info[0] == "Termination:":
				if info[1] == "Number_of_evals:" and info[2] == '1,':
					container.numEvals = 1
				elif info[3] == "no_change_in_average_population_fitness_for_n_generations:" and info[4] == '1,':
					# sets flag for parent tournament
					container.avgPopFitness = 1
				elif info[5] == "no_change_in_best_fitness_in_population_for_n_generations:" and info[6] == '1':
					# sets flag for parent tournament
					container.bestPopFitness = 1

		# Seeds the random function using a saved value that is put into the log file
		random.seed(container.seed)

		# opening the log file 
		result_log = open(container.prob_log_file, 'w')
		# formatting the result log with Result Log at the top and parameters used
		result_log.write("Result Log \n")
		result_log.write("Problem Instance Path = ../%s \n" % sys.argv[2])
		result_log.write("Random Seed = %s \n" % container.seed)
		result_log.write("Initialization = {'Uniform_Random': %s }\n" % container.uniformRandom)
		result_log.write("Parent_Selection = {'Fitness_Proportional_Selection': %s,'k-Tournament_Selection_with_replacement': %s}\n" % (container.fitnessSelection, container.parentTournament))
		result_log.write("Survival_Selection = {'Truncation': %s, 'k-Tournament_Selection_without_replacement': %s}\n" % (container.truncation, container.offspringTournament))
		result_log.write("Termination = {'Number_of_evals': %s, 'no_change_in_average_population_fitness_for_n_generations': %s, 'no_change_in_best_fitness_in_population_for_n_generations': %s}\n" % (container.numEvals, container.avgPopFitness, container.bestPopFitness))
		result_log.write("Parameters used = {'fitness evaluations': %s, 'number of runs': %s, 'problem solution location': '%s', 'mutation_rate': %s, 'μ': %s, 'λ': %s}\n\n" % (container.evaluations, container.numRuns, container.prob_solution_file, container.mutationRate, container.populationSize, container.offspringSize))

		# runs through the program as many times as the config files says to
		for run in range(1, int(container.numRuns) + 1):
			# highest fitness calculation thus far this run
			highest_fitness = 0

			# clear the population for the next run
			container.population_locations.clear()
			container.population_fitness_values.clear()
			container.recombined_offspring.clear()
			container.mutated_offspring.clear()
			container.mutated_offspring_fitness.clear()

			# Titles each section with Run i, where i is the run number (1-30)
			result_log.write("Run " + str(run) + "\n")

			
			'''------INITIALIZATION------'''
			for person in range(0, int(container.populationSize)):
				# holders for length of material used
				LargestX = 0
				SmallestX = 156

				# clears the solution for each evaluation
				container.solution_locations.clear()

				# the material sheet being used to cut out shapes
				container.materialSheet = [[0 for x in range(0, int(container.maxWidth))] for y in range(0, int(container.maxLength))]

				# for every shape in the file, choose a position
				for shape in container.shapes:
					valid = False
					# Keep obtaining a new position until it fits on the material
					while not valid:
						# generate random position and rotation
						x_cord = random.randrange(0, int(container.maxLength))
						y_cord = random.randrange(0, int(container.maxWidth))
						rotation = random.randrange(0,4)

						# Rotate the shape if needed
						if rotation != 0:
							shape = rotate.rotate_shape(rotation, shape)

						# Check whether the shape fits on the material in the current position
						valid = shapeManipulation.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)
							
						# if the move was valid and was placed
						if valid:
							shapeManipulation.placeShape(container.materialSheet, x_cord, y_cord, shape)
							# store the location in a tuple if it worked
							placementLocation = (x_cord, y_cord, rotation)
							# append it to the list
							container.solution_locations.append(placementLocation)

				# Make a list containing all people in a population
				container.population_locations.append(container.solution_locations)

				# obtains the smallest and largest position in the material array
				for i in range(len(container.materialSheet)):
					if 1 in container.materialSheet[i]:
						if i < SmallestX:
							SmallestX = i
						elif i > LargestX:
							LargestX = i

				# Determines the Length of the material used by this iteration
				usedLength = ((LargestX - SmallestX) + 1)
				current_fitness = fitnessCalc(container.maxLength, usedLength)

				# Make a list of fitness values associated with each person in the population
				container.population_fitness_values.append(current_fitness)


			'''------Parent Selection------'''
			# if the user wants fitness proportional selection
			if container.fitnessSelection == 1:
				container.parents = deepcopy(selections.fitnessSelection(container.population_locations, container.population_fitness_values, container.kParent))
			# if the user wants tournament selection
			elif container.parentTournament == 1:
				container.parents = deepcopy(selections.parentTournament(container.population_locations, container.population_fitness_values, container.kParent))
			# if the user didnt set their parent selector
			else:
				print("You did not select a parent selection method in the configuration file")


			'''------Recombination------'''
			for index in range(0, int(container.offspringSize)):
				# holds the valid recombined offspring offspring
				recombined_offspring = []

				# obtain the two parents for recombination
				parent1 = random.randrange(0, len(container.parents))
				parent2 = random.randrange(0, len(container.parents))

				# determine the amout of genes used from parent 1... the rest form parent 2
				amount_parent1_genes = random.randrange(0, len(container.shapes))

				parent1_genes = deepcopy(container.parents[parent1][0:amount_parent1_genes])
				parent2_genes = deepcopy(container.parents[parent2][amount_parent1_genes: len(container.shapes)])

				test_offspring = parent1_genes + parent2_genes

				# for every shape in the file, choose a position
				for index in range(0, len(test_offspring)):
					valid = False


					# the material sheet being used to cut out shapes
					container.materialSheet = [[0 for x in range(0, int(container.maxWidth))] for y in range(0, int(container.maxLength))]

					x_cord, y_cord, rotation = test_offspring[index]


					if rotation != 0:
						shape = rotate.rotate_shape(rotation, container.shapes[index])
					elif rotation == 0:
						shape = container.shapes[index]

					valid = shapeManipulation.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)

					# Keep obtaining a new position until it fits on the material
					while not valid:
						# generate random position and rotation
						x_cord = random.randrange(0, int(container.maxLength))
						y_cord = random.randrange(0, int(container.maxWidth))
						rotation = random.randrange(0,4)

						# Rotate the shape if needed
						if rotation != 0:
							shape = rotate.rotate_shape(rotation, container.shapes[index])
						elif rotation == 0:
							shape = container.shapes[index]

						# Check whether the shape fits on the material in the current position
						valid = shapeManipulation.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)
							

					shapeManipulation.placeShape(container.materialSheet, x_cord, y_cord, shape)
					# store the location in a tuple if it worked
					placementLocation = (x_cord, y_cord, rotation)

					# Create the true offspring
					recombined_offspring.append(placementLocation)

				container.recombined_offspring.append(recombined_offspring)


			'''------Mutation------'''
			for offspring in container.recombined_offspring:
				# holders for length of material used
				LargestX = 0
				SmallestX = 156

				mutated_offspring = []

				# the material sheet being used to cut out shapes
				container.materialSheet = [[0 for x in range(0, int(container.maxWidth))] for y in range(0, int(container.maxLength))]

				for index in range(0, len(offspring)):
					valid = False

					x_cord, y_cord, rotation = offspring[index]


					if rotation != 0:
						shape = rotate.rotate_shape(rotation, container.shapes[index])
					elif rotation == 0:
						shape = container.shapes[index]

					valid = shapeManipulation.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)

					# Keep obtaining a new position until it fits on the material
					while not valid:
						# generate random position and rotation
						x_cord = random.randrange(0, int(container.maxLength))
						y_cord = random.randrange(0, int(container.maxWidth))
						rotation = random.randrange(0,4)

						# Rotate the shape if needed
						if rotation != 0:
							shape = rotate.rotate_shape(rotation, container.shapes[index])
						elif rotation == 0:
							shape = container.shapes[index]

						# Check whether the shape fits on the material in the current position
						valid = shapeManipulation.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)
							

					shapeManipulation.placeShape(container.materialSheet, x_cord, y_cord, shape)
					# store the location in a tuple if it worked
					placementLocation = (x_cord, y_cord, rotation)

					# Create the true offspring
					mutated_offspring.append(placementLocation)

				container.mutated_offspring.append(recombined_offspring)

				# obtains the smallest and largest position in the material array
				for i in range(len(container.materialSheet)):
					if 1 in container.materialSheet[i]:
						if i < SmallestX:
							SmallestX = i
						elif i > LargestX:
							LargestX = i

				# Determines the Length of the material used by this iteration
				usedLength = ((LargestX - SmallestX) + 1)
				current_fitness = fitnessCalc(container.maxLength, usedLength)

				# Make a list of fitness values associated with each person in the population
				container.mutated_offspring_fitness.append(current_fitness)
	

			'''------Survival Selection------'''
			if container.truncation == 1:
				container.mutated_offspring = deepcopy(container.mutated_offspring[0: int(container.kOffspring)])
				container.mutated_offspring_fitness = deepcopy(container.mutated_offspring_fitness[0: int(container.kOffspring)])
				print(container.mutated_offspring)
				print(container.mutated_offspring_fitness)
			elif container.offspringTournament == 1:
				pass


			'''------Termination------'''


			# formatting the result log with a space after each run block
			result_log.write("\n")

		result_log.close()


def fitnessCalc(maxLength, usedLength):
	# determine the fitness of the evaluation
	fitness_calculation = maxLength - usedLength

	return fitness_calculation


if __name__ == '__main__':
	main()