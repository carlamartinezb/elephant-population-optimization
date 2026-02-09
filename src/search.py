"""
Name: Carla Fabiana Lorena Martinez Becerra
Date: 10/27/2025
Term: FA25
Course: ES1093

Lab 06
"""


import random
import sys


def searchSortedList(myList, value):
    # assign to the variable done, the value False
    done = False
    
    # assign to the variable found, the value False
    found = False

    # assign to the variable count, the value 0
    count = 0

    # assign to the variable maxIdx, the one less than the length of mylist
    maxIdx = len(myList) - 1

    # assign to the variable minIdx, the value 0
    minIdx = 0

    # start a while loop that executes while done is not True
    while done == False:
        # increment count (which keeps track of how many times the loop executes)
        count += 1
        # assign to testIndex the average of maxIdx and minIdx (use integer math)
        testIndex = (maxIdx + minIdx) // 2
        
        # if the myList value at testIndex is less than value
        if myList[testIndex] < value:
            minIdx = testIndex +1 # assign to minIdx the value testIndex + 1
        # elif the myList value at testIndex is greater than value
        elif myList[testIndex] > value:
            maxIdx = testIndex -1 # assign to maxIdx the value testIndex - 1
        else:
            done = True # set done to True
            found =  True # set found to True
        
        # if maxIdx is less than minIdx
        if maxIdx < minIdx:
            done = True # set done to True
            found = False # set found to False
    
    return (found, count)


def test(searchVal):
    
    a = []
    
    for i in range(10000):
        a.append(random.randint(0, 100000))
    
    a.append(searchVal)
    
    a.sort()
    
    print(searchSortedList(a, searchVal))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("USAGE: python <name of the code file> <searchVal>")
        exit()

    searchVal = int(sys.argv[1]) # typecasting from string to int
    
    test(searchVal) # calling test