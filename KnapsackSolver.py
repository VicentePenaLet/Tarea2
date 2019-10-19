from Knapsack import *
import random
import numpy as np

#This fucntion generates a list of knapsacks with random solutions
def populationGenerator(populationSize,bagSize):
    population = []
    for i in range(populationSize):
        #Create a kanpsack with a random solution and append to the list
        population.append(Knapsack(bagSize))
    return population

#The fitness of an individual is simply its solution weight
def fitnessFunction(bag):
    return bag.solutionValue

#The KanpsackSolver class defines the solver for the kanpsack problem using a genetic algorithm
class KnapsackSolver:
    #Tho constructor of the class requires the population size, the maximun capacity of the bag, the problem fitness function
    #addiotianlly the mutation rate and tournament size can be given as parameters
    def __init__(self, populationSize, bagSize, fitnessFunction, mutationRate = 0.5, tournamentSize = 2):
        self.bagSize = bagSize
        #Generate the population using the popuationGenerator function
        self.population = populationGenerator(populationSize, bagSize)
        self.populationSize = populationSize
        self.fitnessFunction = fitnessFunction
        #Compute the fitness of each infividua
        self.fitness = [0] * self.populationSize
        self.computeFitness()
        self.tournamentSize = tournamentSize
        #search the individual with the best fitness
        self.bestbag = None
        self.getBest()
        self.mutationRate = mutationRate

    #This method returns the infividual with the best fitness function
    def getBest(self):
        bestValue = 0
        bestIndividual = None
        for individual in self.population:
            if individual.solutionValue > bestValue:
                bestValue = individual.solutionValue
                bestIndividual = individual
        self.bestbag = bestIndividual
    #This method updates the fitness vector of the knapsack with the current fitness of each individual
    def computeFitness(self):
        self.fitness = []
        for bag in self.population:
            self.fitness.append(self.fitnessFunction(bag))
    #This method selects the best individuals in the population, it randomly chooses a subset of the initial population
    #And selects the best of them, discarding the rest. The size of the subset is given in the tournamentSize field of the
    #Class.
    def selection(self):
        choosen = []
        while len(self.population) >= self.tournamentSize:
            bestfit = 0
            #Randomly select individual to be paired
            for i in range(self.tournamentSize):
                try:
                    #Pick a random index in the population
                    idx = random.randrange(len(self.population)-1)
                    #Get the fitness of the selected individual and remove from fitness and population lists
                    score = self.fitness.pop(idx)
                    bag = self.population.pop(idx)
                    #If the selected individual is better than the current best individual of this iteration, replace
                    if score > bestfit:
                        bestfit = score
                        bestbag = bag
                #If there arent enough individuals left in the population break.
                except ValueError:
                    break
            choosen.append(bestbag)
        #Add the remaining individuals to the new population
        for remaining in self.population:
            choosen.append(remaining)
        #Update the population vector and the fitness vector
        self.population = choosen
        self.computeFitness()
    #This method generates new individual from the current population, using the crossOver operator. It randomly selects
    #2 individuals, and swaps the solution of those individual at a random pivot point
    def crossOver(self):
        newBags = []
        #Generate new bags until the population is the original population
        while len(newBags) < self.populationSize:
            #Randomly choose 2 individuals
            idx1 = random.randrange(len(self.population)-1)
            idx2 = random.randrange(len(self.population)-1)
            #If the selected individuals are the same, repeat
            while idx1 == idx2:
                idx2 = random.randrange(len(self.population)-1)

            bag1 = self.population[idx1]
            bag2 = self.population[idx2]
            #Randomly select a pivot point
            splitidx = random.randrange(len(self.population))
            #Create 2 new individuals, swaping the genes of both individuals after the pivot point
            newSolution1 = bag1.solution.tolist()[0:splitidx] + (bag2.solution.tolist()[splitidx:])
            newSolution2 = bag2.solution.tolist()[0:splitidx] + (bag1.solution.tolist()[splitidx:])
            #Create new Knapsacks with the new solutions, the Knapsack constructor will ensure that the new solutions dont
            #Exceed the maximun capacity of the bag, randomly deleting items if tahat threshold is exceeded
            newBag1 = Knapsack(self.bagSize, solution = newSolution1)
            newBag2 = Knapsack(self.bagSize, solution = newSolution2)
            #Add the new Bags to the vector
            newBags.append(newBag1)
            newBags.append(newBag2)
        #Udate population, fitness and best solution
        self.population = newBags
        self.computeFitness()
        self.getBest()
    #This method Randomly modifies randomly choosen individuals of the population, changing and item of the solution for
    #Another one. The new item is choosen so the weight of the bag wont exceed its maximun capacity. If no valid item is
    # able to bve added, then the mutation deletes one randomly.
    def mutation(self):
        result = []
        for individual in self.population:
            #For each individual get its solution
            solution = individual.solution
            #With a mutationRate chance, decide if the individual is mutated
            if random.random() < self.mutationRate:
                #Randomly select one of the non zero values of the solution
                nonZero = np.nonzero(solution)
                removeIdx = np.random.choice(nonZero[0])
                #Decrease the number of items at the choosen index by 1.
                solution[removeIdx] -= 1
                #Randomly select one of the items to be added instead
                newIdx = random.randint(0,len(individual.weights)-1)
                #Add the new Item to the bag
                solution[newIdx] += 1
                solution = np.array(solution)
                #Compute the weight of the new solution
                weight = np.dot(individual.weights,solution)
                #The tried set stores all the indexes that have been already tried
                tried = set([])
                #If the weight of the bag exceeds its capacity and not all indexes have been tried
                while weight > self.bagSize and len(tried) < len(individual.weights):
                    #Add the last index to the tried set
                    tried.add(newIdx)
                    #Generate and try new index
                    solution[newIdx] -= 1
                    newIdx = random.randint(0, len(individual.weights) - 1)
                    solution[newIdx] += 1
                    weight = np.dot(individual.weights, solution)
                #Create a new individual with the resulting solution, if at this point the weight of the solution exceeds
                #The bag capacity, the constructor will randomly delete items until the solution is valid
                individual = Knapsack(self.bagSize,solution=solution)
            result.append(individual)
        #update population, fitness and best individual
        self.population = result
        self.computeFitness()
        self.getBest()

    #This emthod defines the behaviour of str(KnapsackSolver), it returns and string with all the individuals information
    def __str__(self):
        string = ''
        for i,individual in enumerate(self.population):
            string+="Individual: {}   ".format(i)+str(individual)+"\n"
        return string

if __name__ == '__main__':
    #Create a solver object
    solver = KnapsackSolver(100, 100, fitnessFunction, tournamentSize = 3)
    #Iterate 100 generations
    for i in range(100):
        solver.selection()
        solver.crossOver()
        solver.mutation()
        print("Generation: {}, ".format(i)+str(solver.bestbag))