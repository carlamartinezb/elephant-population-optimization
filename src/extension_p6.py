"""
Name: Carla Fabiana Lorena Martinez Becerra
Date: 11/7/2025
Term: FA25
Course: ES1093

Uber-extension 06
"""


import sys
import elephant
import optimize
import random
import matplotlib.pyplot as plt


def csvs(filename, headerX, headerY, headerZ, rows): # to write a three column csv file
    
    f = open(filename, "w")
    
    f.write("%s,%s,%s\n" % (headerX, headerY, headerZ))
    
    for triple in rows: # loop over each triple in the list
        x = triple[0] # read the adult survival value
        y = triple[1] # read the calf survival value
        z = triple[2] # read the optimal darting probability value
        
        f.write("%.3f,%.3f,%.6f\n" % (x, y, z)) # to write one row
    
    f.close()
    
    return


def heatmap(filename, title, xlabel, ylabel, xVals, yVals, grid): # to save a heatmap image
    
    #had to edit a lot this thing because it gave not so accurate heatmaps

    plt.figure(figsize = (8, 5)) # making the figure a bit wider so labels fit properly
    plt.imshow(grid, origin = "lower", aspect = "auto")
    plt.colorbar(label = "Optimal darting probability")

    ax = plt.gca() # making axes to get ticks
    ax.set_xticks(list(range(len(xVals)))) #to put one tick at each column index
    ax.set_xticklabels(["%.2f" % v for v in xVals], rotation = 45, ha = "right") # labeling each x tick
    ax.set_yticks(list(range(len(yVals)))) # put one tick at each y position
    ax.set_yticklabels(["%.3f" % v for v in yVals]) # labeling each y tick

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename) 
    plt.close()

    return


def twoParameter(): # to run the two-parameter process for max age and senior survival
    
    paramsBase = elephant.defaultParameters() # get a fresh default parameter list
    #paramsBase[elephant.IDX_CarryingCapacity] = 200 # reducing carrying capacity for speed

    maxAgeVals = [] # list to hold the max age values for the y axis
    seniorVals = [] # list to hold the senior survival values for the x axis
    resultsTriples = [] # list to hold (maxAge, seniorSurvival, optimalPercDart) rows
    grid = [] # 2nd list to hold heatmap rows where each row is a list of z values

    m = 56 # start the max age

    while m <= 64: # loop until sixty four (but inclusive!)
        
        maxAgeVals.append(m) # remember this max age value for the y axis labels
        rowZ = [] # list to hold one heatmap row for this max age

        s = 0.10 # start the senior survival

        isFirstRow = (m == 56) # this is true only on the first max age row

        while s <= 0.50 + 1e-9: # loop til that (and added the 1e-9 so that  0.50 is always included)

            if isFirstRow: # only on the first row we collect all x axis tick values
                seniorVals.append(s) # add this senior survival value to the x ticks

            p = paramsBase[:] # copy of the base parameters to modify safely
            p[elephant.IDX_MaxAge] = m # set the max age value in the parameter list
            p[elephant.IDX_ProbSeniorSurvival] = s # set the senior survival in the parameter list

            z = optimize.optimize(0.0, 0.5, elephant.elephantSim, parameters = p, tolerance = 0.001, maxIterations = 20, verbose = False) # to find the optimal darting probability for this pair

            resultsTriples.append((m, s, z)) # store the triple to the results list
            rowZ.append(z) # add the z value to the current heatmap row

            s = s + 0.10 # increment the senior survival by one tenth

        grid.append(rowZ) # add the completed row to the heatmap grid
        
        m = m + 2 # increment the max age by two years
    
    return resultsTriples, seniorVals, maxAgeVals, grid


def runUber(): 
    
    resultsTriples, seniorVals, maxAgeVals, grid = twoParameter()
    
    csvs("uber_maxAge_senior.csv", "max_age", "senior_survival", "optimal_percDart", resultsTriples)
    heatmap("uber_maxAge_senior.png", "Optimal darting for max age vs senior survival", "Senior survival", "Max age (years)", seniorVals, maxAgeVals, grid)
    
    print("am done") # just checkinggg
    
    return


if __name__ == "__main__":
    runUber()
