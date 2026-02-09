"""
Name: Carla Fabiana Lorena Martinez Becerra
Date: 11/3/2025
Term: FA25
Course: ES1093

Project 06
"""


import random
import sys


# =================== Top Level Variables ===========

# Parameter list Indexes
IDX_CalvingInterval = 0
IDX_PercentDarted = 1
IDX_JuvenileAge = 2
IDX_MaxAge = 3
IDX_ProbCalfSurvival = 4
IDX_ProbAdultSurvival = 5
IDX_ProbSeniorSurvival = 6
IDX_CarryingCapacity = 7
IDX_NumYears = 8

# Indivudal Elephant list Indexes
IDX_Gender = 0
IDX_Age = 1
IDX_MonthsPregnant = 2
IDX_MonthsContraceptiveRemaining = 3


# =================== FUNCTIONS ===================
def newElephant(parameters, age):
    
    calvingInterval = parameters[IDX_CalvingInterval]
    
    juvenileAge = parameters[IDX_JuvenileAge]
    
    maxAge = parameters[IDX_MaxAge]

    elephant = [0, 0, 0, 0]

    elephant[IDX_Gender] = random.choice(["m","f"])

    elephant[IDX_Age] = age

    """
    Dave Lab thinking 
    if random.random() < 0.5:
        elephant[IDX_Gender] = "f"
    else:
        elephant[IDX_Gender] = "m"
    """
    
    if elephant[IDX_Gender] == "f": # if the elephant is female
        if juvenileAge < age < maxAge: # and if that female is of breeding age
            if random.random() < (1.0 / calvingInterval):
                elephant[IDX_MonthsPregnant] = random.randint(1, 22) # assign a random num between 1-22 to the elephant list in the months preg column

    return elephant


def initPopulation(paramlist):
    
    carryingCapacity = paramlist[IDX_CarryingCapacity]

    population = []

    for x in range(carryingCapacity):
        #population.append(newElephant(paramlist, random.randint(1, paramlist[IDX_MaxAge]))), realized it might be easier to debug if i take it step by step
        age = random.randint(1, paramlist[IDX_MaxAge])
        e = newElephant(paramlist, age)
        population.append(e) 

    return population
    

def incrementAge(population):

    for e in population:
        e[IDX_Age] += 1

    return population


def calcSurvival(parameters, population):

    # Parameters
    juvenileAge = parameters[IDX_JuvenileAge]
    maxAge = parameters[IDX_MaxAge]
    pCalf = parameters[IDX_ProbCalfSurvival]
    pAdult = parameters[IDX_ProbAdultSurvival]
    pSenior = parameters[IDX_ProbSeniorSurvival]

    newPopulation = [] # accumulator to collect elephants that survive this year

    for e in population: # iterating through each list within the list
        age = e[IDX_Age] # reading this elephant's age to decide which prob applies to it

        if age <= 1.0: # if the elephant is a calf
            p = pCalf # use calf survival probability
        elif age < maxAge: # if the elephant is an adult
            p = pAdult # use adult survival probability
        else: # otherwise it's a grandpa
            p = pSenior # use senior survival probability

        if random.random() < p: # if it survives
            newPopulation.append(e) # we carry it to the new population list
    
    return newPopulation # survivors list


def dartElephants(parameters, population):

    # Parameters
    percentDarted = parameters[IDX_PercentDarted]
    juvenileAge = parameters[IDX_JuvenileAge]
    maxAge = parameters[IDX_MaxAge]

    for e in population:
        gender = e[IDX_Gender]
        
        if gender == "f": # if elephant is a she
            age = e[IDX_Age]

            if juvenileAge <= age <= maxAge: # and if that elephant is adult
                if random.random() < percentDarted: # dart this adult if it passes the prob of darting
                    e[IDX_MonthsPregnant] = 0 # darting ends any current pregnancy immediately
                    e[IDX_MonthsContraceptiveRemaining] = 22 # she also starts contraception countdown at 22 months

    return population


def cullElephants(parameters, population):

    # Parameters
    carryingCapacity = parameters[IDX_CarryingCapacity]

    currentSize = len(population) # counting how many elephants we currently have

    excess = currentSize - carryingCapacity # how many need to be removed

    if excess > 0: # if we exceed capacity
        numCulled = excess # we will cull exactly the excess
    else: #otherwise
        numCulled = 0 # we cull none
    
    if numCulled > 0: # if there IS excess
        random.shuffle(population) # shuffle them so the removal/culling is random
        newPopulation = population[:carryingCapacity] # keep the elephants until the carrying capacity
    else: # otherwise
        newPopulation = population[:] # make a copy so we don't affect the original list, and just keep it as it was because no culling was needed!

    return newPopulation, numCulled


def controlPopulation(parameters, population):

    # Parameters
    percentDarted = parameters[IDX_PercentDarted]

    if percentDarted == 0: # if the parameter value for "percent darted" is zero:
        newPop, numCulled = cullElephants(parameters, population) # call cullElephants, storing the return values in a two variables
    else:
        newPop = dartElephants(parameters, population) # call dartElephants and store the result in a variable named newpop
        numCulled = 0 # set a variable named numCulled to zero
    
    return (newPop, numCulled)


def simulateMonth(parameters, population):
    
    # Parameters
    calvingInterval = parameters[IDX_CalvingInterval]
    juvenileAge = parameters[IDX_JuvenileAge]
    maxAge = parameters[IDX_MaxAge]

    # Monthly conception probability when elephanty is just fertile (not pregnant, no contraception)
    monthlyPregProb = 1.0 / (calvingInterval * 12.0 - 22.0)

    for e in population:
        gender = e[IDX_Gender] # assign to gender the IDXGender item in e
        age = e[IDX_Age] # assign to age the IDXAge item in e
        monthsPregnant = e[IDX_MonthsPregnant] # assign to monthsPregnant the IDXMonthsPregnant item in e
        monthsContraceptive = e[IDX_MonthsContraceptiveRemaining] # assign to monthsContraceptive the IDXMonthsContraceptiveRemaining item in e
        
        if gender == "f" and (juvenileAge < age < maxAge): # if gender is female and the elephant is an adult
            if monthsContraceptive > 0: # if monthsContraceptive is greater than zero
                e[IDX_MonthsContraceptiveRemaining] -= 1 # decrement the months of contraceptive left (IDXMonthsContraceptiveRemaining element of e) by one
            elif monthsPregnant > 0: # if monthsPregnant is greater than zero
                if monthsPregnant >= 22: # if monthsPregnant is greater than or equal to 22
                    calf = newElephant(parameters, 1) # create a new elephant of age 1 
                    population.append(calf) # and append it to the population list
                    e[IDX_MonthsPregnant] = 0 # reset the months pregnant (the IDXMonthsPregnant element of e) to zero
                else:
                    e[IDX_MonthsPregnant] = monthsPregnant + 1 # increment the months pregnant (IDXMonthsPregnant element of e) by 1
            else:
                if random.random() < monthlyPregProb: # if the elephant becomes pregnant
                    e[IDX_MonthsPregnant] = 1 # set months pregnant (IDXMonthsPregnant element of e) to 1

    return population


def simulateYear(parameters, population):

    population = calcSurvival(parameters, population)

    population = incrementAge(population)

    for i in range(12):
        population = simulateMonth(parameters, population)

    return population


def calcResults(parameters, population, numCulled):

    # Parameters
    juvenileAge = parameters[IDX_JuvenileAge]
    maxAge = parameters[IDX_MaxAge]

    # Counters
    calves = 0
    juveniles = 0
    adultsM = 0
    adultsF = 0
    seniors = 0

    for e in population: # for each elephant
        age = e[IDX_Age] # to check out its age
        gender = e[IDX_Gender] # to check out sex

        if age < 0:
            pass
        elif age == 1:
            calves += 1
        elif age <= juvenileAge:
            juveniles += 1
        elif age < maxAge:
            if gender == "f":
                adultsF += 1
            else:
                adultsM += 1
        else: # seniors ARE the max age, so that would be the >=
            seniors += 1

    totalPop = len(population) # total population size

    return [totalPop, calves, juveniles, adultsM, adultsF, seniors, numCulled]


def runSimulation(parameters):
    
    # Parameters
    popsize = parameters[IDX_CarryingCapacity]
    numYears = parameters[IDX_NumYears]
    
    # init the population
    population = initPopulation(parameters)
    
    [population, numCulled] = controlPopulation(parameters, population)
    
    # run the simulation for N years, storing the results
    results = []

    for i in range(numYears):
        population = simulateYear(parameters, population)
        
        [population, numCulled] = controlPopulation(parameters, population)
        
        #results.append(calcResults(parameters, population, numCulled))

        row = calcResults(parameters, population, numCulled) # [total, calves, juveniles, adultM, adultF, seniors, numCulled]

        results.append(row) # storing this year's stats

        #print(row[0]) # printing total population value for this year
        
        if row[0] > 2 * popsize or row[0] == 0 : # cancel early, out of control
            #print("Terminating early")
            break
    
    return results


def defaultParameters():
    
    # Parameters
    calvingInterval = 3.1 # Years between calves, on average
    percentDarted = 0.0 # percent of females darted each year as probability
    juvenileAge = 12 # Juveniles are age <= 12
    maxAge = 60 # Seniors are age >= 60
    probCalfSurvival = 0.85 # Yearly survival probability for calves
    probAdultSurvival = 0.996 # Yearly survival probability for adults
    probSeniorSurvival = 0.20 # Yearly survival probability for seniors
    carryingCapacity = 1000 # cap
    numYears = 200 # Years to simulate

    return [calvingInterval, percentDarted, juvenileAge, maxAge, probCalfSurvival, probAdultSurvival, probSeniorSurvival, carryingCapacity, numYears]


def elephantSim(percDart, inputParameters = None):
    
    if inputParameters is None: # if no parameter list was provided
        parameters = defaultParameters() # use the default parameters list
    else: # otherwise
        parameters = inputParameters # use the provided parameters list
    
    parameters[IDX_PercentDarted] = percDart # overwrite the percent darted in the parameters list

    #print("percDart was set to", parameters[IDX_PercentDarted])
    #print("parameters of the function are:", percDart, "and", inputParameters)

    results = runSimulation(parameters) # run the simulation once and store the list of yearly rows

    for i in range(4):
        results = results + runSimulation(parameters) # add another run’s rows to the results list

    #print("initial pop:", results[0][0])

    totalSum = 0.0 # accumulator for total population across all rows

    for row in results: # loop over every yearly row in the combined results
        totalSum = totalSum + row[0] # add the total population from this year which is the first element

    average = totalSum / len(results) # compute the average total population across all rows

    k = parameters[IDX_CarryingCapacity]
    diff = k - average # read the carrying capacity from the parameters list

    #print("the average length of the population:", average, "and the carrying capacity", k)

    return int(diff)


def main(argv):

    #random.seed(0) # for section 10, I fixed the simulations with the random generator, so runs are comparable and the diff trials of % darted reflect THE %, not luck/randomness

    # Usage statement
    if len(argv) != 2:
        print("Only one argument is needed: probability of darting")
        return

    # Reading darting probaility from command line
    percentDarted = float(argv[1])

    # Parameters
    calvingInterval = 3.1 # Years between calves, on average
    juvenileAge = 12 # Juveniles are age <= 12
    maxAge = 60 # Seniors are age >= 60
    probCalfSurvival = 0.85 # Yearly survival probability for calves
    probAdultSurvival = 0.996 # Yearly survival probability for adults
    probSeniorSurvival = 0.20 # Yearly survival probability for seniors
    carryingCapacity = 7000 # Population cap
    numYears = 200 # Years to simulate

    parameters = [calvingInterval, percentDarted, juvenileAge, maxAge, probCalfSurvival, probAdultSurvival, probSeniorSurvival, carryingCapacity, numYears]

    # Running the simulation once and get the list of yearly results
    results = runSimulation(parameters)

    # Printing the last item in the results list (final year)
    last = results[-1]
    print("Final year results:", last)

    # Averages
    nYears = len(results) # number of simulated years
    numCols = len(last) # number of columns in each row (just taking "last" because all are the same as that one)
    sums = [0.0] * numCols # column accumulators

    for r in range(nYears): # go year by year

        row = results[r] # get the row for this year

        for c in range(numCols): # loop over each column index

            sums[c] += row[c] # add that value to the correct column total

    averages = [] # preparing an empty list to hold column averages

    for i in range(numCols): # loop over columns againnn
        averages.append(sums[i] / nYears) # compute the average for this column and append it

    print("\nAverages over", nYears, "years:")
    print("\tAvg total population: %.2f" % (averages[0]))
    print("\tAvg calves: %.2f" % (averages[1]))
    print("\tAvg juveniles: %.2f" % (averages[2]))
    print("\tAvg adult males: %.2f" % (averages[3]))
    print("\tAvg adult females: %.2f" % (averages[4]))
    print("\tAvg seniors: %.2f" % (averages[5]))
    print("\tAvg culled per year: %.2f" % (averages[6]))


# ====================== TEST CODE ======================
def test():

    calvingInterval = 3.1
    percentDarted = 0.0
    juvenileAge = 12
    maxAge = 60
    probCalfSurvival = 0.85
    probAdultSurvival = 0.996
    probSeniorSurvival = 0.20
    carryingCapacity = 20
    numYears = 200

    parameters = [calvingInterval, percentDarted, juvenileAge, maxAge, probCalfSurvival, probAdultSurvival, probSeniorSurvival, carryingCapacity, numYears]
    
    #print(parameters)

    pop = []

    for i in range(15):
        pop.append(newElephant(parameters, random.randint(1, parameters[IDX_MaxAge])))
    
    #for e in pop:
        #print(e)
    
    # initPopulation
    newPop = initPopulation(parameters)
    print("Creating the population ")
    for x in newPop:
        print(x)

    newPop = incrementAge(newPop)
    print("One year age incremenet")
    for y in newPop: 
        print(y)

    # calcSurvival

    print("Before survival: ", len(pop))
    pop = calcSurvival(parameters, pop)
    print("After survival: ", len(pop))

    pass


if __name__ == "__main__":
    #test()
    main(sys.argv)
