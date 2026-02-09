"""
Bruce Maxwell
Fall 2015
CS 151 Project 6
Test function for elephantSim.

Modified by: Victoria Edwards
Date: 10/15/2025

Purpose: go through the colby intro to cs lab exercises
Source: https://cs.colby.edu/courses/S20/cs152-labs/labs/lab06/
"""

import sys
import elephant

def main(argv):

    for i in range(5):
        probDarting = 0.405 + i * 0.01
        diff = elephant.elephantSim( probDarting )
        print("probDarting %.3f  diff %d" % (probDarting, diff))

    return

if __name__ == "__main__":
    main(sys.argv)

