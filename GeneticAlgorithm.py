import string
import random
from random import randrange
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#This function Creates a list of random string of characters
def wordGenerator(wordlenght, n):
    result = []
    #Create n strings
    while len(result)<n:
        #start with a empty string
        word = ''
        #Add characters randomly selected until the string has the specified length
        for i in range(wordlenght):
            #add a random character from the set of printable characters
            word+=(random.choice(string.printable))
        result.append(word)
    return result
#This function computes the fitness of a certain word, definined as the number of characters that are different from the target
def fitnessFunction(word1, word2):
        fitness = 0
        #For each character, compare it with the corresponding character of the target word, if they are not the same, add 1 to the fitness
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                fitness += 1
        return fitness
#The class WordSearcherEvolution defines the Genetic algorithm for the word search
class WordSearcherEvolution:
    #The constructor receives the wordGenerator, the fitnessFunction and the searched word, additionally parameteres can
    #be given to the model
    def __init__(self, wordGenerator, fitnessFunction, searchedWord, populationSize = 100,mutationRate = 0.2, tournamentSize =5):
        self.populationSize = populationSize
        self.enableMutation=True
        self.mutationRate = mutationRate
        self.population = wordGenerator(len(searchedWord), self.populationSize)
        self.fitnessFunction = fitnessFunction
        self.tournamentSize=tournamentSize
        self.bestFitness = sys.maxsize
        self.bestWord = ''
        self.fitness = [sys.maxsize] * self.populationSize
        self.searchedWord = searchedWord
    #This method computes the fitness of the population
    def computeFitness(self, real):
        self.fitness = []
        for word in self.population:
            self.fitness.append(self.fitnessFunction(word, real))

    # This method selects the best individuals in the population, it randomly chooses a subset of the initial population
    # And selects the best of them, discarding the rest.
    def selectTournament(self):
        choosen = []
        while self.fitness:
            bestfit = sys.maxsize
            bestword = ''
            for i in range(self.tournamentSize):
                try:
                    idx = randrange(len(self.fitness))
                    score = self.fitness.pop(idx)
                    word = self.population.pop(idx)
                    if score < bestfit:
                        bestfit = score
                        bestword = word
                except ValueError:
                    break
            choosen.append(bestword)
        self.population = choosen

    # This method generates new individuals from the current population, using the crossOver operator. It randomly selects
    # 2 individuals, and swaps the solution of those individual at a random pivot point
    def crossOver(self):
        newWords = []
        while len(newWords) < self.populationSize:
            idx1 = randrange(len(self.population))
            idx2 = randrange(len(self.population))
            while idx1 == idx2:
                idx2 = randrange(len(self.population))
            word1 = self.population[idx1]
            word2 = self.population[idx2]
            splitidx = randrange(len(self.population))
            newWord = word1[0:splitidx] + word2[splitidx:]
            newWords.append(newWord)
        self.population = newWords

    # This method Randomly modifies randomly choosen individuals of the population, changing and item of the solution for
    # Another one. The new item is choosen so the weight of the bag wont exceed its maximun capacity. If no valid item is
    # able to bve added, then the mutation deletes one randomly.
    def mutate(self):
        result = []
        for word in self.population:
            if random.random() < self.mutationRate:
                idx = randrange(len(word))
                stringaslist = list(word)
                stringaslist[idx] = random.choice(string.printable)
                result.append("".join(stringaslist))
            else:
                result.append(word)
        return result
    #This method performs a generation of the genetic algorithm, selecting the best individuals, mutating them and obtaining new ones
    def generation(self):
        self.computeFitness(self.searchedWord)
        bestidx = self.fitness.index(min(self.fitness))
        self.bestFitness = min(self.fitness)
        self.bestWord = self.population[bestidx]
        self.selectTournament()
        self.crossOver()
        if self. enableMutation:
            self.population = self.mutate()



if __name__=='__main__':
    words = ['helpless', 'Wrapping everything together','which we can also chain by the gradient with respect to the centred input $\hat{h}_{kl}$ to break down the problem a little more']
    initialPopulation = [10, 50, 100, 500, 1000, 5000, 10000]
    mutationRate = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    ax = []
    for word in words:
        populationGeneration = []
        for populationSize in initialPopulation:
            mutationGeneration = []
            for prob in mutationRate:
                evolution = WordSearcherEvolution(wordGenerator, fitnessFunction, word, populationSize = populationSize,mutationRate = prob)
                i=0
                while evolution.bestFitness > 0:
                    if i >= 1000:
                        break
                    evolution.generation()
                    i+=1
                print('Generation: {}, mutation prob: {}, population: {}'.format(i, prob, populationSize))
                mutationGeneration.append(i)
            populationGeneration.append(mutationGeneration)
        data = np.array(populationGeneration)
        print(data)
        plt.figure()
        cmap = sns.cm.rocket_r
        ax = sns.heatmap(data, yticklabels = initialPopulation, xticklabels=mutationRate,annot=True, cbar=False, cmap = cmap)
        ax.set_ylim(len(initialPopulation) - 0.5, -0.5)
        plt.xlabel('mutation Rate')
        plt.ylabel('Population')

        #plt.title('number of generation requiered for different mutation rates and population size')
        plt.savefig('word_lenght_{}_heatmap.png'.format(len(word)))