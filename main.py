from Container import Container
from copy import deepcopy
import sys
import string
import random
import time
import Length
import rotate
import shapeManipulation


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

	# User decided on the Randomized run
	if sys.argv[3] == "Random":

		# setting up variables using config file
		if sys.argv[4] == "newSeed":
			for rules in config:
				info = rules.split(" ")
				if info[0] == "fitness_evaluations":
					container.evaluations = info[1]
				elif info[0] == "runs":
					container.numRuns = info[1]
				elif info[0] == "prob_log":
					container.prob_log_file = info[1]
				elif info[0] == "prob_solution":
					container.prob_solution_file = info[1]
				elif info[0] == "seed":
					container.seed = eval(info[1])
		elif sys.argv[4] == "lastSeed":
			for rules in config:
				info = rules.split(" ")
				if info[0] == "fitness_evaluations":
					container.evaluations = info[1]
				elif info[0] == "runs":
					container.numRuns = info[1]
				elif info[0] == "prob_log":
					container.prob_log_file = info[1]
				elif info[0] == "prob_solution":
					container.prob_solution_file = info[1]
				elif info[0] == "seed":
					obtain_seed = open(container.prob_log_file).read().splitlines(3)
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

			# Open the current solution file to obtain the fitness value
			# solution_file = open(container.prob_solution_file).read().splitlines()
				
			# grabs the solution file's fitness value
			# solution_fitness = 0 # solution_file[1].split(" ")[3]

			# Titles each section with Run i, where i is the run number (1-30)
			result_log.write("Run " + str(run) + "\n")

			# run through the given amount of times given by fitness evaluation
			for fitness in range(1, int(container.evaluations)+1):
				# list of solution locations incase it is the best
				container.solution_locations = []

				# holders for length of material used
				LargestX = 0
				SmallestX = 156

				# the material sheet being used to cut out shapes
				container.materialSheet = [[0 for x in range(0, int(container.maxWidth))] for y in range(0, int(container.maxLength))]

				# for every shape in the file, choose a position
				for shape in container.shapes:
					if not shape[0].isdigit():
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


def fitnessCalc(maxLength, usedLength):
	# determine the fitness of the evaluation
	fitness_calculation = maxLength - usedLength

	return fitness_calculation


if __name__ == '__main__':
	main()