import string


def validPlacement(array, maxLength, maxWidth, xCord, yCord, string):
	valid = True

	#splits string into moves
	moves = string.split(" ")

	#used to save current x and y Positions
	newXcord = xCord
	newYcord = yCord

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


def placeShape(array, xCord, yCord, string):
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
		elif element[0] == 'L':
			for i in range(0, int(element[1])):
				newXcord = newXcord - 1
				array[newXcord][newYcord] = 1
