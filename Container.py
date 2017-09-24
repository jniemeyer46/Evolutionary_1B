class Container:
	# holds the max length and width of the problem
	maxWidth = 0
	maxlength = 0

	# holds the shape list and the total number of shapes in the list
	shapes = []
	numShapes = 0

	# The sheet of material that the shapes will be cut out of
	materialSheet = []
	population_locations = []
	population_fitness_values = []
	parents = []

	# Holds the highest solution fitness this run and the locations of the solution shapes
	solution_fitness = 0
	solution_locations = []

	# Setting for EA runs
	uniformRandom = 0

	fitnessSelection = 0
	parentTournament = 0

	truncation = 0
	offspringTournament = 0

	numEvals = 0
	avgPopFitness = 0
	bestPopFitness = 0

	# variables that are set via the config file are stored here
	numRuns = 0
	evaluations = 0
	populationSize = 0
	recombinationPool = 0
	mutationRate = 0
	numEvalsTerminate = 0
	kParent = 0
	kOffSpring = 0
	n = 0
	prob_log_file = 0
	prob_solution_file = 0
	seed = 0
