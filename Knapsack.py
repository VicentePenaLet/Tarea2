import random
import numpy as np

#This class defines  knapsack, it allows to create a knapsack with a certain combination of items, where the weight
#of the items doesnt exceed the bad capacity.
class Knapsack:
    #The contrurctor for the knapsack, the maximum capacity is given in the size variable, and a certain solution can be
    #provided in the solution field. If none is specified, a random solution is generated
    def __init__(self, size, weights = [7, 2, 1, 1, 4], values = [4, 2, 2, 1, 10],solution = None):
        self.size = size
        self.weights = np.array(weights)
        self.values = np.array(values)
        #A solution is a combination of items, these are represented by a vector in which every element is the number of
        #objects in the weights and values arrays in the same index
        self.solution = np.array([0]*len(self.weights))
        #The total weights and values of the current solution
        self.solutionValue = 0
        self.solutionWeight = 0
        #If no solution is given, generate a new one
        if solution is None:
            self.generateSolution()
        else:
            #if a solution given, store it and update the value and weight
            self.solution = np.array(solution)
            self.update()
            #if the solution weight exceeds the capacity of the bag, randomly elimnate items until the weight is valid
            while self.solutionWeight > self.size:
                nonZero = np.nonzero(self.solution)
                removeIdx = np.random.choice(nonZero[0])
                self.solution[removeIdx]-=1
                self.update()
    #This method udates the weights and values of the bag
    def update(self):
        self.solutionValue = np.dot(self.values,self.solution)
        self.solutionWeight = np.dot(self.weights,self.solution)

    #This method randomly generates a valid solution, the solution is such that its weight is close to the bag capacity
    def generateSolution(self):
        while True:
            #Randomly choose and index and add one item to that index solutin
            idx = random.randint(0, len(self.weights)-1)
            #If the weight doesnt exceed the bag capacity, add it to the solution
            if self.solutionWeight + self.weights[idx] < self.size:
                self.solution[idx]+=1
                self.update()
            #If not, end the process
            else:
                break
    #This method defines de behavior of str(kanpsack) used for debugging
    def __str__(self):
        return "Current value: {}, Current Weight: {}, Current Selection: {}".format(self.solutionValue,self.solutionWeight,self.solution)


if __name__=='__main__':
    knapsack = Knapsack(15, solution = [1, 0, 0, 0, 0])
    print(knapsack)