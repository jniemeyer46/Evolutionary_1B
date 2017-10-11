import random
import string

# will return the maxLength of the sheet of material
def getLength(listShapes):
	# variable to be sent back once the maximum length is found
	maxLength = 0

	for shape in listShapes:
		# splits the lines of shape into lists so they can be iterated by word
		moves = shape.split(" ")
		if shape[0].isdigit(): # not a shape, dont increase maxLength
			pass
		elif 'L' not in shape and 'R' not in shape:
			maxLength += 1
		elif 'L' in shape and 'R' not in shape:
			maxLength += 1
			for element in moves:
				if element[0] == 'L':
					maxLength += int(element[1])
		elif 'L' not in shape and 'R' in shape:
			maxLength += 1
			for element in moves:
				if element[0] == 'R':
					maxLength += int(element[1])
		else:
			# number of moves to the left and right
			LCount = 0
			RCount = 0

			for element in moves:
				if element[0] == 'L':
					LCount += int(element[1])
				elif element[0] == 'R':
					RCount += int(element[1])

			# Determine the larger and use it to increase the count
			if LCount > RCount:
				maxLength += LCount + 1
			elif LCount < RCount:
				maxLength += RCount + 1
			else:
				maxLength += LCount + 1
	return maxLength


def validPlacement(array, maxLength, maxWidth, xCord, yCord, string):
	valid = True

	#splits string into moves
	moves = string.split(" ")

	#used to save current x and y Positions
	newXcord = xCord
	newYcord = yCord

	if newXcord < 0 or newXcord >= int(maxLength) or newYcord < 0 or newYcord >= int(maxWidth):
		valid = False
		return valid

	for element in moves:
		if element[0] == 'U':
			if ((newYcord + int(element[1])) < int(maxWidth)) and not (array[newXcord][newYcord] == 1):
				for i in range(1, int(element[1]) + 1):
					if (newYcord + 1) >= int(maxWidth) or array[newXcord][newYcord + 1] == 1:
						valid = False
						return valid
					else:
						newYcord = newYcord + 1
			else:
				valid = False
				return valid
		elif element[0] == 'D':
			if (newYcord - int(element[1])) >= 0 and not (array[newXcord][newYcord] == 1):
				for i in range(1, int(element[1]) + 1):
					if (newYcord + 1) >= int(maxWidth) or array[newXcord][newYcord - 1] == 1:
						valid = False
						return valid
					else:
						newYcord = newYcord - 1
			else:
				valid = False
				return valid
		elif element[0] == 'R':
			if (newXcord + int(element[1])) < int(maxLength) and not (array[newXcord][newYcord] == 1):
				for i in range(1, int(element[1]) + 1):
					if (newXcord + 1) >= int(maxLength) or array[newXcord + 1][newYcord] == 1:
						valid = False
						return valid
					else:
						newXcord = newXcord + 1
			else:
				valid = False
				return valid
		elif element[0] == 'L':
			if (newXcord - int(element[1])) >= 0 and not (array[newXcord][newYcord] == 1):
				for i in range(1, int(element[1]) + 1):
					if (newXcord + 1) >= int(maxLength) or array[newXcord - 1][newYcord] == 1:
						valid = False
						return valid
					else:
						newXcord = newXcord - 1
			else:
				valid = False
				return valid

	return valid


def placeShape(array, maxL, xCord, yCord, string, smallest, largest):
	smallest = smallest
	largest = largest
	#splits string into moves
	moves = string.split(" ")

	# used to save current x and y Positions
	newXcord = xCord
	newYcord = yCord

	# sets the starting position of the shape
	array[newXcord][newYcord] = 1

	for element in moves:
		if element[0] == 'U':
			for i in range(0, int(element[1])):
				newYcord = newYcord + 1
				array[newXcord][newYcord] = 1
		elif element[0] == 'D':
			for i in range(0, int(element[1])):
				newYcord = newYcord - 1
				array[newXcord][newYcord] = 1
		elif element[0] == 'R':
			for i in range(0, int(element[1])):
				newXcord = newXcord + 1
				array[newXcord][newYcord] = 1
				if largest < newXcord:
					largest = newXcord
		elif element[0] == 'L':
			for i in range(0, int(element[1])):
				newXcord = newXcord - 1
				array[newXcord][newYcord] = 1
				if smallest > newXcord:
					smallest = newXcord

	return smallest, largest


def rotate_shape(num, string):
	if num == 1:
		# list of rotated elements
		word = []
		moves = string.split(" ")
		for element in moves:
			if element[0] == 'U':
				element = 'R' + element[1]
				word.append(element)
			elif element[0] == 'D':
				element = 'L' + element[1]
				word.append(element)
			elif element[0] == 'R':
				element = 'D' + element[1]
				word.append(element)
			elif element[0] == 'L':
				element = 'U' + element[1]
				word.append(element)
	elif num == 2:
		word = []
		moves = string.split(" ")
		for element in moves:
			if element[0] == 'U':
				element = 'D' + element[1]
				word.append(element)
			elif element[0] == 'D':
				element = 'U' + element[1]
				word.append(element)
			elif element[0] == 'R':
				element = 'L' + element[1]
				word.append(element)
			elif element[0] == 'L':
				element = 'R' + element[1]
				word.append(element)
	elif num == 3:
		word = []
		moves = string.split(" ")
		for element in moves:
			if element[0] == 'U':
				element = 'L' + element[1]
				word.append(element)
			elif element[0] == 'D':
				element = 'R' + element[1]
				word.append(element)
			elif element[0] == 'R':
				element = 'U' + element[1]
				word.append(element)
			elif element[0] == 'L':
				element = 'D' + element[1]
				word.append(element)

	# combines the list of elements back into a string
	shape = ' '.join(word)
	
	return shape


def fitnessCalc(maxLength, usedLength):
	# determine the fitness of the evaluation
	fitness_calculation = maxLength - usedLength
	return fitness_calculation


def recombination(sheet, maxL, maxW, shapes, test_offspring, index):
	recombination_valid = False
	x_cord, y_cord, rotation = test_offspring[int(index)]

	if rotation != 0:
		shape = rotate_shape(rotation, shapes[index])
	elif rotation == 0:
		shape = shapes[index]

	recombination_valid = validPlacement(sheet, maxL, maxW, x_cord, y_cord, shape)

	# Keep obtaining a new position until it fits on the material
	while not recombination_valid:	
		# generate random position and rotation
		x_cord = random.randrange(0, int(maxL))
		y_cord = random.randrange(0, int(maxW))
		rotation = random.randrange(0,4)

		# Rotate the shape if needed
		if rotation != 0:
			shape = rotate_shape(rotation, shapes[index])
		elif rotation == 0:
			shape = shapes[index]

		# Check whether the shape fits on the material in the current position
		recombination_valid = validPlacement(sheet, maxL, maxW, x_cord, y_cord, shape)

	return x_cord, y_cord, rotation, shape


def mutation(sheet, maxL, maxW, shape):
	mutation_valid = False
	# Keep obtaining a new position until it fits on the material
	while not mutation_valid:
		# generate random position and rotation
		x_cord = random.randrange(0, int(maxL))
		y_cord = random.randrange(0, int(maxW))
		rotation = random.randrange(0,4)

		# Rotate the shape if needed
		if rotation != 0:
			shape = rotate_shape(rotation, shape)

		mutation_valid = validPlacement(sheet, maxL, maxW, x_cord, y_cord, shape)

	return x_cord, y_cord, rotation, shape


def mutationSelfAdapt(length, mutation, up_count, down_count, string):
	
	if length == up_count:
		mutation = mutation + 0.001
		up_count = 0

		return mutation, up_count
	elif (length / 2) == down_count:
		mutation = mutation - 0.001
		down_count = 0

		return mutation, down_count

	if string == "recombination":
		return mutation, up_count
	elif string == "mutate":
		return mutation, down_count
