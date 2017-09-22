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