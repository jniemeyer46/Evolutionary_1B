from Container import Container
from copy import deepcopy
import sys
import string
import random
import time
import selections
import operations
import config_setup

def main():
	container = Container()

	#obtain configs in a list format
	config = open(sys.argv[1]).read().splitlines()

	# obtain the problem file and throw it into a list object
	container.shapes = open(sys.argv[2]).read().splitlines()

	# Variables that will be used to set the 2d array of material
	container.maxWidth = int(container.shapes[0].split(" ")[0])
	container.maxLength = int(operations.getLength(container.shapes))
	#number of shapes in the problem file
	container.numShapes = int(container.shapes[0].split(" ")[1])

	# delete the width and number of shapes from the shape list
	del container.shapes[0]

	config_setup.setup(container, config)

	# Config file says use Random Search
	if config[0] == 'Random = 1':
		# Seeds the random function using a saved value that is put into the log file
		random.seed(container.seed)

		# opening the log file 
		result_log = open(container.prob_log_file_random, 'w')
		# formatting the result log with Result Log at the top
		result_log.write("Result Log \n")
		result_log.write("Problem Instance Path = ../%s \n" % sys.argv[2])
		result_log.write("Random Seed = %s \n" % container.seed)
		result_log.write("Parameters used = {'fitness evaluations': %s, 'number of runs': %s, 'problem solution location': '%s'}\n\n"
						% (container.evaluations, container.numRuns, container.prob_solution_file_random))

		# runs through the program as many times as the config files says to
		for run in range(1, container.numRuns + 1):
			# highest fitness calculation thus far this run
			highest_fitness = 0

			# Titles each section with Run i, where i is the run number (1-30)
			result_log.write("Run " + str(run) + "\n")
			print("Run " + str(run) + "\n")

			# run through the given amount of times given by fitness evaluation
			for fitness in range(1, container.evaluations + 1):
				# holders for length of material used
				LargestX = 0
				SmallestX = container.maxLength - 1

				# clears the solution list each evaluation
				container.solution_locations.clear()

				# the material sheet being used to cut out shapes
				container.materialSheet = [[0 for x in range(0, container.maxWidth)] for y in range(0, container.maxLength)]

				# for every shape in the file, choose a position
				for shape in container.shapes:
					valid = False

					# Keep obtaining a new position until it fits on the material
					while not valid:
						# generate random position and rotation
						x_cord = random.randrange(0, container.maxLength)
						y_cord = random.randrange(0, container.maxWidth)
						rotation = random.randrange(0,4)

						# Rotate the shape if needed
						if rotation != 0:
							shape = operations.rotate_shape(rotation, shape)

						# Check whether the shape fits on the material in the current position
						valid = operations.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)
							
						# if the move was valid and was placed
						if valid:
							SmallestX, LargestX = operations.placeShape(container.materialSheet, container.maxLength, x_cord, y_cord, shape, SmallestX, LargestX)
							# store the location in a tuple if it worked
							placementLocation = (x_cord, y_cord, rotation)
							# append it to the list
							container.solution_locations.append(placementLocation)

				# Determines the Length of the material used by this iteration
				usedLength = ((LargestX - SmallestX) + 1)
				current_fitness = operations.fitnessCalc(container.maxLength, usedLength)

				# Determines if the current fitness is higher than the highest fitness this run
				# if it is, writes it to the log file
				if highest_fitness < current_fitness:
					highest_fitness = current_fitness
					result_log.write(str(fitness) + "	" + str(highest_fitness) + "\n")
					print(str(fitness) + "	" + str(highest_fitness))

				# If the current solution is the best, replace the current solution with the new solution
				if container.solution_fitness < highest_fitness:
					# set the new solution fitness value
					container.solution_fitness = current_fitness

					# Write the shape configuration to the solution file
					solution_file = open(container.prob_solution_file_random, 'w')

					solution_file.write("Solution File \n\n")
					for i in range(len(container.solution_locations)):
						solution_file.write(str(container.solution_locations[i])[1:-1] + "\n")
										
			# formatting the result log with a space after each run block
			result_log.write("\n")

		result_log.close()
		solution_file.close()

	# User wants the EA run
	elif config[1] == "EA = 1":
		# Seeds the random function using a saved value that is put into the log file
		random.seed(container.seed)

		# opening the log file 
		result_log = open(container.prob_log_file_EA, 'w')
		# formatting the result log with Result Log at the top and parameters used
		result_log.write("Result Log \n")
		result_log.write("Problem Instance Path = ../%s \n" % sys.argv[2])
		result_log.write("Random Seed = %s \n" % container.seed)
		result_log.write("Initialization = {'Uniform_Random': %s }\n" % container.uniformRandom)
		result_log.write("Parent_Selection = {'Fitness_Proportional_Selection': %s,'k-Tournament_Selection_with_replacement': %s}\n" % (container.fitnessSelection, container.parentTournament))
		result_log.write("Survival_Selection = {'Truncation': %s, 'k-Tournament_Selection_without_replacement': %s}\n" % (container.truncation, container.offspringTournament))
		result_log.write("Termination = {'Number_of_evals': %s, 'no_change_in_average_population_fitness_for_n_generations': %s, 'no_change_in_best_fitness_in_population_for_n_generations': %s}\n" % (container.numEvals, container.avgPopFitness, container.bestPopFitness))
		result_log.write("Parameters used = {'fitness evaluations': %s, 'number of runs': %s, 'problem solution location': '%s', 'mutation_rate': %s, 'mu': %s, 'lambda': %s}\n\n" % (container.evaluations, container.numRuns, container.prob_solution_file_EA, container.mutationRate, container.populationSize, container.offspringSize))

		# runs through the program as many times as the config files says to
		for run in range(1, container.numRuns + 1):
			# highest fitness calculation thus far this run
			highest_fitness = 0
			best_run_fitness = 0
			average_run_fitness = 0

			# clear the population for the next run
			container.population_locations.clear()
			container.population_fitness_values.clear()
			container.best_fitness_holder.clear()
			container.average_fitness_holder.clear()

			# Titles each section with Run i, where i is the run number (1-30)
			result_log.write("Run " + str(run) + "\n")
			print("Run " + str(run) + "\n")
			
			'''------INITIALIZATION------'''
			for person in range(0, container.populationSize):
				# holders for length of material used
				LargestX = 0
				SmallestX = int(container.maxLength) - 1

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
							shape = operations.rotate_shape(rotation, shape)

						# Check whether the shape fits on the material in the current position
						valid = operations.validPlacement(container.materialSheet, container.maxLength, container.maxWidth, x_cord, y_cord, shape)
							
						# if the move was valid and was placed
						if valid:
							SmallestX, LargestX = operations.placeShape(container.materialSheet, container.maxLength, x_cord, y_cord, shape, SmallestX, LargestX)
							# store the location in a tuple if it worked
							placementLocation = (x_cord, y_cord, rotation)
							# append it to the list
							container.solution_locations.append(placementLocation)

				# Make a list containing all people in a population
				container.population_locations.append(container.solution_locations)

				# Determines the Length of the material used by this iteration
				usedLength = ((LargestX - SmallestX) + 1)
				current_fitness = operations.fitnessCalc(container.maxLength, usedLength)

				# Make a list of fitness values associated with each person in the population
				container.population_fitness_values.append(current_fitness)


			'''------OBTAINING FIRST RESULT LOG ROW RESULTS------'''
			best_fitness = 0
			average_fitness = 0

			for i in container.population_fitness_values:
				if int(i) > best_fitness:
					best_fitness = int(i)

			for i in container.population_fitness_values:
				average_fitness += int(i)
			average_fitness = average_fitness / int(container.populationSize)


			# Print and write the results to the file/screen
			result_log.write(str(container.populationSize) + "     " + str("%.4f" % float(container.mutationRate)) + "     " + str(round(average_fitness)) + "     " + str(best_fitness) + "\n")
			print(str(container.populationSize) + "     " + str("%.4f" % float(container.mutationRate)) + "     " + str(round(average_fitness)) + "     " + str(best_fitness) + "\n")

			'''------START OF THE EA------'''
			for fitness in range(1, container.evaluations + 1):
				# clear the population for the next run
				container.mutated_offspring.clear()
				container.mutated_offspring_fitness.clear()
				container.offspring.clear()
				container.offspring_fitness.clear()

				'''------Parent Selection------'''
				# if the user wants uniform random selection
				if container.uniformRandomParent == 1:
					container.parents = selections.uniformRandomParent(container.population_locations, container.population_fitness_values, int(container.kParent))
				# if the user wants fitness proportional selection
				elif container.fitnessSelection == 1:
					container.parents = selections.fitnessSelection(container.population_locations, container.population_fitness_values, int(container.kParent))
				# if the user wants tournament selection
				elif container.parentTournament == 1:
					container.parents = selections.parentTournament(container.population_locations, container.population_fitness_values, int(container.kParent))
				# if the user didnt set their parent selector
				else:
					print("You did not select a parent selection method in the configuration file")


				'''------Recombination------and------Mutation------'''
				for index in range(0, int(container.offspringSize)):
					# holders for length of material used
					LargestX = 0
					SmallestX = int(container.maxLength) - 1

					# Used to self adapt the mutation operators if it isnt being used often enough
					nonMutation_count = 0
					Mutation_count = 0

					# Stores the newly created offspring
					mutated_offspring = []

					# the material sheet being used to cut out shapes
					container.materialSheet = [[0 for x in range(0, int(container.maxWidth))] for y in range(0, int(container.maxLength))]

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
						# obtain a random chance for mutation
						mutate = random.random()

						# ------RECOMBINATION------
						if mutate > float(container.mutationRate):
							# Does the recombination, found in Recombination File
							x_cord, y_cord, rotation, shape = operations.recombination(container.materialSheet, container.maxLength, container.maxWidth, container.shapes, test_offspring, index)

							# This count will determine when the mutation is too low
							nonMutation_count += 1

							# This determines whether the mutation rate is in need of an increase or not
							if container.adaptiveMutation:
								# Increase the mutation rate by .1%
								container.mutationRate, nonMutation_count = operations.mutationSelfAdapt(len(container.shapes), container.mutationRate, nonMutation_count, Mutation_count, "recombination")

						else:  # no penalty for recombination if mutation is occuring
							x_cord, y_cord, rotation, shape = operations.recombination(container.materialSheet, container.maxLength, container.maxWidth, container.shapes, test_offspring, index)
						
						# ----MUTATION-----
						# If necessary mutate
						if mutate <= float(container.mutationRate):
							x_cord, y_cord, rotation, shape = operations.mutation(container.materialSheet, container.maxLength, container.maxWidth, shape)

							# This count will determine if there is too much mutation happening
							Mutation_count += 1

							# This determines whether it is time to increase the mutation rate or not
							if container.adaptiveMutation:
								# Decrease the mutation rate by .1%
								container.mutationRate, Mutation_count = operations.mutationSelfAdapt(len(container.shapes), container.mutationRate, nonMutation_count, Mutation_count, "mutate")

						# Place the newly created shape if it is valid
						SmallestX, LargestX = operations.placeShape(container.materialSheet, container.maxLength, x_cord, y_cord, shape, SmallestX, LargestX)

						# store the location in a tuple if it worked
						placementLocation = (x_cord, y_cord, rotation)

						# Create the true offspring
						mutated_offspring.append(placementLocation)

					container.mutated_offspring.append(mutated_offspring)

					# Determines the Length of the material used by this iteration
					usedLength = ((LargestX - SmallestX) + 1)
					current_fitness = operations.fitnessCalc(container.maxLength, usedLength)

					# If the current solution is the best, replace the current solution with the new solution
					if container.solution_fitness < current_fitness:
						# set the new solution fitness value
						container.solution_fitness = current_fitness

						# Write the shape configuration to the solution file
						solution_file = open(container.prob_solution_file_EA, 'w')

						solution_file.write("Solution File \n\n")
						for i in range(0, len(mutated_offspring)):
							solution_file.write(str(mutated_offspring[i])[1:-1] + "\n")

					# Make a list of fitness values associated with each person in the population
					container.mutated_offspring_fitness.append(current_fitness)


					'''------Termination------'''
					if container.numEvals == 1 and int(container.numEvalsTerminate) == index:
						break
					elif container.avgPopFitness == 1:
						count = 0
						end = False

						for num in container.mutated_offspring_fitness:
							if count >= int(container.n) - 1:
								end = True
							elif int(num) == int(round(average_run_fitness)):
								count += 1
						if end:
							break
					elif container.mutated_offspring_fitness == 1:
						count = 0
						end = False

						for num in container.best_fitness_holder:
							if count >= int(container.n) - 1:
								end = True
							elif num == best_run_fitness:
								count += 1					
						if end:
							break


				'''------Survival Strategy Implementation and Survival Selection------'''
				if container.survivalStrategyPlus:
					container.mutated_offspring = container.mutated_offspring + container.population_locations
					container.mutated_offspring_fitness = container.mutated_offspring_fitness + container.population_fitness_values
				elif container.survivalStrategyComma:
					# Parents are automaticaly killed off after this, no implementation for this particular part needed
					pass


				'''------Survival Selection------'''
				if container.uniformRandomSurvival == 1:
					container.offspring, container.offspring_fitness = deepcopy(selections.uniformRandomSurvival(container.mutated_offspring, container.mutated_offspring_fitness, int(container.kOffspring)))
				elif container.truncation == 1:
					container.offspring = deepcopy(container.mutated_offspring[0: int(container.kOffspring)])
					container.offspring_fitness = deepcopy(container.mutated_offspring_fitness[0: int(container.kOffspring)])
				elif container.offspringTournament == 1:				
					container.offspring, container.offspring_fitness = deepcopy(selections.offspringTournament(container.mutated_offspring, container.mutated_offspring_fitness, container.kOffspring))


				# Stores the new population to be used in the following generations	(Uses the survival strategy through survival selection)
				container.population_locations = deepcopy(container.offspring)
				container.population_fitness_values = deepcopy(container.offspring_fitness)

				'''------Result Log Formatting Evaluations------'''
				average_fitness = 0
				for i in container.offspring_fitness:
					if int(i) > best_run_fitness:
						best_run_fitness = int(i)

				container.best_fitness_holder.append(best_run_fitness)

				for i in container.offspring_fitness:
					average_fitness += int(i)
				average_fitness = average_fitness / int(container.kOffspring) 

				container.average_fitness_holder.append(round(average_fitness))

				for i in container.average_fitness_holder:
					average_run_fitness += i
				average_run_fitness = average_run_fitness / len(container.average_fitness_holder)


				# Printing and writing the results to the log/screen
				result_log.write(str(fitness) + "     " + str("%.4f" % container.mutationRate) + "     " + str("%.2f" % average_run_fitness) + "     " + str(best_run_fitness) + "\n")
				if fitness % 20 == 0:
					print(str(fitness) + "     " + str("%.4f" % container.mutationRate) + "     " + str("%.2f" % average_run_fitness) + "     " + str(best_run_fitness))
			# formatting the result log with a space after each run block
			result_log.write("\n")

		result_log.close()


if __name__ == '__main__':
	main()

