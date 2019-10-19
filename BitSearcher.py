from GeneticAlgorithm import *
#This function Creates a list of random string of 1s and 0s
def BitGenerator(wordlenght, n):
    result = []
    while len(result)<n:
        word = ''
        for i in range(wordlenght):
            word+=(random.choice("01"))
        result.append(word)
    return result
#This function computes the fitness of a certain word, definined as the number of characters that are different from the target
def fitnessFunction(word1, word2):
    fitness = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            fitness += 1
    return fitness

#The class WordSearcherEvolution defines the Genetic algorithm for the bit search, as a sub Class of WordSearchEvolution,
#Only the mutate funciton is changed, by choosing new elements from the 01 string instead of all the printables
class BitSearcher(WordSearcherEvolution):
    def mutate(self):
        result = []
        for word in self.population:
            if random.random() < self.mutationRate:
                idx = randrange(len(word))
                stringaslist = list(word)
                stringaslist[idx] = random.choice("01")
                result.append("".join(stringaslist))
            else:
                result.append(word)
        return result


if __name__=='__main__':
    searchedbit = '101010100001010101101101010101001010101010101'
    evolution = BitSearcher(BitGenerator, fitnessFunction, searchedbit)
    print(evolution.population)
    i = 0
    while evolution.bestFitness > 0:
        evolution.generation()
        i += 1
        print('Generation: {}, best fit = {}'.format(i, evolution.bestWord))