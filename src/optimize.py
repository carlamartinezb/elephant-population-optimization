"""
Name: Carla Fabiana Lorena Martinez Becerra
Date: 11/7/2025
Term: FA25
Course: ES1093

Project 06
"""


import sys
import elephant
import random
import matplotlib.pyplot as plt


# Executes a search to bring the result of the function optfunc to zero.
def optimize(min, # min: minimum parameter value to search
             max, # max: maximum parameter value to search
             optfunc, # optfunc: function to optimize
             parameters = None, # parameters: optional parameter list to pass to optfunc
             tolerance = 0.001, # tolerance: how close to zero to get before terminating the search
             maxIterations = 20, # maxIterations: how many iterations to run before terminating the search
             verbose = False): # verbose: whether to print lots of information or not

    done = False

    while done == False:

        testValue = (max + min) / 2.0 # average

        if verbose == True:
            print("testValue:", testValue)
        
        result = optfunc(testValue, parameters)

        if verbose == True:
            print("result:", result)
        
        if result > 0:
            max = testValue
        elif result < 0:
            min = testValue
        else:
            done = True
        
        if (max - min) < tolerance:
            done = True
        
        maxIterations = maxIterations - 1

        if maxIterations <= 0:
            done = True
        
    return testValue
        

def testEsim():

    res = optimize(0.0, 0.5, elephant.elephantSim, parameters = None, tolerance = 0.001, maxIterations = 20, verbose = True)

    print("res:", res)

    return


# Evaluates the effects of the selected parameter on the dart percentage
def evalParameterEffect(whichParameter, # whichParameter: the index of the parameter to test
                        testmin, # testmin: the minimum value to test 
                        testmax, # testmax: the maximum value to test
                        teststep, # teststep: the step between parameter values to test
                        defaults = None, # defaults: default parameters to use (default value of None)
                        verbose = False):
    
    if defaults == None: # if defaults is None, 
        simParameters = elephant.defaultParameters() #assign to simParameters the result of calling elephant.defaultParameters.
    else:
        simParameters = defaults[:] # else, assign to simParameters a copy of defaults (e.g. simParameters = defaults[:]
    
    results = [] # create an empty list (e.g. results) to hold the results
    
    if verbose:
        print("Evaluating parameter %d from %.3f to %.3f with step %.3f" % (whichParameter, testmin, testmax, teststep)) 
    
    t = testmin # assign to t the value testmin
    
    while t < testmax: # while t is less than testmax
        simParameters[whichParameter] = t # assign to the whichParameter element of simParameters (e.g. simParameters[whichParameter]) the value t
        percDart = optimize(0.0, 0.5, elephant.elephantSim, parameters = simParameters, tolerance = 0.001, maxIterations = 20, verbose = verbose) # assign to percDart the result of calling optimize with the appropriate arguments, including simParameters
        results.append((t, percDart)) # append to results the tuple (t, percDart)
        
        if verbose:
            print("%8.3f \t%8.3f" % (t, percDart))
        
        t = t + teststep # increment t by the value teststep
    
    if verbose:
        print("Terminating")
    
    return results # return the list of results


#---------------------------------------SECTION 8---------------------------------------------

# To create CSVs
def csv(filename, headerX, headerY, rows):
    
    f = open(filename, "w") # new file to write text

    f.write("%s,%s\n" % (headerX, headerY)) # header

    for pair in rows: # loop over each pair in the list
        
        x = pair[0]
        y = pair[1]
        
        f.write("%.3f,%.6f\n" % (x, y))
    
    f.close()

    return


# To plot
def plot(filename, title, xLabel, yLabel, rows):
    
    xs = [] # a list for x values
    ys = [] # a list for y values

    for pair in rows: # loop over each pair in the list
        
        xs.append(pair[0]) # add the x value to the list
        ys.append(pair[1]) # add the y value to the list
    
    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
    return



# 8.a. Vary the adult survival probability from 0.98 to 1.0 in steps of 0.001
def adultSurvival():
    
    whichParameter = elephant.IDX_ProbAdultSurvival
    testMin = 0.98
    testMax = 1.001 # I put it above 1.00 so 1 is actually included when the loop uses "<" in the while loop
    testStep = 0.001

    # This was to try 200 first
    #d = elephant.defaultParameters()
    #d[elephant.IDX_CarryingCapacity] = 200
    #rows = evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults = d, verbose = False)

    rows = evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults = None, verbose = False)

    #print("rows:", rows) # list of (adultSurvival, optimalDart) pairs for a table

    csv("adult_survival.csv", "adult_survival", "optimal_percDart", rows)
    plot("adult_survival.png", "Adult survival vs Optimal darting probability", "Adult survival", "Darting probability", rows)

    return rows


# 8.b. Vary the calf survival probability from 0.80 to 0.90 in steps of 0.01.
def calfSurvival():

    whichParameter = elephant.IDX_ProbCalfSurvival
    testMin = 0.80
    testMax = 0.901 # a little above 0.90 so that 0.90 is included when loop uses "<"
    testStep = 0.01

    rows = evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults = None, verbose = False)

    csv("calf_survival.csv", "calf_survival", "optimal_percDart", rows)
    plot("calf_survival.png", "Calf survival vs Optimal darting probability", "Calf survival", "Darting probability", rows)

    return rows


# 8.c. Varying the senior survival probability from 0.1 to 0.5 in steps of 0.05.
def seniorSurvival():

    whichParameter = elephant.IDX_ProbSeniorSurvival
    testMin = 0.10
    testMax = 0.501 # same logic as before
    testStep = 0.05

    rows = evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults = None, verbose = False)

    csv("senior_survival.csv", "senior_survival", "optimal_percDart", rows)
    plot("senior_survival.png", "Senior survival vs Optimal darting probability", "Senior survival", "Darting probability", rows)

    return rows


# 8.d. Varying the calving interval from 3.0 to 3.4 in steps of 0.05.
def calvingInterval():

    whichParameter = elephant.IDX_CalvingInterval
    testMin = 3.0
    testMax = 3.401
    testStep = 0.05
    
    rows = evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults = None, verbose = False)
    
    csv("calving_interval.csv", "calving_interval", "optimal_percDart", rows)
    plot("calving_interval.png", "Calving interval vs Optimal darting probability", "Calving interval (years)", "Darting probability", rows)
    
    return rows


# 8.e. Varying the max age from 56 to 66 in steps of 2.
def maxAge():
    
    whichParameter = elephant.IDX_MaxAge
    testMin = 56
    testMax = 66.001
    testStep = 2

    rows = evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults = None, verbose = False)
    
    csv("max_age.csv", "max_age", "optimal_percDart", rows)
    plot("max_age.png", "Max age vs Optimal darting probability", "Max age (years)", "Darting probability", rows)
    
    return rows  


#--------------------------------------Other project sections----------------------------------------------
# A function that returns x - target
def target(x, pars):
    return x - 0.73542618


# Tests the binary search using a simple target function.
# Try changing the tolerance to see how that affects the search.
def testTarget():
    res = optimize( 0.0, 1.0, target, tolerance = 0.000001, verbose=True)
    print( res )
    return


if __name__ == "__main__":
    #testTarget()
    #testEsim()
    #evalParameterEffect(elephant.IDX_ProbAdultSurvival, 0.98, 1.0, 0.001, verbose = True)
    #rows = adultSurvival()
    #rows = calfSurvival()
    #rows = seniorSurvival()
    #rows = calvingInterval()
    rows = maxAge()