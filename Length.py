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