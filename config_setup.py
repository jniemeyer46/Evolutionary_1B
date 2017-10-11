import string
import time

def setup(container, config):
	# setting up variables using config file
	for rules in config:
		# split the rules into words
		info = rules.split(" ")

		if info[0] == "mu:":
			container.populationSize = int(info[1])
		elif info[0] == "lambda:":
			container.offspringSize = int(info[1])
		elif info[0] == "runs:":
			container.numRuns = int(info[1])
		elif info[0] == "newSeed":
			if info[2] == '1':
				for rules in config:
					info = rules.split(" ")
					if info[0] == "seed:":
						container.seed = eval(info[1])
						break
			else:
				obtain_seed = open(container.prob_log_file).read().splitlines(3)
				for lines in obtain_seed:
					line = lines.split(" ")
					if line[0] == "Random":
						container.seed = line[3]
						break
		elif info[0] == "selfAdaptive:":
			if info[1] == "adaptMutation:" and info[2] == '1':
				container.adaptiveMutation = 1
		elif info[0] == "mutation_rate:":
			container.mutationRate = float(info[1])
		elif info[0] == "fitness_evaluations:":
			container.evaluations = int(info[1])
		elif info[0] == "prob_log_random:":
			container.prob_log_file_random = info[1]
		elif info[0] == "prob_log_EA:":
			container.prob_log_file_EA = info[1]
		elif info[0] == "number_of_evals_till_termination:":
			container.numEvalsTerminate = int(info[1])
		elif info[0] == "tournament_size_for_parent_selection:":
			container.kParent = int(info[1])
		elif info[0] == "tournament_size_for_survival_selection:":
			container.kOffspring = int(info[1])
		elif info[0] == "n_for_termination_convergence_criterion:":
			container.n = int(info[1])
		elif info[0] == "prob_solution_random:":
			container.prob_solution_file_random = info[1]
		elif info[0] == "prob_solution_EA:":
			container.prob_solution_file_EA = info[1]
		elif info[0] == "Initialization:":
			if info[1] == "Uniform_Random:" and info[2] == '1':
				# sets flag for uniform random
				container.uniformRandom = 1
		elif info[0] == "Parent_Selection:":
			if info[1] == "Uniform_random_parent:" and info[2] == '1,':
				# sets flag for Uniform random selection
				container.uniformRandomParent = 1
			elif info[3] == "Fitness_Proportional_Selection:" and info[4] == '1,':
				# sets flag for fitness selection
				container.fitnessSelection = 1
			elif info[5] == "k-Tournament_Selection_with_replacement:" and info[6] == '1':
				# sets flag for parent tournament
				container.parentTournament = 1
		elif info[0] == "Survival_Strategy:":
			if info[1] == "plus:" and info[2] == '1,':
				container.survivalStrategyPlus = 1
			elif info[3] == 'comma:' and info[2] == '1':
				container.survivalStrategyComma = 1
		elif info[0] == "Survival_Selection:":
			if info[1] == "Uniform_random_survival:" and info[2] == '1,':
				container.uniformRandomSurvival = 1
			if info[3] == "Truncation:" and info[4] == '1,':
				container.truncation = 1
			elif info[5] == "k-Tournament_Selection_without_replacement:" and info[6] == '1':
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
