Please refer to http://web.mst.edu/~tauritzd/courses/ec/cs5401fs2017/ for homework assignments.

Direct any grading questions to John Liming at jrl2n4@mst.edu


In order to run the program correctly please use the following syntax:
	./run.sh <config_file> <problem_file> <algorithm_type> <random_seed>

	* Uses the Random Search algorithm with a new seed value
		./run.sh config1.txt problem1.txt Random newSeed

	* Uses the Random Search algorithm with the seed value from the last run
		./run.sh config1.txt problem1.txt Random lastSeed

	* Uses the EA algorithm with a new seed value
		./run.sh config1.txt problem1.txt EA newSeed

	* Uses the EA algorithm with the seed value from the last run
		./run.sh config1.txt problem1.txt EA lastSeed